#!/usr/bin/env node
/**
 * Token Usage Tracker - Main Entry Point (Node.js Wrapper)
 * 
 * This is a convenient CLI wrapper around the Python backend.
 * It provides a unified interface for:
 *   - Fetching token usage data from configured platforms
 *   - Viewing balance summaries
 *   - Launching the web configuration interface
 * 
 * Usage:
 *   node index.js              # Fetch and display all balances
 *   node index.js fetch        # Same as above
 *   node index.js web          # Launch web configuration UI
 *   node index.js report       # Generate report
 *   node index.js help         # Show this help
 */

const { execSync, spawn } = require('child_process');
const path = require('path');
const fs = require('fs');

const SCRIPTS_DIR = path.join(__dirname, 'scripts');
const PYTHON = process.platform === 'win32' ? 'python' : 'python3';

function runPython(script, args = []) {
  const scriptPath = path.join(SCRIPTS_DIR, script);
  if (!fs.existsSync(scriptPath)) {
    console.error(`Script not found: ${scriptPath}`);
    process.exit(1);
  }
  try {
    const result = execSync(
      `"${PYTHON}" "${scriptPath}" ${args.join(' ')}`,
      { cwd: __dirname, stdio: 'inherit' }
    );
    return result;
  } catch (err) {
    process.exit(err.status);
  }
}

function showHelp() {
  console.log(`
Token Usage Tracker - AI Platform Balance Monitor

Usage:
  node index.js              Fetch and display all balances
  node index.js fetch        Fetch balances for all configured platforms
  node index.js web          Launch web configuration interface
  node index.js report       Generate daily report
  node index.js help         Show this help

Web Interface:
  Once started, open http://localhost:8888 in your browser.
  `);
}

const command = process.argv[2] || 'fetch';

switch (command) {
  case 'fetch':
  case 'start':
    runPython('run.py', process.argv.slice(3));
    break;
  case 'web':
  case 'config':
    console.log('Starting web configuration interface...');
    console.log('Open http://localhost:8888 in your browser\n');
    runPython('../config/web_config.py', process.argv.slice(3));
    break;
  case 'report':
    runPython('run.py', ['--lang', 'both', ...process.argv.slice(3)]);
    break;
  case 'help':
  case '--help':
  case '-h':
    showHelp();
    break;
  default:
    console.error(`Unknown command: ${command}\n`);
    showHelp();
    process.exit(1);
}
