#!/usr/bin/env node

const puppeteer = require('puppeteer-core');

async function evaluateJs() {
  const jsCode = process.argv[2];

  if (!jsCode) {
    console.error('Please provide JavaScript code: node eval.js <code>');
    console.error('Example: node eval.js "document.title"');
    process.exit(1);
  }

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
    
    try {
      const result = await page.evaluate(`(${jsCode})`);
      console.log('Result:', result);
    } catch (error) {
      console.error('JavaScript evaluation error:', error.message);
    }

    await browser.disconnect();
  } catch (error) {
    console.error('Error: Make sure Chrome is running with remote debugging on port 9222');
    console.error('Run: start.js first');
    process.exit(1);
  }
}

evaluateJs().catch(console.error);
