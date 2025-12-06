import { test, expect } from '@playwright/test';

test.describe('Login Page', () => {

  test('Login page loads correctly', async ({ page }) => {
    await page.goto('http://localhost:8000/login/');
    await expect(page).toHaveTitle(/Login - NestMate CUET/);
    await expect(page.locator('h3')).toHaveText('Login');
  });

  test('Successful login redirects user to dashboard', async ({ page }) => {
    await page.goto('http://localhost:8000/login/');
    
    // Fill login with a valid user (change to actual username/password)
    await page.locator('input[name="username"]').fill('student1');
    await page.locator('input[name="password"]').fill('student123');
    await page.getByRole('button', { name: 'Login' }).click();

    // Wait for redirect to student dashboard
    await page.waitForNavigation({ waitUntil: 'networkidle', timeout: 60000 });
    await expect(page).toHaveURL('http://localhost:8000/student_dashboard/');
  });

  test('Invalid login shows error message', async ({ page }) => {
    await page.goto('http://localhost:8000/login/');
    await page.locator('input[name="username"]').fill('wronguser');
    await page.locator('input[name="password"]').fill('wrongpass');
    await page.getByRole('button', { name: 'Login' }).click();

    // Match your actual error message from Django
    await expect(page.locator('.alert')).toContainText('Invalid username or password');
  });

});
