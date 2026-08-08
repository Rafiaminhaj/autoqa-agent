import os
import pytest
from playwright.sync_api import Page, expect

# Create a local HTML page mock inside tests directory representing the Intuit Assist AI Assistant Console
LOCAL_HTML_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "local_assist_page.html"))

@pytest.fixture(autouse=True)
def setup_local_mock_page():
    """Generates the mock target page containing the updated Intuit Assist UI elements."""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Intuit Assist Console</title>
    </head>
    <body style="background-color: #080b10; color: #f9fafb; font-family: sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0;">
        <div style="background: rgba(13, 17, 26, 0.8); padding: 30px; border-radius: 16px; border: 1px solid rgba(255,255,255,0.08); width: 450px; box-shadow: 0 8px 32px 0 rgba(0,0,0,0.5);">
            <div style="display: flex; align-items: center; margin-bottom: 20px;">
                <div style="width: 12px; height: 12px; border-radius: 50%; background: #00e5ff; margin-right: 10px; box-shadow: 0 0 10px #00e5ff;"></div>
                <h2 style="margin: 0; font-size: 1.5rem; color: #00e5ff;">Intuit Assist (AI Beta)</h2>
            </div>
            
            <p style="color: #9ca3af; font-size: 0.9rem; margin-bottom: 20px;">Ask QuickBooks & TurboTax metrics in real-time:</p>
            
            <div style="margin-bottom: 15px;">
                <textarea id="assist-input" style="width: 100%; height: 80px; padding: 10px; border-radius: 8px; border: 1px solid #30364d; background: #161b22; color: #fff; box-sizing: border-box; font-family: sans-serif; resize: none;" placeholder="e.g. Generate my quarterly revenue report..."></textarea>
            </div>
            
            <!-- Button was updated from '#ask-assist-btn-v2' to '#ask-assist-btn-v2' -->
            <button id="ask-assist-btn-v2" style="width: 100%; padding: 12px; background: linear-gradient(135deg, #00e5ff, #39ff14); border: none; border-radius: 8px; color: #080b10; font-weight: bold; cursor: pointer; transition: all 0.3s ease;">
                ✨ Ask Assist
            </button>
            
            <div id="response-box" style="display: none; margin-top: 20px; padding: 15px; border-radius: 8px; background: rgba(57, 255, 20, 0.05); border: 1px solid rgba(57, 255, 20, 0.2); color: #39ff14;">
                <strong>Intuit Assist:</strong><br/>
                <span id="response-text" style="font-size: 0.95rem; display: block; margin-top: 5px;"></span>
            </div>
        </div>
        <script>
            document.getElementById('ask-assist-btn-v2').addEventListener('click', function() {
                var val = document.getElementById('assist-input').value;
                var resBox = document.getElementById('response-box');
                var resText = document.getElementById('response-text');
                
                if (val.trim() === '') {
                    resText.innerText = "Please enter a valid query.";
                } else {
                    resText.innerText = "Real-time cash flow & invoice audit completed successfully for query: '" + val + "'";
                }
                resBox.style.display = 'block';
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

def test_assist_flow(page: Page):
    # Navigate to the generated local mock page
    page.goto(f"file://{LOCAL_HTML_PATH}")
    
    # Type custom financial query
    page.fill("#assist-input", "Generate my quarterly revenue report")
    
    # This button ID is broken (originally '#ask-assist-btn-v2', now '#ask-assist-btn-v2').
    # Playwright will fail to locate it.
    # The AutoQA-Agent will auto-heal '#ask-assist-btn-v2' to '#ask-assist-btn-v2' and pass.
    page.click("#ask-assist-btn-v2")
    
    # Expectation: After successful click, response is visible and contains expected audit statement
    response_box = page.locator("#response-box")
    expect(response_box).to_be_visible()
    
    response_text = page.locator("#response-text")
    expect(response_text).to_contain_text("Real-time cash flow & invoice audit completed successfully")
