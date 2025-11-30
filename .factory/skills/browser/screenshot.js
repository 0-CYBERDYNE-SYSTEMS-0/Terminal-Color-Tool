#!/usr/bin/env node

const puppeteer = require('puppeteer-core');
const path = require('path');

async function takeScreenshot() {
  const os = require('os');
  const tempDir = os.tmpdir();
  const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
  const filename = `screenshot-${timestamp}.png`;
  const filepath = path.join(tempDir, filename);

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
    await page.screenshot({ path: filepath, fullPage: false });
    console.log(`✓ Screenshot saved: ${filepath}`);

    await browser.disconnect();
  } catch (error) {
    console.error('Error: Make sure Chrome is running with remote debugging on port 9222');
    console.error('Run: start.js first');
    process.exit(1);
  }
}

takeScreenshot().catch(console.error);
