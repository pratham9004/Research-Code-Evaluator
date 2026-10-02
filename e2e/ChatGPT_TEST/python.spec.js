const { test } = require('@playwright/test');
const { runBatch } = require('../helpers/research-batch');

test('ChatGPT + python: submit P001 through P050', async ({ page, request, baseURL }) => {
  if (!baseURL) throw new Error('PLAYWRIGHT_BASE_URL must point to the running Research Code Evaluator frontend');
  await runBatch({ page, request, baseURL, model: 'ChatGPT', language: 'python' });
});
