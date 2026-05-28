import asyncio
from playwright.async_api import async_playwright
import os

async def test_wos_parser():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        try:
            # Navigate to the page
            await page.goto('http://localhost:8080/wos-parser-enhanced.html')
            print("Page loaded successfully!")

            # Take screenshot
            await page.screenshot(path='screenshot_initial.png')
            print("Initial screenshot saved")

            # Check if help button works
            help_btn = page.locator('#helpBtn')
            if await help_btn.count() > 0:
                await help_btn.click()
                await page.wait_for_selector('#helpModal.show', timeout=5000)
                print("Help modal opened!")
                await page.screenshot(path='screenshot_help.png')

                # Close modal
                await page.locator('#closeModal').click()
                await page.wait_for_selector('#helpModal', state='hidden', timeout=5000)
                print("Help modal closed!")

            # Check config status
            config_status = await page.locator('#configStatus').text_content()
            print(f"Config status: {config_status}")

            # Upload test file
            test_file = os.path.abspath('data/wos/savedrecs.txt')
            if os.path.exists(test_file):
                file_input = page.locator('#fileInput')
                await file_input.set_input_files(test_file)
                print(f"Uploaded test file: {test_file}")

                # Check file list
                await page.wait_for_selector('.file-item', timeout=5000)
                file_name = await page.locator('.file-name').first.text_content()
                print(f"File listed: {file_name}")

                # Click parse button
                parse_btn = page.locator('#parseBtn')
                await parse_btn.click()
                print("Parse button clicked!")

                # Wait for results
                await page.wait_for_selector('#resultCard:not(.hidden)', timeout=30000)
                print("Results displayed!")

                # Take screenshot of results
                await page.screenshot(path='screenshot_results.png', full_page=True)
                print("Results screenshot saved!")

                # Check stats
                stats = await page.locator('.stat-number').all_text_contents()
                print(f"Stats: {stats}")

                # Test pagination
                page_size_select = page.locator('#pageSize')
                await page_size_select.select_option('25')
                print("Set page size to 25")

                # Test filter
                author_filter = page.locator('[data-filter="Author"]')
                await author_filter.fill('Tang')
                await page.wait_for_timeout(500)
                print("Filtered by Author: Tang")
                await page.screenshot(path='screenshot_filtered.png')

            else:
                print(f"Test file not found: {test_file}")

            # Keep browser open for a moment
            await page.wait_for_timeout(3000)

        except Exception as e:
            print(f"Error: {e}")
            await page.screenshot(path='screenshot_error.png')
        finally:
            await browser.close()

if __name__ == '__main__':
    asyncio.run(test_wos_parser())
