import streamlit as st
import os
import sys
from datetime import datetime
import time
from dotenv import load_dotenv
import threading
import queue

# Load environment variables
load_dotenv()

# Import your CrewAI components
try:
    from agents import reporter1, reporter2, analyst
    from tasks import report_task1, report_task2, summary_task
    from crewai import Crew
except ImportError as e:
    st.error(f"Error importing CrewAI components: {e}")
    st.stop()

# Page configuration
st.set_page_config(
    page_title="AI News Reporter",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .status-running {
        color: #ff6b6b;
        font-weight: bold;
    }
    .status-complete {
        color: #51cf66;
        font-weight: bold;
    }
    .news-section {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        border-left: 4px solid #1f77b4;
    }
    .agent-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

def check_api_keys():
    """Check if required API keys are present"""
    missing_keys = []
    
    if not os.getenv("NEWSAPI_KEY"):
        missing_keys.append("NEWSAPI_KEY")
    if not os.getenv("OPENAI_API_KEY"):
        missing_keys.append("OPENAI_API_KEY")
    
    return missing_keys

def run_crew_in_thread(crew, result_queue):
    """Run CrewAI crew in a separate thread"""
    try:
        result = crew.kickoff()
        result_queue.put(("success", result))
    except Exception as e:
        result_queue.put(("error", str(e)))

def main():
    # Header
    st.markdown('<h1 class="main-header">🤖 AI News Reporter</h1>', unsafe_allow_html=True)
    st.markdown("### Powered by CrewAI - Fetching Political & Tech News in Parallel")
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # API Key Status
        st.subheader("🔑 API Keys Status")
        missing_keys = check_api_keys()
        
        if missing_keys:
            st.error(f"Missing API Keys: {', '.join(missing_keys)}")
            st.info("Please set up your .env file with the required API keys:")
            st.code("""
NEWSAPI_KEY=your_newsapi_key_here
OPENAI_API_KEY=your_openai_api_key_here
            """)
        else:
            st.success("All API keys configured ✅")
        
        # News Categories
        st.subheader("📰 News Categories")
        
        col1, col2 = st.columns(2)
        with col1:
            politics_enabled = st.checkbox("🏛️ Indian Politics", value=True)
        with col2:
            tech_enabled = st.checkbox("💻 Global Tech", value=True)
        
        # Advanced Settings
        with st.expander("🔧 Advanced Settings"):
            verbose_mode = st.checkbox("Verbose Logging", value=True, 
                                     help="Show detailed agent reasoning")
            max_headlines = st.slider("Headlines per category", 1, 5, 3)
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Control Panel
        st.header("🎛️ Control Panel")
        
        if missing_keys:
            st.warning("Please configure API keys in the sidebar before proceeding.")
            run_button = st.button("🚀 Fetch News", disabled=True)
        else:
            run_button = st.button("🚀 Fetch News", type="primary")
        
        # Progress and Status Area
        if 'crew_running' not in st.session_state:
            st.session_state.crew_running = False
        
        if 'last_result' not in st.session_state:
            st.session_state.last_result = None
            
        if 'last_run_time' not in st.session_state:
            st.session_state.last_run_time = None
    
    with col2:
        # Agent Status Panel
        st.header("🤖 Agent Status")
        
        agents_info = [
            {"name": "Politics Reporter", "icon": "🏛️", "status": "Ready"},
            {"name": "Tech Reporter", "icon": "💻", "status": "Ready"}, 
            {"name": "Summary Analyst", "icon": "📊", "status": "Ready"}
        ]
        
        for agent in agents_info:
            status_class = "status-complete" if not st.session_state.crew_running else "status-running"
            current_status = "Running..." if st.session_state.crew_running else agent["status"]
            
            st.markdown(f"""
            <div class="agent-card">
                <strong>{agent['icon']} {agent['name']}</strong><br>
                <span class="{status_class}">Status: {current_status}</span>
            </div>
            """, unsafe_allow_html=True)
    
    # Handle news fetching
    if run_button and not st.session_state.crew_running:
        st.session_state.crew_running = True
        st.session_state.last_result = None
        
        # Create progress indicators
        progress_container = st.container()
        
        with progress_container:
            st.info("🔄 Initializing AI agents...")
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Create and configure crew
            try:
                crew = Crew(
                    agents=[reporter1, reporter2, analyst],
                    tasks=[report_task1, report_task2, summary_task],
                    verbose=verbose_mode,
                    process="sequential"
                )
                
                progress_bar.progress(25)
                status_text.text("🏛️ Politics reporter fetching Indian news...")
                
                # Run crew in background thread
                result_queue = queue.Queue()
                crew_thread = threading.Thread(target=run_crew_in_thread, args=(crew, result_queue))
                crew_thread.start()
                
                # Monitor progress
                progress = 25
                while crew_thread.is_alive():
                    time.sleep(1)
                    progress = min(progress + 5, 90)
                    progress_bar.progress(progress)
                    
                    if progress < 60:
                        status_text.text("🏛️ Politics reporter working...")
                    elif progress < 80:
                        status_text.text("💻 Tech reporter gathering global news...")
                    else:
                        status_text.text("📊 Analyst creating summary...")
                
                crew_thread.join()
                
                # Get result
                result_type, result_data = result_queue.get()
                
                progress_bar.progress(100)
                status_text.text("✅ News collection completed!")
                
                if result_type == "success":
                    st.session_state.last_result = result_data
                    st.session_state.last_run_time = datetime.now()
                    st.success("🎉 News successfully fetched and analyzed!")
                else:
                    st.error(f"❌ Error occurred: {result_data}")
                
            except Exception as e:
                st.error(f"❌ Failed to initialize crew: {str(e)}")
            
            finally:
                st.session_state.crew_running = False
                time.sleep(2)  # Brief pause before clearing progress
                progress_container.empty()
    
    # Display Results
    if st.session_state.last_result:
        st.header("📋 Latest News Report")
        
        # Show timestamp
        if st.session_state.last_run_time:
            st.caption(f"Last updated: {st.session_state.last_run_time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Display the news summary
        st.markdown('<div class="news-section">', unsafe_allow_html=True)
        st.markdown(st.session_state.last_result)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Download option
        st.download_button(
            label="📄 Download Report",
            data=str(st.session_state.last_result),
            file_name=f"news_report_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
            mime="text/plain"
        )
    
    # Footer
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("🏛️ Political News", "India Focus")
    with col2:
        st.metric("💻 Tech News", "Global Coverage") 
    with col3:
        if st.session_state.last_run_time:
            time_diff = datetime.now() - st.session_state.last_run_time
            minutes_ago = int(time_diff.total_seconds() / 60)
            st.metric("🕐 Last Update", f"{minutes_ago}m ago")
        else:
            st.metric("🕐 Last Update", "Never")
    
    # Help Section
    with st.expander("ℹ️ How to Use"):
        st.markdown("""
        ### Getting Started:
        1. **Set up API Keys**: Add your NewsAPI and OpenAI API keys to a `.env` file
        2. **Configure Settings**: Use the sidebar to adjust news categories and settings
        3. **Fetch News**: Click the "🚀 Fetch News" button to start the AI agents
        4. **View Results**: The summary will appear below with organized news from both categories
        
        ### Features:
        - **Parallel Processing**: Politics and tech news are fetched simultaneously
        - **AI Analysis**: Advanced summarization and key insights extraction
        - **Real-time Status**: Monitor agent progress in real-time
        - **Export Options**: Download reports for offline viewing
        
        ### Agents:
        - **Politics Reporter**: Focuses on Indian political developments
        - **Tech Reporter**: Covers global technology innovations
        - **Summary Analyst**: Creates comprehensive analysis and insights
        """)

if __name__ == "__main__":
    main()