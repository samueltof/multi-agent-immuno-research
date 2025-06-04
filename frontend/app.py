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
    """Format agent content to make it more readable"""
    try:
        # Try to parse as JSON first
        if content.strip().startswith('{') and content.strip().endswith('}'):
            import json
            data = json.loads(content)
            
            # Handle thought processes
            if "thought" in data and "title" in data:
                formatted = f"""
                <div style="background: #f8fafc; padding: 1.5rem; border-radius: 12px; margin: 1rem 0; border-left: 4px solid #3b82f6;">
                    <h4 style="color: #1e3a8a; margin-bottom: 1rem;">💭 Agent Analysis</h4>
                    <div style="background: #ffffff; padding: 1rem; border-radius: 8px; margin-bottom: 1rem;">
                        <strong>Thought Process:</strong><br>
                        <em style="color: #64748b;">{data['thought']}</em>
                    </div>
                    <div style="background: #ffffff; padding: 1rem; border-radius: 8px;">
                        <strong>Plan Title:</strong> {data['title']}
                    </div>
                </div>
                """
                
                # Add steps if they exist
                if "steps" in data and isinstance(data["steps"], list):
                    formatted += """
                    <div style="background: #f8fafc; padding: 1.5rem; border-radius: 12px; margin: 1rem 0;">
                        <h4 style="color: #1e3a8a; margin-bottom: 1rem;">📋 Execution Plan</h4>
                    """
                    
                    for i, step in enumerate(data["steps"], 1):
                        # Better agent icon mapping
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
                        
                        formatted += f"""
                        <div style="background: #ffffff; padding: 1rem; border-radius: 8px; margin-bottom: 0.5rem; border-left: 3px solid #3b82f6;">
                            <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                                <span style="background: #1e3a8a; color: #ffffff; padding: 0.25rem 0.5rem; border-radius: 6px; font-size: 0.8rem; margin-right: 0.5rem;">
                                    Step {i}
                                </span>
                                <span style="margin-right: 0.5rem;">{agent_icon}</span>
                                <strong>{step.get('title', 'Untitled')}</strong>
                                <span style="margin-left: auto; color: #64748b; font-size: 0.8rem;">
                                    {step.get('agent_name', 'unknown').title()}
                                </span>
                            </div>
                            <p style="margin-bottom: 0.5rem; color: #1e293b;">{step.get('description', '')}</p>
                            {f'<p style="font-size: 0.9rem; color: #64748b; font-style: italic;">💡 {step.get("note", "")}</p>' if step.get("note") else ''}
                        </div>
                        """
                    formatted += "</div>"
                
                return formatted
            
            # Handle other JSON structures
            else:
                return f"""
                <div style="background: #f8fafc; padding: 1rem; border-radius: 8px; font-family: monospace; font-size: 0.9rem;">
                    <pre>{json.dumps(data, indent=2)}</pre>
                </div>
                """
        
        # If not JSON, return as-is but with better formatting
        else:
            # Handle markdown headers
            content = content.replace('# ', '<h3 style="color: #1e3a8a; margin: 1.5rem 0 1rem 0;">')
            content = content.replace('## ', '<h4 style="color: #1e3a8a; margin: 1rem 0 0.5rem 0;">')
            content = content.replace('\n\n', '</p><p>')
            
            if not content.startswith('<'):
                content = f'<p>{content}</p>'
            if content.endswith('</p><p>'):
                content = content[:-7]
            
            return content
            
    except json.JSONDecodeError:
        # If JSON parsing fails, return formatted text
        content = content.replace('# ', '<h3 style="color: #1e3a8a; margin: 1.5rem 0 1rem 0;">')
        content = content.replace('## ', '<h4 style="color: #1e3a8a; margin: 1rem 0 0.5rem 0;">')
        content = content.replace('\n\n', '</p><p>')
        
        if not content.startswith('<'):
            content = f'<p>{content}</p>'
        if content.endswith('</p><p>'):
            content = content[:-7]
            
        return content
    except Exception:
        return content

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
        # Format assistant content for better readability
        content = format_agent_content(content)
    
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
    
    # Agent descriptions for better context
    agent_descriptions = {
        "coordinator": "🎯 Analyzes the request and decides the best workflow approach",
        "planner": "📋 Creates detailed step-by-step execution plans for complex tasks",
        "supervisor": "👥 Manages team coordination and delegates tasks to specialized agents",
        "researcher": "🔍 Searches for information using web searches and data collection",
        "coder": "💻 Executes Python code, performs calculations, and technical analysis",
        "browser": "🌐 Interacts with web pages and performs complex web operations",
        "reporter": "📄 Compiles comprehensive reports from all gathered information"
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
        
        # Create containers for different types of content
        response_container = st.empty()
        current_response = ""
        
        # Create event log container
        event_container = st.expander("📊 Event Log", expanded=False)
        
        # Track agent outputs separately
        agent_outputs = {}
        current_agent_output = ""
        current_output_agent = None
        
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
                    
                    # Track agent state changes for output capture
                    if event.event == "start_of_agent":
                        agent_name = event_data.get("agent_name", "unknown")
                        current_output_agent = agent_name
                        current_agent_output = ""
                    elif event.event == "end_of_agent":
                        agent_name = event_data.get("agent_name", "unknown")
                        # Store the agent's output
                        if current_output_agent == agent_name and current_agent_output.strip():
                            agent_outputs[agent_name] = current_agent_output.strip()
                            current_agent_output = ""
                            current_output_agent = None
                    
                    # Update event log display
                    with event_container:
                        event_log_text = ""
                        for log_entry in st.session_state.event_log[-20:]:  # Show last 20 events
                            event_log_text += f"[{log_entry['timestamp']}] {log_entry['event']}: {str(log_entry['data'])[:150]}...\n"
                        
                        st.code(event_log_text, language="text")
                    
                    # Handle message content streaming with better filtering
                    if event.event == "message":
                        # Handle delta content from streaming
                        if "delta" in event_data and "content" in event_data["delta"]:
                            delta_content = event_data["delta"]["content"]
                            
                            # Filter out supervisor routing JSON
                            if delta_content.strip().startswith('{"next":') or delta_content.strip() == '{"next":"FINISH"}':
                                continue
                                
                            # Capture planner output (structured plans)
                            if current_output_agent == "planner":
                                current_agent_output += delta_content
                                
                                # Show simple "Planning..." message during planner work
                                with response_container:
                                    display_message({"role": "assistant", "content": "Planning your request..."})
                            
                            # Capture coordinator, reporter, and other final outputs
                            elif current_output_agent in ["coordinator", "reporter"] or not current_output_agent:
                                current_response += delta_content
                                
                                # Update display immediately during streaming
                                with response_container:
                                    if current_response.strip():
                                        display_message({"role": "assistant", "content": current_response.strip()})
                    
                    elif event.event == "error":
                        st.error(f"Workflow Error: {event_data}")
                        break
                        
                except json.JSONDecodeError as e:
                    st.warning(f"Failed to parse event data: {e}")
                    continue
                except Exception as e:
                    st.warning(f"Error processing event: {e}")
                    continue
        
        # Handle final response for session history
        final_response = current_response.strip() if current_response.strip() else "Response completed."
        
        # Handle planner output for sidebar
        if current_agent_output.strip():
            thought_process = extract_thought_process(current_agent_output.strip())
            if thought_process:
                st.session_state.current_thought_process = thought_process
        
        # Store in session history
        if final_response and final_response != "Planning your request...":
            st.session_state.messages.append({
                "role": "assistant", 
                "content": final_response
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
            <span>{status_text}</span>
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
            if not server_status:
                st.error("⚠️ API server is not available. Please check the server status.")
                return
            
            # Add user message to history
            user_message = {"role": "user", "content": user_input.strip()}
            st.session_state.messages.append(user_message)
            
            # Configuration for API call
            config = {
                "debug": debug_mode,
                "deep_thinking_mode": deep_thinking_mode,
                "search_before_planning": search_before_planning
            }
            
            # Stream response
            with st.spinner("Processing..."):
                stream_chat_response(
                    st.session_state.api_url,
                    st.session_state.messages,
                    config
                )
            
            # Rerun to show the new message
            st.rerun()
    
    with col2:
        st.markdown("## Status")
        
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
        
        # Performance metrics (placeholder)
        st.markdown("### Performance")
        st.metric("Total Messages", len(st.session_state.messages))
        st.metric("Events Logged", len(st.session_state.event_log))
        
        # Display thought process if available
        if st.session_state.current_thought_process:
            st.markdown("### Current Analysis")
            st.markdown(st.session_state.current_thought_process, unsafe_allow_html=True)
        
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