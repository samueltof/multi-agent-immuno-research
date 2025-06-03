import streamlit as st
import requests
import json
import time
from typing import Dict, List, Any, Optional
import sseclient
from urllib.parse import urljoin

# Page configuration
st.set_page_config(
    page_title="LangManus - Multiagent System",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for modern, aesthetic design
st.markdown("""
<style>
    /* Main container styling */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Custom chat message styling */
    .chat-message {
        padding: 1rem;
        border-radius: 12px;
        margin-bottom: 1rem;
        border: 1px solid #e0e0e0;
        background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        margin-left: 2rem;
    }
    
    .assistant-message {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        margin-right: 2rem;
    }
    
    .system-message {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        color: white;
        font-size: 0.9rem;
        opacity: 0.9;
    }
    
    /* Header styling */
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 12px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 16px rgba(0,0,0,0.1);
    }
    
    /* Sidebar styling */
    .sidebar .sidebar-content {
        background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
    }
    
    /* Configuration section styling */
    .config-section {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        border-left: 4px solid #667eea;
    }
    
    /* Status indicators */
    .status-indicator {
        display: inline-block;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        margin-right: 8px;
    }
    
    .status-connected {
        background-color: #28a745;
    }
    
    .status-disconnected {
        background-color: #dc3545;
    }
    
    .status-processing {
        background-color: #ffc107;
        animation: pulse 1.5s infinite;
    }
    
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.5; }
        100% { opacity: 1; }
    }
    
    /* Agent status styling */
    .agent-status {
        padding: 0.5rem 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border-left: 4px solid;
        font-weight: 500;
    }
    
    .agent-processing {
        background: #fff3cd;
        border-left-color: #ffc107;
        color: #856404;
    }
    
    .agent-completed {
        background: #d4edda;
        border-left-color: #28a745;
        color: #155724;
    }
    
    .agent-error {
        background: #f8d7da;
        border-left-color: #dc3545;
        color: #721c24;
    }
    
    /* Streaming indicator */
    .streaming-indicator {
        display: inline-flex;
        align-items: center;
        padding: 0.25rem 0.5rem;
        background: #e3f2fd;
        border-radius: 12px;
        font-size: 0.8rem;
        color: #1976d2;
        margin-left: 0.5rem;
    }
    
    .streaming-dot {
        width: 6px;
        height: 6px;
        background: #1976d2;
        border-radius: 50%;
        margin-right: 0.5rem;
        animation: pulse 1.5s infinite;
    }
    
    /* Event log improvements */
    .event-log {
        background: #f8f9fa;
        border: 1px solid #dee2e6;
        border-radius: 8px;
        padding: 1rem;
        font-family: 'Courier New', monospace;
        font-size: 0.75rem;
        max-height: 400px;
        overflow-y: auto;
        line-height: 1.4;
    }
    
    .event-log::-webkit-scrollbar {
        width: 6px;
    }
    
    .event-log::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 3px;
    }
    
    .event-log::-webkit-scrollbar-thumb {
        background: #c1c1c1;
        border-radius: 3px;
    }
    
    .event-log::-webkit-scrollbar-thumb:hover {
        background: #a8a8a8;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "api_url" not in st.session_state:
    st.session_state.api_url = "http://localhost:8000"
if "conversation_id" not in st.session_state:
    st.session_state.conversation_id = 0
if "event_log" not in st.session_state:
    st.session_state.event_log = []

def display_header():
    """Display the main header"""
    st.markdown("""
    <div class="main-header">
        <h1>🤖 LangManus</h1>
        <p>Advanced Multiagent System with LangGraph</p>
    </div>
    """, unsafe_allow_html=True)

def display_message(message: Dict[str, str], is_user: bool = False):
    """Display a chat message with modern styling"""
    role = message.get("role", "assistant")
    content = message.get("content", "")
    
    if role == "user":
        message_class = "user-message"
        icon = "👤"
    elif role == "system":
        message_class = "system-message"
        icon = "⚙️"
    else:
        message_class = "assistant-message"
        icon = "🤖"
    
    st.markdown(f"""
    <div class="chat-message {message_class}">
        <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
            <span style="font-size: 1.2rem; margin-right: 0.5rem;">{icon}</span>
            <strong>{role.title()}</strong>
        </div>
        <div>{content}</div>
    </div>
    """, unsafe_allow_html=True)

def get_server_status(api_url: str) -> bool:
    """Check if the API server is running"""
    try:
        response = requests.get(f"{api_url}/docs", timeout=5)
        return response.status_code == 200
    except:
        return False

def stream_chat_response(api_url: str, messages: List[Dict], config: Dict) -> None:
    """Stream chat response from the API"""
    payload = {
        "messages": messages,
        "debug": config.get("debug", False),
        "deep_thinking_mode": config.get("deep_thinking_mode", False),
        "search_before_planning": config.get("search_before_planning", False)
    }
    
    try:
        url = urljoin(api_url, "/api/chat/stream")
        headers = {
            "Content-Type": "application/json",
            "Accept": "text/event-stream"
        }
        
        response = requests.post(
            url,
            json=payload,
            headers=headers,
            stream=True,
            timeout=60
        )
        
        if response.status_code != 200:
            st.error(f"API Error: {response.status_code} - {response.text}")
            return
        
        # Create a placeholder for the streaming response
        response_container = st.empty()
        current_response = ""
        
        # Create event log container
        event_container = st.expander("📊 Event Log", expanded=False)
        
        # Create agent status container
        agent_status_container = st.empty()
        current_agent = ""
        
        # Process SSE stream
        client = sseclient.SSEClient(response)
        
        for event in client.events():
            if event.event and event.data:
                try:
                    event_data = json.loads(event.data)
                    
                    # Log the event
                    st.session_state.event_log.append({
                        "timestamp": time.strftime("%H:%M:%S"),
                        "event": event.event,
                        "data": event_data
                    })
                    
                    # Update event log display
                    with event_container:
                        event_log_text = ""
                        for log_entry in st.session_state.event_log[-20:]:  # Show last 20 events
                            event_log_text += f"[{log_entry['timestamp']}] {log_entry['event']}: {str(log_entry['data'])[:150]}...\n"
                        
                        st.code(event_log_text, language="text")
                    
                    # Handle different event types
                    if event.event == "message":
                        # Handle delta content from streaming
                        if "delta" in event_data and "content" in event_data["delta"]:
                            delta_content = event_data["delta"]["content"]
                            current_response += delta_content
                            
                            # Update the display with current response
                            with response_container:
                                display_message({"role": "assistant", "content": current_response})
                    
                    elif event.event == "end_of_llm":
                        # Agent finished generating response
                        if "agent_name" in event_data:
                            agent_name = event_data["agent_name"]
                            with agent_status_container:
                                st.markdown(f"""
                                <div class="agent-status agent-completed">
                                    🤖 Agent '<strong>{agent_name}</strong>' completed response generation
                                </div>
                                """, unsafe_allow_html=True)
                    
                    elif event.event == "end_of_agent":
                        # Agent workflow completed
                        if "agent_name" in event_data:
                            agent_name = event_data["agent_name"]
                            with agent_status_container:
                                st.markdown(f"""
                                <div class="agent-status agent-completed">
                                    ✅ Agent '<strong>{agent_name}</strong>' workflow completed
                                </div>
                                """, unsafe_allow_html=True)
                    
                    elif event.event == "start_of_agent":
                        # Agent started processing
                        if "agent_name" in event_data:
                            agent_name = event_data["agent_name"]
                            current_agent = agent_name
                            with agent_status_container:
                                st.markdown(f"""
                                <div class="agent-status agent-processing">
                                    <span class="streaming-dot"></span>
                                    🔄 Agent '<strong>{agent_name}</strong>' started processing...
                                </div>
                                """, unsafe_allow_html=True)
                    
                    elif event.event == "error":
                        st.error(f"Workflow Error: {event_data}")
                        break
                        
                except json.JSONDecodeError as e:
                    st.warning(f"Failed to parse event data: {e}")
                    continue
                except Exception as e:
                    st.warning(f"Error processing event: {e}")
                    continue
        
        # Clear agent status when done
        agent_status_container.empty()
        
        # Add the final response to message history
        if current_response.strip():
            st.session_state.messages.append({
                "role": "assistant",
                "content": current_response.strip()
            })
            
            # Show completion message
            st.success("✅ Response completed!")
    
    except requests.exceptions.Timeout:
        st.error("Request timed out. Please try again.")
    except requests.exceptions.ConnectionError:
        st.error("Could not connect to the API server. Please check if the server is running.")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.exception(e)  # For debugging

def main():
    """Main application function"""
    display_header()
    
    # Sidebar configuration
    with st.sidebar:
        st.markdown("## ⚙️ Configuration")
        
        # API Configuration
        st.markdown('<div class="config-section">', unsafe_allow_html=True)
        st.markdown("### 🌐 API Settings")
        api_url = st.text_input(
            "API URL",
            value=st.session_state.api_url,
            help="The URL of your LangManus API server"
        )
        st.session_state.api_url = api_url
        
        # Server status indicator
        server_status = get_server_status(api_url)
        status_class = "status-connected" if server_status else "status-disconnected"
        status_text = "Connected" if server_status else "Disconnected"
        
        st.markdown(f"""
        <div style="margin-top: 0.5rem;">
            <span class="status-indicator {status_class}"></span>
            <span>{status_text}</span>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Agent Configuration
        st.markdown('<div class="config-section">', unsafe_allow_html=True)
        st.markdown("### 🧠 Agent Settings")
        
        debug_mode = st.checkbox(
            "Debug Mode",
            value=False,
            help="Enable debug logging for detailed workflow information"
        )
        
        deep_thinking_mode = st.checkbox(
            "Deep Thinking Mode",
            value=False,
            help="Enable deep reasoning and analysis capabilities"
        )
        
        search_before_planning = st.checkbox(
            "Search Before Planning",
            value=False,
            help="Perform web search before creating execution plans"
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Conversation Management
        st.markdown('<div class="config-section">', unsafe_allow_html=True)
        st.markdown("### 💬 Conversation")
        
        if st.button("🗑️ Clear Conversation", use_container_width=True):
            st.session_state.messages = []
            st.session_state.event_log = []
            st.session_state.conversation_id += 1
            st.rerun()
        
        st.markdown(f"Messages: {len(st.session_state.messages)}")
        st.markdown(f"Conversation ID: {st.session_state.conversation_id}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Main chat interface
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown("## 💬 Chat Interface")
        
        # Display conversation history
        if st.session_state.messages:
            st.markdown("### Conversation History")
            for message in st.session_state.messages:
                display_message(message)
        else:
            st.markdown("""
            <div style="text-align: center; padding: 2rem; color: #6c757d;">
                <h3>👋 Welcome to LangManus!</h3>
                <p>Start a conversation with the multiagent system by typing your message below.</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Chat input
        with st.form("chat_form", clear_on_submit=True):
            user_input = st.text_area(
                "Your message:",
                height=100,
                placeholder="Type your message here... (e.g., 'Help me analyze this data', 'Create a plan for...', etc.)"
            )
            
            col_submit, col_example = st.columns([1, 2])
            
            with col_submit:
                submit_button = st.form_submit_button("Send 🚀", use_container_width=True)
            
            with col_example:
                if st.form_submit_button("💡 Example Query", use_container_width=True):
                    user_input = "Help me create a comprehensive project plan for developing a mobile app. Include research, design, development, and testing phases."
                    submit_button = True
        
        # Process user input
        if submit_button and user_input.strip():
            if not server_status:
                st.error("⚠️ API server is not available. Please check the server status.")
                return
            
            # Add user message to history
            user_message = {"role": "user", "content": user_input.strip()}
            st.session_state.messages.append(user_message)
            
            # Display user message
            display_message(user_message)
            
            # Configuration for API call
            config = {
                "debug": debug_mode,
                "deep_thinking_mode": deep_thinking_mode,
                "search_before_planning": search_before_planning
            }
            
            # Stream response
            with st.spinner("🤖 Processing your request..."):
                stream_chat_response(
                    st.session_state.api_url,
                    st.session_state.messages,
                    config
                )
    
    with col2:
        st.markdown("## 📊 System Status")
        
        # Current configuration display
        st.markdown("### Current Settings")
        config_info = f"""
        **Debug Mode:** {'✅' if debug_mode else '❌'}
        **Deep Thinking:** {'✅' if deep_thinking_mode else '❌'}
        **Search Planning:** {'✅' if search_before_planning else '❌'}
        """
        st.markdown(config_info)
        
        # Performance metrics (placeholder)
        st.markdown("### Performance")
        st.metric("Total Messages", len(st.session_state.messages))
        st.metric("Events Logged", len(st.session_state.event_log))
        
        # Quick actions
        st.markdown("### Quick Actions")
        
        if st.button("🔄 Refresh Status", use_container_width=True):
            st.rerun()
        
        if st.button("📥 Export Chat", use_container_width=True):
            if st.session_state.messages:
                chat_export = json.dumps(st.session_state.messages, indent=2)
                st.download_button(
                    "💾 Download JSON",
                    chat_export,
                    file_name=f"langmanus_chat_{int(time.time())}.json",
                    mime="application/json",
                    use_container_width=True
                )
            else:
                st.info("No messages to export")

if __name__ == "__main__":
    main()