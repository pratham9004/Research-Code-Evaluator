const { test } = require('@playwright/test');
const { runBatch } = require('../helpers/research-batch');

test('Perplexity + java: submit P001 through P050', async ({ page, request, baseURL }) => {
  if (!baseURL) throw new Error('PLAYWRIGHT_BASE_URL must point to the running Research Code Evaluator frontend');
  await runBatch({
    page,
    request,
    baseURL,
    model: 'Perplexity',
    language: 'java',
    onlyProblemId: process.env.E2E_PROBLEM_ID,
    submissionModelName: process.env.E2E_SUBMISSION_MODEL_NAME,
  });
});
