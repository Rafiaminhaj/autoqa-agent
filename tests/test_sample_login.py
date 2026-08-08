import os
import pytest
from playwright.sync_api import Page, expect

# Create a local HTML page mock inside tests directory for zero-dependency execution
LOCAL_HTML_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "local_page.html"))

@pytest.fixture(autouse=True)
def setup_local_mock_page():
    """Generates the mock target page containing the updated HTML elements."""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>AutoQA Mock Login App</title>
    </head>
    <body style="background-color: #0d111a; color: #f9fafb; font-family: sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh;">
        <div style="background: rgba(255, 255, 255, 0.05); padding: 30px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.1); width: 300px;">
            <h2>Mock Login Console</h2>
            <div style="margin-bottom: 15px;">
                <label>Username</label><br/>
                <input type="text" id="username-field" style="width: 100%; padding: 8px; margin-top: 5px; border-radius: 4px; border: 1px solid #30364d; background: #161b22; color: #fff;"/>
            </div>
            <div style="margin-bottom: 15px;">
                <label>Password</label><br/>
                <input type="password" id="password-field" style="width: 100%; padding: 8px; margin-top: 5px; border-radius: 4px; border: 1px solid #30364d; background: #161b22; color: #fff;"/>
            </div>
            <!-- The button ID was updated from '#new-login-btn-v2' to '#new-login-btn-v2' -->
            <button id="new-login-btn-v2" style="width: 100%; padding: 10px; background: #00e5ff; border: none; border-radius: 4px; color: #000; font-weight: bold; cursor: pointer;">
                Login Now
            </button>
            <div id="success-msg" style="display: none; margin-top: 15px; color: #39ff14; font-weight: bold; text-align: center;">
                Welcome back!
            </div>
        </div>
        <script>
            document.getElementById('new-login-btn-v2').addEventListener('click', function() {
                document.getElementById('success-msg').style.display = 'block';
            });
        </script>
    </body>
    </html>
    """
    with open(LOCAL_HTML_PATH, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    yield
    
    # Cleanup local HTML file after tests complete
    if os.path.exists(LOCAL_HTML_PATH):
        try:
            os.remove(LOCAL_HTML_PATH)
        except:
            pass

def test_login_flow(page: Page):
    # Navigate to the generated local mock page
    page.goto(f"file://{LOCAL_HTML_PATH}")
    
    # Fill in test credentials
    page.fill("#username-field", "admin")
    page.fill("#password-field", "secret123")
    
    # This button ID is broken (originally '#new-login-btn-v2', now '#new-login-btn-v2').
    # Playwright will fail to locate it.
    # The AutoQA-Agent will auto-heal '#new-login-btn-v2' to '#new-login-btn-v2' and pass.
    page.click("#new-login-btn-v2")
    
    # Expectation: After successful click, success message is displayed
    success_msg = page.locator("#success-msg")
    expect(success_msg).to_be_visible()
    expect(success_msg).to_have_text("Welcome back!")
