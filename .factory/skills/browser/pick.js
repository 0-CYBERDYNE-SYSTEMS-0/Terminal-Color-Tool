#!/usr/bin/env node

const puppeteer = require('puppeteer-core');

async function pickElements() {
  const prompt = process.argv[2] || 'Click elements to pick them';

  try {
    const browser = await puppeteer.connect({
      browserURL: 'http://localhost:9222'
    });

    const pages = await browser.pages();
    if (pages.length === 0) {
      console.error('No tabs open. Navigate to a page first.');
      process.exit(1);
    }

    const page = pages[0];

    // Inject the picker script
    await page.addScriptTag({
      content: `
        (function() {
          let selectedElements = [];
          let isMultiSelect = false;
          
          const highlightElement = (element) => {
            if (selectedElements.includes(element)) {
              element.style.outline = '3px solid #ff0000';
              element.style.outlineOffset = '2px';
            } else {
              element.style.outline = '3px solid #0066cc';
              element.style.outlineOffset = '2px';
            }
          };

          const cleanup = () => {
            document.querySelectorAll('[data-droid-picked]').forEach(el => {
              el.style.outline = '';
              el.removeAttribute('data-droid-picked');
            });
          };

          const getElementInfo = (element) => {
            const tagName = element.tagName.toLowerCase();
            const id = element.id ? '#' + element.id : '';
            const classes = element.className ? '.' + element.className.split(' ').join('.') : '';
            const text = element.textContent.trim().substring(0, 100);
            
            return {
              tag: tagName,
              id: id,
              classes: classes,
              selector: tagName + id + classes,
              text: text
            };
          };

          const handleClick = (event) => {
            event.preventDefault();
            event.stopPropagation();
            
            const element = event.target;
            const index = selectedElements.indexOf(element);
            
            if (event.ctrlKey || event.metaKey) {
              // Multi-select mode
              if (index > -1) {
                selectedElements.splice(index, 1);
                element.style.outline = '';
                element.removeAttribute('data-droid-picked');
              } else {
                selectedElements.push(element);
                element.setAttribute('data-droid-picked', 'true');
                highlightElement(element);
              }
            } else {
              // Single select
              cleanup();
              selectedElements = [element];
              element.setAttribute('data-droid-picked', 'true');
              highlightElement(element);
            }
          };

          const handleKeyDown = (event) => {
            if (event.key === 'Enter') {
              cleanup();
              const results = selectedElements.map(getElementInfo);
              window.droidPickerResults = results;
              window.droidPickerDone = true;
              console.log('✓ Selection complete. Found', results.length, 'elements.');
            }
          };

          console.log('${prompt}');
          console.log('Click to select, Cmd/Ctrl+Click for multi-select, Enter to finish.');
          
          document.addEventListener('click', handleClick, true);
          document.addEventListener('keydown', handleKeyDown);
        })();
      `
    });

    console.log('Interactive picker started. Click elements to select them, Cmd/Ctrl+Click for multi-select, Enter to finish.');

    // Wait for picker to complete
    await page.waitForFunction(() => window.droidPickerDone, { timeout: 60000 });

    const results = await page.evaluate(() => window.droidPickerResults);
    
    console.log('\nSelected Elements:');
    results.forEach((result, index) => {
      console.log(`${index + 1}. ${result.selector}`);
      console.log(`   Tag: ${result.tag}, ID: ${result.id || 'none'}, Classes: ${result.classes || 'none'}`);
      if (result.text) {
        console.log(`   Text: "${result.text}"`);
      }
      console.log('');
    });

    await browser.disconnect();
  } catch (error) {
    console.error('Error: Make sure Chrome is running with remote debugging on port 9222');
    console.error('Run: start.js first');
    process.exit(1);
  }
}

pickElements().catch(console.error);
