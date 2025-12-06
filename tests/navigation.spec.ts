import { test, expect } from '@playwright/test';

test.describe('Navigation and Navbar', () => {

  test('Navbar links work correctly', async ({ page }) => {
    await page.goto('http://localhost:8000/');

    // Home
    await page.getByRole('link', { name: 'Home' }).click();
    await expect(page).toHaveURL('http://localhost:8000/');

    // About Us
    await page.getByRole('link', { name: 'About Us' }).click();
    await expect(page).toHaveURL('http://localhost:8000/about/');

    // Contact
    await page.getByRole('link', { name: 'Contact' }).click();
    await expect(page).toHaveURL('http://localhost:8000/contact/');

    // Login
    await page.getByRole('link', { name: 'Login' }).click();
    await expect(page).toHaveURL('http://localhost:8000/login/');

    // Signup
    await page.getByRole('link', { name: 'Sign Up' }).click();
    await expect(page).toHaveURL('http://localhost:8000/signup/');
  });

});
