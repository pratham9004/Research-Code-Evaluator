const { test } = require('@playwright/test');
const { runBatch } = require('../helpers/research-batch');

test('Claude_Sonnet_5 + cpp: submit P001 through P050', async ({ page, request, baseURL }) => {
  if (!baseURL) throw new Error('PLAYWRIGHT_BASE_URL must point to the running Research Code Evaluator frontend');
  const onlyProblemId = process.env.E2E_PROBLEM_IDS
    ?.split(',')
    .map((id) => id.trim())
    .filter(Boolean);
  await runBatch({ page, request, baseURL, model: 'Claude_Sonnet_5', language: 'cpp', onlyProblemId });
});
