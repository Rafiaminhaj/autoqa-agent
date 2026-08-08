import asyncio
from mcp.server.fastmcp import FastMCP
from playwright.async_api import async_playwright

# Create FastMCP server instance
mcp = FastMCP("AutoQA-Browser-Server")

# Global variables to persist browser state across tool calls
playwright_instance = None
browser_instance = None
current_page = None

async def init_browser():
    """Helper to guarantee browser and page are initialized."""
    global playwright_instance, browser_instance, current_page
    if playwright_instance is None:
        playwright_instance = await async_playwright().start()
        # Launching in headless mode for server/CLI usage, but can be configured
        browser_instance = await playwright_instance.chromium.launch(headless=True)
        current_page = await browser_instance.new_page()

@mcp.tool()
async def open_url(url: str) -> str:
    """Navigate the automated browser to the specified URL."""
    global current_page
    await init_browser()
    try:
        await current_page.goto(url, wait_until="networkidle", timeout=15000)
        title = await current_page.title()
        return f"Successfully navigated to: {url} | Page Title: '{title}'"
    except Exception as e:
        return f"Failed to navigate to {url}. Error: {str(e)}"

@mcp.tool()
async def click_element(selector: str) -> str:
    """Click a button, link, or input element matched by the CSS selector."""
    global current_page
    await init_browser()
    try:
        # Wait briefly for element presence
        await current_page.wait_for_selector(selector, state="visible", timeout=5000)
        await current_page.click(selector)
        return f"Successfully clicked selector: '{selector}'"
    except Exception as e:
        return f"Error clicking '{selector}': {str(e)}. Selector might have changed."

@mcp.tool()
async def input_text(selector: str, text: str) -> str:
    """Fill an input field or textarea with text using a CSS selector."""
    global current_page
    await init_browser()
    try:
        await current_page.wait_for_selector(selector, state="visible", timeout=5000)
        # Clear field before entering text
        await current_page.fill(selector, "")
        await current_page.type(selector, text)
        return f"Successfully filled '{selector}' with text."
    except Exception as e:
        return f"Error entering text into '{selector}': {str(e)}"

@mcp.tool()
async def capture_page_screenshot(output_path: str) -> str:
    """Take a full-screen screenshot of the current browser tab and save to disk."""
    global current_page
    await init_browser()
    try:
        await current_page.screenshot(path=output_path, full_page=True)
        return f"Page screenshot successfully saved to: {output_path}"
    except Exception as e:
        return f"Failed to capture screenshot. Error: {str(e)}"

@mcp.tool()
async def get_page_html() -> str:
    """Retrieve the raw HTML document source code of the currently loaded page."""
    global current_page
    await init_browser()
    try:
        content = await current_page.content()
        return content
    except Exception as e:
        return f"Failed to retrieve page source. Error: {str(e)}"

@mcp.tool()
async def close_browser_session() -> str:
    """Shut down the browser session and clean up system resources."""
    global playwright_instance, browser_instance, current_page
    if browser_instance:
        await browser_instance.close()
    if playwright_instance:
        await playwright_instance.stop()
    playwright_instance = None
    browser_instance = None
    current_page = None
    return "Browser session closed successfully."

if __name__ == "__main__":
    # Start the FastMCP server on standard I/O (default transport protocol)
    mcp.run()
