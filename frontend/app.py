import streamlit as st
import requests
import json
import time
from typing import Dict, List, Any, Optional
import sseclient
from urllib.parse import urljoin
import asyncio
import sys
import os

# Add the parent directory to the path to import from src
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import for direct workflow execution
try:
    from src.service.workflow_service import run_agent_workflow as run_workflow_direct
    DIRECT_MODE_AVAILABLE = True
except ImportError:
    DIRECT_MODE_AVAILABLE = False
    print("Warning: Direct workflow execution not available. Only API mode will work.")

# Page configuration
st.set_page_config(
    page_title="LangManus - Multiagent System",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for modern, minimal design
st.markdown("""
<style>
    /* Import modern font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Root variables for consistent theming */
    :root {
        --navy-blue: #1e3a8a;
        --light-navy: #3b82f6;
        --dark-navy: #1e40af;
        --pure-white: #ffffff;
        --light-gray: #f8fafc;
        --border-gray: #e2e8f0;
        --text-gray: #64748b;
        --text-dark: #1e293b;
    }
    
    /* Main container styling */
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 2rem;
        font-family: 'Inter', sans-serif;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom chat message styling */
    .chat-message {
        padding: 1.25rem;
        border-radius: 16px;
        margin-bottom: 1rem;
        border: 1px solid var(--border-gray);
        background: var(--pure-white);
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        transition: all 0.2s ease;
    }
    
    .chat-message:hover {
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }
    
    .user-message {
        background: var(--navy-blue);
        color: var(--pure-white);
        margin-left: 3rem;
        border: none;
    }
    
    .assistant-message {
        background: var(--light-gray);
        color: var(--text-dark);
        margin-right: 3rem;
        border: 1px solid var(--border-gray);
    }
    
    .system-message {
        background: var(--light-navy);
        color: var(--pure-white);
        font-size: 0.9rem;
        opacity: 0.95;
        border: none;
    }
    
    /* Header styling */
    .main-header {
        text-align: center;
        padding: 3rem 2rem;
        background: var(--navy-blue);
        color: var(--pure-white);
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 20px rgba(30, 58, 138, 0.15);
    }
    
    .main-header h1 {
        font-weight: 700;
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }
    
    .main-header p {
        font-weight: 400;
        opacity: 0.9;
        font-size: 1.1rem;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: var(--pure-white);
    }
    
    .css-1lcbmhc {
        background: var(--pure-white);
    }
    
    /* Configuration section styling */
    .config-section {
        background: var(--light-gray);
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        border: 1px solid var(--border-gray);
    }
    
    .config-section h3 {
        color: var(--navy-blue);
        font-weight: 600;
        margin-bottom: 1rem;
    }
    
    /* Status indicators */
    .status-indicator {
        display: inline-block;
        width: 10px;
        height: 10px;
        border-radius: 50%;
        margin-right: 8px;
    }
    
    .status-connected {
        background-color: #10b981;
    }
    
    .status-disconnected {
        background-color: #ef4444;
    }
    
    .status-processing {
        background-color: #f59e0b;
        animation: pulse 1.5s infinite;
    }
    
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.5; }
        100% { opacity: 1; }
    }
    
    /* Agent status styling */
    .agent-status {
        padding: 1rem 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        border-left: 4px solid;
        font-weight: 500;
        font-size: 0.95rem;
    }
    
    .agent-processing {
        background: #fef3c7;
        border-left-color: #f59e0b;
        color: #92400e;
    }
    
    .agent-completed {
        background: #dcfce7;
        border-left-color: #10b981;
        color: #065f46;
    }
    
    .agent-error {
        background: #fecaca;
        border-left-color: #ef4444;
        color: #991b1b;
    }
    
    /* Streaming indicator */
    .streaming-indicator {
        display: inline-flex;
        align-items: center;
        padding: 0.25rem 0.75rem;
        background: #e0f2fe;
        border-radius: 20px;
        font-size: 0.8rem;
        color: var(--light-navy);
        margin-left: 0.5rem;
    }
    
    .streaming-dot {
        width: 6px;
        height: 6px;
        background: var(--light-navy);
        border-radius: 50%;
        margin-right: 0.5rem;
        animation: pulse 1.5s infinite;
    }
    
    /* Event log improvements */
    .event-log {
        background: var(--light-gray);
        border: 1px solid var(--border-gray);
        border-radius: 12px;
        padding: 1.5rem;
        font-family: 'SF Mono', 'Monaco', 'Cascadia Code', 'Roboto Mono', monospace;
        font-size: 0.8rem;
        max-height: 400px;
        overflow-y: auto;
        line-height: 1.5;
        color: var(--text-dark);
    }
    
    .event-log::-webkit-scrollbar {
        width: 6px;
    }
    
    .event-log::-webkit-scrollbar-track {
        background: #f1f5f9;
        border-radius: 3px;
    }
    
    .event-log::-webkit-scrollbar-thumb {
        background: var(--text-gray);
        border-radius: 3px;
    }
    
    .event-log::-webkit-scrollbar-thumb:hover {
        background: var(--navy-blue);
    }
    
    /* Button styling */
    .stButton > button {
        background: var(--navy-blue);
        color: var(--pure-white);
        border: none;
        border-radius: 10px;
        padding: 0.75rem 1.5rem;
        font-weight: 500;
        font-family: 'Inter', sans-serif;
        transition: all 0.2s ease;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    
    .stButton > button:hover {
        background: var(--dark-navy);
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(30, 58, 138, 0.2);
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    /* Form styling */
    .stTextArea > div > div > textarea {
        border-radius: 12px;
        border: 2px solid var(--border-gray);
        font-family: 'Inter', sans-serif;
        transition: border-color 0.2s ease;
    }
    
    .stTextArea > div > div > textarea:focus {
        border-color: var(--light-navy);
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
    }
    
    /* Input styling */
    .stTextInput > div > div > input {
        border-radius: 8px;
        border: 2px solid var(--border-gray);
        font-family: 'Inter', sans-serif;
        transition: border-color 0.2s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: var(--light-navy);
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
    }
    
    /* Checkbox styling */
    .stCheckbox {
        font-family: 'Inter', sans-serif;
    }
    
    /* Selectbox styling */
    .stSelectbox > div > div {
        border-radius: 8px;
        border: 2px solid var(--border-gray);
        font-family: 'Inter', sans-serif;
    }
    
    /* Metric styling */
    .metric-container {
        background: var(--pure-white);
        padding: 1rem;
        border-radius: 12px;
        border: 1px solid var(--border-gray);
        margin-bottom: 0.5rem;
    }
    
    /* Welcome message */
    .welcome-message {
        text-align: center;
        padding: 4rem 2rem;
        color: var(--text-gray);
        background: var(--light-gray);
        border-radius: 16px;
        margin: 2rem 0;
    }
    
    .welcome-message h3 {
        color: var(--navy-blue);
        font-weight: 600;
        margin-bottom: 1rem;
    }
    
    /* Section headers */
    h2, h3 {
        color: var(--navy-blue);
        font-weight: 600;
        font-family: 'Inter', sans-serif;
    }
    
    /* Clean up margins */
    .element-container {
        margin-bottom: 1rem;
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
if "current_thought_process" not in st.session_state:
    st.session_state.current_thought_process = ""

def display_header():
    """Display the main header"""
    st.markdown("""
    <div style="text-align: center; padding: 2rem 1rem; margin-bottom: 2rem;">
        <h1 style="color: #1e3a8a; font-weight: 600; margin: 0;">LangManus</h1>
    </div>
    """, unsafe_allow_html=True)

def extract_thought_process(content: str) -> str:
    """Extract thought process from planner content for sidebar display"""
    try:
        if content.strip().startswith('{') and content.strip().endswith('}'):
            import json
            data = json.loads(content)
            
            if "thought" in data and "title" in data:
                return f"""
                <div style="background: #f8fafc; padding: 1rem; border-radius: 8px; margin: 1rem 0; border-left: 3px solid #3b82f6;">
                    <h4 style="color: #1e3a8a; margin-bottom: 0.75rem; font-size: 1rem;">💭 Agent Analysis</h4>
                    <div style="background: #ffffff; padding: 0.75rem; border-radius: 6px; margin-bottom: 0.75rem;">
                        <strong style="font-size: 0.9rem;">Thought Process:</strong><br>
                        <em style="color: #64748b; font-size: 0.85rem; line-height: 1.4;">{data['thought']}</em>
                    </div>
                    <div style="background: #ffffff; padding: 0.75rem; border-radius: 6px;">
                        <strong style="font-size: 0.9rem;">Plan Title:</strong><br>
                        <span style="color: #1e293b; font-size: 0.85rem;">{data['title']}</span>
                    </div>
                </div>
                """
    except:
        pass
    return ""

def format_agent_content(content: str) -> str:
    """Format agent content to make it more readable - simplified version"""
    try:
        # Try to parse as JSON first
        if content.strip().startswith('{') and content.strip().endswith('}'):
            import json
            data = json.loads(content)
            
            # Handle thought processes - extract just the essential text
            if "thought" in data and "title" in data:
                result = f"💭 **Agent Analysis**\n\n"
                result += f"**Thought Process:** {data['thought']}\n\n"
                result += f"**Plan Title:** {data['title']}\n\n"
                
                # Add steps if they exist
                if "steps" in data and isinstance(data["steps"], list):
                    result += "**Execution Plan:**\n"
                    for i, step in enumerate(data["steps"], 1):
                        agent_icons = {
                            "researcher": "🔍",
                            "coder": "💻", 
                            "browser": "🌐",
                            "reporter": "📄",
                            "supervisor": "👥",
                            "planner": "📋",
                            "coordinator": "🎯"
                        }
                        agent_icon = agent_icons.get(step.get("agent_name"), "🤖")
                        
                        result += f"\n{i}. {agent_icon} **{step.get('title', 'Untitled')}** ({step.get('agent_name', 'unknown').title()})\n"
                        result += f"   {step.get('description', '')}\n"
                        if step.get("note"):
                            result += f"   💡 {step.get('note')}\n"
                
                return result
            
            # For other JSON structures, just show key information
            else:
                # Extract key fields if they exist
                result = ""
                if "content" in data:
                    result += f"{data['content']}\n"
                elif "message" in data:
                    result += f"{data['message']}\n"
                elif "text" in data:
                    result += f"{data['text']}\n"
                else:
                    # If no recognizable structure, show the raw content but cleaner
                    result = str(data)
                
                return result
        
        # If not JSON, return as-is
        else:
            return content
            
    except json.JSONDecodeError:
        # If JSON parsing fails, return as plain text
        return content
    except Exception:
        return content

def display_message(message: Dict[str, str], is_user: bool = False):
    """Display a chat message with simplified styling"""
    role = message.get("role", "assistant")
    content = message.get("content", "")
    
    if role == "user":
        icon = "👤"
        # User messages in blue background
        st.markdown(f"""
        <div style="background: #1e3a8a; color: white; padding: 1rem; border-radius: 10px; margin: 1rem 3rem 1rem 0;">
            <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                <span style="margin-right: 0.5rem;">{icon}</span>
                <strong>You</strong>
            </div>
            <div>{content}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        icon = "🤖"
        # Format assistant content for better readability but keep it simple
        formatted_content = format_agent_content(content)
        
        # Assistant messages in light background
        st.markdown(f"""
        <div style="background: #f8fafc; border: 1px solid #e2e8f0; padding: 1rem; border-radius: 10px; margin: 1rem 0 1rem 3rem;">
            <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                <span style="margin-right: 0.5rem;">{icon}</span>
                <strong>Assistant</strong>
            </div>
            <div style="white-space: pre-wrap; font-family: inherit;">{formatted_content}</div>
        </div>
        """, unsafe_allow_html=True)

def get_server_status(api_url: str) -> bool:
    """Check if the API server is running"""
    try:
        response = requests.get(f"{api_url}/docs", timeout=5)
        return response.status_code == 200
    except:
        return False

async def run_direct_workflow(messages: List[Dict], config: Dict) -> None:
    """Run workflow directly without API server - with streaming simulation"""
    if not DIRECT_MODE_AVAILABLE:
        st.error("❌ Direct workflow execution is not available. Please start the API server.")
        return
    
    try:
        # Create containers for streaming output
        response_container = st.empty()
        current_response = ""
        
        # Show processing indicator
        with st.status("Running workflow directly...", expanded=True) as status:
            status.write("🤖 Starting direct workflow execution...")
            
            # Convert messages to the format expected by the direct workflow
            user_input_messages = []
            for msg in messages:
                if msg["role"] == "user":
                    user_input_messages.append({"role": "user", "content": msg["content"]})
            
            if not user_input_messages:
                st.error("No user messages found")
                return
            
            # Run the workflow directly with streaming events
            agent_responses = []
            final_message = ""
            
            async for event in run_workflow_direct(
                user_input_messages=user_input_messages,
                debug=config.get("debug", False),
                deep_thinking_mode=config.get("deep_thinking_mode", False),
                search_before_planning=config.get("search_before_planning", False)
            ):
                event_type = event.get("event")
                event_data = event.get("data", {})
                
                if event_type == "start_of_workflow":
                    status.write("🚀 Workflow started...")
                
                elif event_type == "start_of_agent":
                    agent_name = event_data.get("agent_name", "unknown")
                    status.write(f"🤖 Starting {agent_name.title()} agent...")
                
                elif event_type == "message":
                    # Handle streaming message content
                    if "delta" in event_data and "content" in event_data["delta"]:
                        delta_content = event_data["delta"]["content"]
                        current_response += delta_content
                        
                        # Update display with streaming content
                        with response_container:
                            if current_response.strip():
                                st.markdown(f"""
                                <div style="background: #f8fafc; border: 1px solid #e2e8f0; padding: 1rem; border-radius: 10px; margin: 1rem 0 1rem 3rem;">
                                    <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                                        <span style="margin-right: 0.5rem;">🤖</span>
                                        <strong>Assistant</strong>
                                        <span style="margin-left: auto; color: #64748b; font-size: 0.8rem;">
                                            <div class="streaming-dot"></div>Processing...
                                        </span>
                                    </div>
                                    <div style="white-space: pre-wrap; font-family: inherit;">{format_agent_content(current_response.strip())}</div>
                                </div>
                                """, unsafe_allow_html=True)
                
                elif event_type == "end_of_agent":
                    agent_name = event_data.get("agent_name", "unknown")
                    status.write(f"✅ {agent_name.title()} agent completed")
                
                elif event_type == "tool_call":
                    tool_name = event_data.get("tool_name", "unknown")
                    status.write(f"🔧 Using tool: {tool_name}")
                
                elif event_type == "end_of_workflow":
                    status.write("🎉 Workflow completed!")
                    final_message = current_response.strip()
                    break
            
            # Update status when complete
            status.update(label="Direct workflow completed!", state="complete")
        
        # Store final response in session history
        if final_message:
            st.session_state.messages.append({
                "role": "assistant", 
                "content": final_message
            })
            
            # Final display without streaming indicator
            with response_container:
                display_message({"role": "assistant", "content": final_message})
            
            st.success("✅ Response completed!")
        else:
            st.warning("⚠️ No response content received from direct workflow.")
    
    except Exception as e:
        st.error(f"❌ Error running direct workflow: {str(e)}")
        st.exception(e)  # For debugging

def stream_chat_response(api_url: str, messages: List[Dict], config: Dict) -> None:
    """Stream chat response from the API - simplified version"""
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
        
        # Create containers for streaming output
        response_container = st.empty()
        current_response = ""
        
        # Show simple processing indicator
        with st.status("Processing your request...", expanded=True) as status:
            # Process SSE stream
            client = sseclient.SSEClient(response)
            
            for event in client.events():
                if event.event and event.data:
                    try:
                        event_data = json.loads(event.data)
                        
                        # Handle message content streaming - simplified
                        if event.event == "message":
                            if "delta" in event_data and "content" in event_data["delta"]:
                                delta_content = event_data["delta"]["content"]
                                current_response += delta_content
                                
                                # Update display with clean content as it streams
                                with response_container:
                                    if current_response.strip():
                                        # Show the streaming content in a clean format
                                        st.markdown(f"""
                                        <div style="background: #f8fafc; border: 1px solid #e2e8f0; padding: 1rem; border-radius: 10px; margin: 1rem 0 1rem 3rem;">
                                            <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                                                <span style="margin-right: 0.5rem;">🤖</span>
                                                <strong>Assistant</strong>
                                                <span style="margin-left: auto; color: #64748b; font-size: 0.8rem;">
                                                    <div class="streaming-dot"></div>Thinking...
                                                </span>
                                            </div>
                                            <div style="white-space: pre-wrap; font-family: inherit;">{format_agent_content(current_response.strip())}</div>
                                        </div>
                                        """, unsafe_allow_html=True)
                        
                        elif event.event == "error":
                            st.error(f"Error: {event_data}")
                            status.update(label="Error occurred", state="error")
                            break
                            
                    except json.JSONDecodeError as e:
                        st.warning(f"Failed to parse event data: {e}")
                        continue
                    except Exception as e:
                        st.warning(f"Error processing event: {e}")
                        continue
            
            # Update status when complete
            status.update(label="Response completed!", state="complete")
        
        # Store final response in session history
        if current_response.strip():
            st.session_state.messages.append({
                "role": "assistant",
                "content": current_response.strip()
            })
            
            # Final display without streaming indicator
            with response_container:
                display_message({"role": "assistant", "content": current_response.strip()})
            
            st.success("✅ Response completed!")
        else:
            st.warning("⚠️ No response content received.")
    
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
        st.markdown("## Configuration")
        
        # API Configuration
        st.markdown('<div class="config-section">', unsafe_allow_html=True)
        st.markdown("### API Settings")
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
            <span>API Server: {status_text}</span>
        </div>
        """, unsafe_allow_html=True)
        
        # Direct mode status
        direct_status_class = "status-connected" if DIRECT_MODE_AVAILABLE else "status-disconnected"
        direct_status_text = "Available" if DIRECT_MODE_AVAILABLE else "Not Available"
        
        st.markdown(f"""
        <div style="margin-top: 0.5rem;">
            <span class="status-indicator {direct_status_class}"></span>
            <span>Direct Mode: {direct_status_text}</span>
        </div>
        """, unsafe_allow_html=True)
        
        # Execution mode info
        if server_status:
            mode_text = "🌐 API Mode (Server Available)"
            mode_color = "var(--navy-blue)"
        elif DIRECT_MODE_AVAILABLE:
            mode_text = "🔧 Direct Mode (Fallback)"
            mode_color = "var(--light-navy)"
        else:
            mode_text = "❌ No Execution Mode Available"
            mode_color = "var(--text-gray)"
        
        st.markdown(f"""
        <div style="margin-top: 1rem; padding: 0.75rem; background: var(--light-gray); border-radius: 8px; border-left: 3px solid {mode_color};">
            <div style="font-weight: 500; color: {mode_color};">{mode_text}</div>
            <div style="font-size: 0.8rem; color: var(--text-gray); margin-top: 0.25rem;">
                {'Using API server for execution' if server_status else ('Using direct workflow execution' if DIRECT_MODE_AVAILABLE else 'Please start API server or fix direct mode')}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Agent Configuration
        st.markdown('<div class="config-section">', unsafe_allow_html=True)
        st.markdown("### Settings")
        
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
        
        # Execution Mode Selection
        st.markdown('<div class="config-section">', unsafe_allow_html=True)
        st.markdown("### Execution Mode")
        
        # Mode selection
        execution_mode = st.radio(
            "Choose execution mode:",
            options=["Auto", "API Only", "Direct Only"],
            index=0,
            help="Select how you want to execute workflows"
        )
        
        # Show mode status based on selection
        if execution_mode == "Auto":
            if server_status:
                selected_mode_text = "🌐 Will use API Mode (preferred)"
                selected_mode_color = "var(--navy-blue)"
            elif DIRECT_MODE_AVAILABLE:
                selected_mode_text = "🔧 Will use Direct Mode (fallback)"
                selected_mode_color = "var(--light-navy)"
            else:
                selected_mode_text = "❌ No mode available"
                selected_mode_color = "#ef4444"
        elif execution_mode == "API Only":
            if server_status:
                selected_mode_text = "🌐 API Mode (available)"
                selected_mode_color = "var(--navy-blue)"
            else:
                selected_mode_text = "⚠️ API Mode (not available)"
                selected_mode_color = "#f59e0b"
        else:  # Direct Only
            if DIRECT_MODE_AVAILABLE:
                selected_mode_text = "🔧 Direct Mode (available)"
                selected_mode_color = "var(--light-navy)"
            else:
                selected_mode_text = "⚠️ Direct Mode (not available)"
                selected_mode_color = "#f59e0b"
        
        st.markdown(f"""
        <div style="margin-top: 0.5rem; padding: 0.75rem; background: var(--light-gray); border-radius: 8px; border-left: 3px solid {selected_mode_color};">
            <div style="font-weight: 500; color: {selected_mode_color}; font-size: 0.9rem;">{selected_mode_text}</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Conversation Management
        st.markdown('<div class="config-section">', unsafe_allow_html=True)
        st.markdown("### Conversation")
        
        if st.button("Clear Conversation", use_container_width=True):
            st.session_state.messages = []
            st.session_state.event_log = []
            st.session_state.conversation_id += 1
            st.rerun()
        
        st.markdown(f"Messages: {len(st.session_state.messages)}")
        st.markdown(f"Conversation ID: {st.session_state.conversation_id}")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Execution Modes Help
        st.markdown('<div class="config-section">', unsafe_allow_html=True)
        st.markdown("### Execution Modes")
        
        with st.expander("ℹ️ About Execution Modes"):
            st.markdown("""
            **🌐 API Server Mode:**
            - Uses remote API server for workflow execution
            - Requires API server to be running
            - Best for production and shared environments
            
            **🔧 Direct Mode:**  
            - Runs workflow directly in the application
            - Useful for development and local testing
            - Requires all dependencies to be installed
            
            **Mode Selection Options:**
            - **Auto**: Automatically chooses the best available mode (API preferred)
            - **API Only**: Forces API mode (fails if server unavailable)
            - **Direct Only**: Forces direct mode (fails if dependencies missing)
            
            **Status Indicators:**
            - 🟢 Available and ready to use
            - ⚠️ Selected but not available
            - ❌ Not available
            """)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Main chat interface
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown("## Chat")
        
        # Display conversation history
        if st.session_state.messages:
            for message in st.session_state.messages:
                display_message(message)
        else:
            st.markdown("""
            <div style="text-align: center; padding: 3rem 1rem; color: #64748b;">
                <h3 style="color: #1e3a8a; font-weight: 500; margin-bottom: 1rem;">Welcome</h3>
                <p>Type your message below to get started.</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Chat input at the bottom
        with st.form("chat_form", clear_on_submit=True):
            user_input = st.text_area(
                "Your message:",
                height=100,
                placeholder="Type your message here..."
            )
            
            col_submit, col_example = st.columns([1, 2])
            
            with col_submit:
                submit_button = st.form_submit_button("Send", use_container_width=True)
            
            with col_example:
                if st.form_submit_button("Example Query", use_container_width=True):
                    user_input = "Help me create a comprehensive project plan for developing a mobile app."
                    submit_button = True
        
        # Process user input
        if submit_button and user_input.strip():
            # Add user message to history
            user_message = {"role": "user", "content": user_input.strip()}
            st.session_state.messages.append(user_message)
            
            # Configuration for execution
            config = {
                "debug": debug_mode,
                "deep_thinking_mode": deep_thinking_mode,
                "search_before_planning": search_before_planning
            }
            
            # Determine execution based on user selection
            should_use_api = False
            should_use_direct = False
            error_message = None
            
            if execution_mode == "Auto":
                # Automatic mode selection (original logic)
                if server_status:
                    should_use_api = True
                elif DIRECT_MODE_AVAILABLE:
                    should_use_direct = True
                else:
                    error_message = "❌ No execution mode available. Please start the API server or fix direct mode dependencies."
            
            elif execution_mode == "API Only":
                # Force API mode
                if server_status:
                    should_use_api = True
                else:
                    error_message = "❌ API mode selected but server is not available. Please start the API server or switch to Auto/Direct mode."
            
            elif execution_mode == "Direct Only":
                # Force direct mode
                if DIRECT_MODE_AVAILABLE:
                    should_use_direct = True
                else:
                    error_message = "❌ Direct mode selected but not available. Please install dependencies or switch to Auto/API mode."
            
            # Execute if we have a valid mode
            if error_message:
                st.error(error_message)
                # Remove the user message since we couldn't process it
                st.session_state.messages.pop()
                return
            
            # Execute the workflow
            if should_use_api:
                st.info("🌐 Using API Server Mode")
                with st.spinner("Processing via API..."):
                    stream_chat_response(
                        st.session_state.api_url,
                        st.session_state.messages,
                        config
                    )
            elif should_use_direct:
                st.info("🔧 Using Direct Mode")
                try:
                    # Run the async direct workflow
                    asyncio.run(run_direct_workflow(
                        st.session_state.messages,
                        config
                    ))
                except Exception as e:
                    st.error(f"❌ Error in direct mode execution: {str(e)}")
                    st.exception(e)
            
            # Rerun to show the new message
            st.rerun()
    
    with col2:
        st.markdown("## Status")
        
        # Execution Mode Status
        st.markdown("### Current Mode")
        server_status = get_server_status(st.session_state.api_url)
        
        # Get the execution mode from the sidebar (we need to access it here)
        # Since we can't directly access the radio button value here, we'll show general status
        
        # Show API Server Status
        if server_status:
            st.markdown("""
            <div style="background: #dcfce7; border: 1px solid #10b981; padding: 0.75rem; border-radius: 8px; margin-bottom: 0.5rem;">
                <div style="font-weight: 600; color: #065f46; font-size: 0.9rem;">🌐 API Server</div>
                <div style="font-size: 0.8rem; color: #065f46;">Connected and ready</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background: #fecaca; border: 1px solid #ef4444; padding: 0.75rem; border-radius: 8px; margin-bottom: 0.5rem;">
                <div style="font-weight: 600; color: #991b1b; font-size: 0.9rem;">🌐 API Server</div>
                <div style="font-size: 0.8rem; color: #991b1b;">Disconnected</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Show Direct Mode Status
        if DIRECT_MODE_AVAILABLE:
            st.markdown("""
            <div style="background: #dcfce7; border: 1px solid #10b981; padding: 0.75rem; border-radius: 8px; margin-bottom: 0.5rem;">
                <div style="font-weight: 600; color: #065f46; font-size: 0.9rem;">🔧 Direct Mode</div>
                <div style="font-size: 0.8rem; color: #065f46;">Available</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background: #fecaca; border: 1px solid #ef4444; padding: 0.75rem; border-radius: 8px; margin-bottom: 0.5rem;">
                <div style="font-weight: 600; color: #991b1b; font-size: 0.9rem;">🔧 Direct Mode</div>
                <div style="font-size: 0.8rem; color: #991b1b;">Not available</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Mode selection info
        st.markdown("""
        <div style="background: #e0f2fe; border: 1px solid #0284c7; padding: 0.75rem; border-radius: 8px; margin-bottom: 1rem;">
            <div style="font-weight: 600; color: #0c4a6e; font-size: 0.9rem;">💡 Mode Selection</div>
            <div style="font-size: 0.8rem; color: #0c4a6e;">Use the sidebar to choose your preferred execution mode</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Current configuration display
        st.markdown("### Settings")
        
        # Create a clean settings display
        settings_html = f"""
        <div style="background: var(--light-gray); padding: 1rem; border-radius: 12px; border: 1px solid var(--border-gray);">
            <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                <span style="color: {'var(--navy-blue)' if debug_mode else 'var(--text-gray)'}; margin-right: 0.5rem;">
                    {'🔍' if debug_mode else '⭕'}
                </span>
                <span style="font-weight: 500; color: var(--text-dark);">Debug Mode</span>
            </div>
            <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                <span style="color: {'var(--navy-blue)' if deep_thinking_mode else 'var(--text-gray)'}; margin-right: 0.5rem;">
                    {'🧠' if deep_thinking_mode else '⭕'}
                </span>
                <span style="font-weight: 500; color: var(--text-dark);">Deep Thinking</span>
            </div>
            <div style="display: flex; align-items: center;">
                <span style="color: {'var(--navy-blue)' if search_before_planning else 'var(--text-gray)'}; margin-right: 0.5rem;">
                    {'🔍' if search_before_planning else '⭕'}
                </span>
                <span style="font-weight: 500; color: var(--text-dark);">Search Planning</span>
            </div>
        </div>
        """
        st.markdown(settings_html, unsafe_allow_html=True)
        
        # Simple metrics
        st.markdown("### Stats")
        st.metric("Messages", len(st.session_state.messages))
        
        # Quick actions
        st.markdown("### Actions")
        
        if st.button("Refresh Status", use_container_width=True):
            st.rerun()
        
        if st.button("Export Chat", use_container_width=True):
            if st.session_state.messages:
                chat_export = json.dumps(st.session_state.messages, indent=2)
                st.download_button(
                    "Download JSON",
                    chat_export,
                    file_name=f"langmanus_chat_{int(time.time())}.json",
                    mime="application/json",
                    use_container_width=True
                )
            else:
                st.info("No messages to export")

if __name__ == "__main__":
    main()