import os
import json
import time
import streamlit as st
from test_runner import run_test_suite_with_healing

# Set up page configurations
st.set_page_config(
    page_title="AutoQA-Agent Console",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Cyber-Glassmorphism CSS Injection
st.markdown("""
<style>
    /* Dark cyber theme imports */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=JetBrains+Mono:wght@400;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
        background-color: #080b10 !important;
        color: #f9fafb !important;
    }
    
    /* Header styling */
    .title-text {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #00e5ff, #39ff14);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2px;
        letter-spacing: -0.5px;
    }
    
    .subtitle-text {
        font-size: 1.1rem;
        color: #9ca3af;
        margin-bottom: 30px;
        letter-spacing: 0.5px;
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: rgba(13, 17, 26, 0.95) !important;
        border-right: 1px solid rgba(0, 229, 255, 0.1);
    }
    
    /* Card panel styling */
    .glass-card {
        background: linear-gradient(135deg, rgba(13, 17, 26, 0.7), rgba(10, 14, 22, 0.8));
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 24px;
        backdrop-filter: blur(20px);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.4);
        transition: all 0.3s ease;
    }
    
    .glass-card:hover {
        border-color: rgba(0, 229, 255, 0.2);
        box-shadow: 0 12px 40px 0 rgba(0, 229, 255, 0.05);
    }
    
    /* Metric Cards */
    .metric-card {
        background: rgba(255, 255, 255, 0.02);
        border-left: 4px solid #00e5ff;
        padding: 14px 20px;
        border-radius: 8px;
        margin-bottom: 15px;
        border: 1px solid rgba(255, 255, 255, 0.03);
        border-left-width: 4px;
    }
    
    .metric-value {
        font-family: 'JetBrains Mono', monospace;
        font-size: 1.5rem;
        font-weight: 700;
    }
    
    /* Scrollable Code block limiting max-height for better UX */
    div.stCodeBlock {
        max-height: 380px !important;
        overflow-y: auto !important;
        border-radius: 8px;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    /* Status pills */
    .status-running {
        color: #00e5ff;
        font-weight: bold;
        text-shadow: 0 0 10px rgba(0, 229, 255, 0.3);
    }
    
    .status-healing {
        color: #ffc107;
        font-weight: bold;
        text-shadow: 0 0 10px rgba(255, 193, 7, 0.3);
    }
    
    .status-success {
        color: #39ff14;
        font-weight: bold;
        text-shadow: 0 0 10px rgba(57, 255, 20, 0.3);
    }
    
    .status-failed {
        color: #ff5722;
        font-weight: bold;
        text-shadow: 0 0 10px rgba(255, 87, 34, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# Application Sidebar
with st.sidebar:
    st.markdown("<h2 style='color:#00e5ff; font-weight:800;'>⚙️ Settings</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Path configuration
    default_test_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "tests", "test_sample_login.py"))
    test_script_path = st.text_input(
        "Target Pytest-Playwright Script Path", 
        value=default_test_path,
        help="Absolute path to the Playwright testing python script."
    )
    
    # API key setup
    st.markdown("### Authentication")
    anthropic_key_check = os.getenv("ANTHROPIC_API_KEY", "")
    if anthropic_key_check:
        st.success("✅ Anthropic API Key detected in .env")
        api_key_override = anthropic_key_check
    else:
        api_key_override = st.text_input("Enter Anthropic API Key Override", type="password")
        if api_key_override:
            os.environ["ANTHROPIC_API_KEY"] = api_key_override

    st.markdown("---")
    st.markdown("<div style='font-size:0.85rem; color:#6b7280;'>AutoQA-Agent v1.0.0<br/>Powered by Playwright & Claude 3.5</div>", unsafe_allow_html=True)

# Main Workspace Layout
st.markdown("<h1 class='title-text'>⚡ AutoQA-Agent</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle-text'>Autonomous AI-Powered Test Generator & Self-Healing QA Suite</p>", unsafe_allow_html=True)

# Metrics overview row
m_col1, m_col2, m_col3 = st.columns(3)
with m_col1:
    st.markdown("""
    <div class="metric-card" style="border-left-color: #00e5ff;">
        <span style="font-size: 0.85rem; color: #9ca3af; text-transform: uppercase;">Active Engine</span><br/>
        <span class="metric-value" style="color: #00e5ff;">Claude-3.5</span>
    </div>
    """, unsafe_allow_html=True)
with m_col2:
    st.markdown("""
    <div class="metric-card" style="border-left-color: #39ff14;">
        <span style="font-size: 0.85rem; color: #9ca3af; text-transform: uppercase;">Pytest Sandbox</span><br/>
        <span class="metric-value" style="color: #39ff14;">Healthy</span>
    </div>
    """, unsafe_allow_html=True)
with m_col3:
    st.markdown("""
    <div class="metric-card" style="border-left-color: #ffc107;">
        <span style="font-size: 0.85rem; color: #9ca3af; text-transform: uppercase;">Self-Healing</span><br/>
        <span class="metric-value" style="color: #ffc107;">Active</span>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br/>", unsafe_allow_html=True)

# Define columns
col1, col2 = st.columns([3, 2], gap="large")

with col1:
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.subheader("🛠️ Testing Automation Core")
    st.write("Trigger the test run. The agent will execute Playwright, find failing selectors, heal them using generative AI, and verify the patch automatically.")
    
    run_btn = st.button("🚀 Start Test Execution", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Logs dashboard area
    log_container = st.empty()
    diff_container = st.empty()

    if run_btn:
        if not os.path.exists(test_script_path):
            st.error(f"Target test script file not found at: {test_script_path}")
        else:
            # Clear previous visual states
            log_container.info("Starting up subprocess execution...")
            diff_container.empty()
            
            # Execute runner
            with st.spinner("Processing test steps..."):
                result = run_test_suite_with_healing(test_script_path)
            
            # Render final state
            log_file_path = os.path.join(os.path.dirname(__file__), "sandbox", "test_run_log.json")
            if os.path.exists(log_file_path):
                with open(log_file_path, "r", encoding="utf-8") as f:
                    log_data = json.load(f)
                
                status = log_data.get("status", "UNKNOWN")
                msg = log_data.get("message", "")
                diff = log_data.get("diff", {})
                
                # Format visual status
                status_color = "status-success"
                if status == "RUNNING":
                    status_color = "status-running"
                elif status == "HEALING":
                    status_color = "status-healing"
                elif status == "FAILED":
                    status_color = "status-failed"
                
                log_container.markdown(f"""
                <div class="glass-card">
                    <h3>Execution Status: <span class="{status_color}">{status}</span></h3>
                    <p style="font-size:1.1rem; color:#e5e7eb;">{msg}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Render diff if healing took place
                if diff:
                    with diff_container:
                        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
                        st.markdown("<h3 style='color:#39ff14;'>✨ Healing Applied Successfully</h3>", unsafe_allow_html=True)
                        
                        d_col1, d_col2 = st.columns(2)
                        with d_col1:
                            st.markdown(f"**Original Locator (Failed)**<br/><code style='background-color:#ffebee; color:#d32f2f; padding:5px; border-radius:4px; display:block;'>{diff.get('old_selector')}</code>", unsafe_allow_html=True)
                        with d_col2:
                            st.markdown(f"**AI Healed Locator (Success)**<br/><code style='background-color:#e8f5e9; color:#2e7d32; padding:5px; border-radius:4px; display:block;'>{diff.get('new_selector')}</code>", unsafe_allow_html=True)
                        
                        st.markdown(f"**Reasoning / Insights**<br/><div style='font-style:italic; color:#9ca3af;'>{diff.get('explanation')}</div>", unsafe_allow_html=True)
                        st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.error("No telemetry log file was found in sandbox workspace.")

with col2:
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.subheader("📸 Failure Analysis (Visual Snapshot)")
    st.write("Displays the layout screenshot captured by Playwright at the exact millisecond of timeout error:")
    
    screenshot_file = os.path.join(os.path.dirname(__file__), "sandbox", "failure_snapshot.png")
    if os.path.exists(screenshot_file):
        st.image(screenshot_file, caption="DOM Failure Snapshot", use_container_width=True)
    else:
        st.info("No failure screenshot available. Run the test to populate visual states.")
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Display script content live to see patch diff
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.subheader("📄 Automated Test Code Viewer")
    if os.path.exists(test_script_path):
        with open(test_script_path, "r", encoding="utf-8") as f:
            code_text = f.read()
        st.code(code_text, language="python")
    else:
        st.write("Select a valid file path in settings to view code.")
    st.markdown("</div>", unsafe_allow_html=True)
