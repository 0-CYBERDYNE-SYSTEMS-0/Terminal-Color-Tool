#!/usr/bin/env node

const puppeteer = require('puppeteer-core');
const path = require('path');
const fs = require('fs');

async function startChrome() {
  const useProfile = process.argv.includes('--profile');
  
  const args = [
    '--remote-debugging-port=9222',
    '--no-sandbox',
    '--disable-setuid-sandbox',
    '--disable-dev-shm-usage',
    '--disable-accelerated-2d-canvas',
    '--no-first-run',
    '--no-zygote',
    '--single-process',
    '--disable-gpu'
  ];

  if (useProfile) {
    const profileDir = path.join(process.env.HOME || process.env.USERPROFILE, '.config', 'google-chrome', 'Default');
    if (fs.existsSync(profileDir)) {
      args.push(`--user-data-dir=${profileDir}`);
      console.log('✓ Chrome started on :9222 with your profile');
    } else {
      console.log('✓ Chrome started on :9222 (fresh profile - no existing profile found)');
    }
  } else {
    console.log('✓ Chrome started on :9222 with fresh profile');
  }

  try {
    await puppeteer.launch({
      executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
      args,
      defaultViewport: null
    });
  } catch (error) {
    if (error.message.includes('executablePath')) {
      console.log('Trying alternative Chrome path...');
      await puppeteer.launch({
        args,
        defaultViewport: null
      });
    } else {
      throw error;
    }
  }
}

startChrome().catch(console.error);
