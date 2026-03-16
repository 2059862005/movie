import { test, expect } from '@playwright/test'

test.describe('Movie Website', () => {
  test('homepage loads successfully', async ({ page }) => {
    await page.goto('/')
    
    // Check that the page title contains MovieHub
    await expect(page.locator('text=MovieHub')).toBeVisible()
    
    // Check that search input exists
    await expect(page.locator('input[placeholder*="搜索"]')).toBeVisible()
    
    // Check that footer exists
    await expect(page.locator('text=发现精彩电影')).toBeVisible()
  })

  test('navigation works', async ({ page }) => {
    await page.goto('/')
    
    // Click on navigation link
    await page.click('text=电影')
    
    // Should navigate to category page
    await expect(page.url()).toContain('/category/')
  })

  test('search input works', async ({ page }) => {
    await page.goto('/')
    
    // Type in search input
    await page.fill('input[placeholder*="搜索"]', 'test')
    await page.press('input[placeholder*="搜索"]', 'Enter')
    
    // Should navigate to search page
    await expect(page.url()).toContain('/search')
  })

  test('responsive layout', async ({ page }) => {
    // Test mobile viewport
    await page.setViewportSize({ width: 375, height: 667 })
    await page.goto('/')
    
    // Page should still load correctly
    await expect(page.locator('text=MovieHub')).toBeVisible()
  })
})
