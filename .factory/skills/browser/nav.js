#!/usr/bin/env node

const puppeteer = require('puppeteer-core');

async function navigateToUrl() {
  const url = process.argv[2];
  const openNew = process.argv.includes('--new');

  if (!url) {
    console.error('Please provide a URL: node nav.js <url> [--new]');
    process.exit(1);
  }

  try {
    const browser = await puppeteer.connect({
      browserURL: 'http://localhost:9222'
    });

    const pages = await browser.pages();
    let page;

    if (openNew || pages.length === 0) {
      page = await browser.newPage();
    } else {
      page = pages[0];
    }

    await page.goto(url, { waitUntil: 'networkidle2' });
    console.log(`✓ Navigated to ${url}${openNew ? ' (new tab)' : ''}`);

    await browser.disconnect();
  } catch (error) {
    console.error('Error: Make sure Chrome is running with remote debugging on port 9222');
    console.error('Run: start.js first');
    process.exit(1);
  }
}

navigateToUrl().catch(console.error);
