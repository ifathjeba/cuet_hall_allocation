import { test, expect } from '@playwright/test';

test.describe('Signup Page', () => {

  test('Signup page loads correctly', async ({ page }) => {
    await page.goto('http://localhost:8000/signup/');
    await expect(page.locator('h2')).toHaveText('Sign Up');
    await expect(page.locator('input[name="username"]')).toBeVisible();
  });

  test('Successful signup redirects to dashboard', async ({ page }) => {
    await page.goto('http://localhost:8000/signup/');

    // Use random username to avoid duplicates
    const randomUser = 'student' + Math.floor(Math.random() * 10000);
    
    await page.locator('input[name="username"]').fill(randomUser);
    await page.locator('input[name="email"]').fill(randomUser + '@example.com');
    await page.locator('input[name="password1"]').fill('student123');
    await page.locator('input[name="password2"]').fill('student123');
    await page.locator('select[name="user_type"]').selectOption('student');

    await page.getByRole('button', { name: 'Sign Up' }).click();

    // Wait for redirect to student dashboard
    await page.waitForNavigation({ waitUntil: 'networkidle', timeout: 60000 });
    await expect(page).toHaveURL('http://localhost:8000/student_dashboard/');
  });

});
