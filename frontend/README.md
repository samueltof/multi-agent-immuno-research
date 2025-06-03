 # LangManus Frontend

A modern, aesthetic Streamlit interface for the LangManus multiagent system.

## Features

🎨 **Modern UI Design**
- Clean, gradient-based design with smooth animations
- Responsive layout that works on different screen sizes
- Professional color scheme and typography

🤖 **Full Multiagent Integration**
- Real-time streaming responses from the LangManus API
- Support for all configuration options (debug, deep thinking, search before planning)
- Live event logging and system status monitoring

💬 **Enhanced Chat Experience**
- Beautiful message bubbles with role-based styling
- Conversation history management
- Export chat functionality
- Quick example queries

⚙️ **Configuration & Monitoring**
- Real-time server status checking
- Configurable API endpoint
- Performance metrics display
- Event log viewer

## Installation

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Frontend**
   ```bash
   streamlit run app.py
   ```

3. **Configure API Connection**
   - The default API URL is `http://localhost:8000`
   - You can change this in the sidebar configuration
   - Make sure your LangManus API server is running

## Usage

### Basic Chat
1. Enter your message in the text area at the bottom
2. Click "Send 🚀" to submit your query
3. Watch the streaming response appear in real-time

### Configuration Options

**Debug Mode**: Enable detailed logging of the workflow execution

**Deep Thinking Mode**: Activate advanced reasoning capabilities for complex queries

**Search Before Planning**: Enable web search before creating execution plans

### Example Queries

Try these example queries to see the multiagent system in action:

- "Help me create a comprehensive project plan for developing a mobile app"
- "Analyze the pros and cons of different database technologies"
- "Design a marketing strategy for a new SaaS product"
- "Research the latest trends in artificial intelligence"

### Advanced Features

**Event Log**: Expand the "📊 Event Log" section to see real-time workflow events

**Export Chat**: Download your conversation history as a JSON file

**System Status**: Monitor connection status and performance metrics in the sidebar

## Troubleshooting

### Connection Issues
- Ensure the LangManus API server is running on the configured port
- Check that CORS is properly configured in the API
- Verify the API URL in the sidebar settings

### Streaming Issues
- If responses appear slowly, check your network connection
- Large responses may take time to process completely
- Check the event log for any error messages

### Performance
- Clear conversation history periodically for better performance
- Monitor the event log size (automatically limited to last 10 events)
- Refresh the page if the interface becomes unresponsive

## API Integration

The frontend communicates with the LangManus API using:

- **Endpoint**: `/api/chat/stream`
- **Method**: POST
- **Content-Type**: `application/json`
- **Response**: Server-Sent Events (SSE)

The request payload includes:
```json
{
  "messages": [...],
  "debug": false,
  "deep_thinking_mode": false,
  "search_before_planning": false
}
```

## Customization

### Styling
The UI uses custom CSS defined in the main app file. You can modify:
- Color gradients in the CSS section
- Message bubble styling
- Animation effects
- Layout proportions

### Configuration
Default settings can be modified in the session state initialization:
- API URL
- Default configuration values
- UI layout options

## Development

To contribute to the frontend:

1. Fork the repository
2. Make your changes to `app.py`
3. Test with the LangManus API running
4. Submit a pull request

### Code Structure
- `main()`: Main application logic
- `display_header()`: Header component
- `display_message()`: Message display component
- `stream_chat_response()`: API communication and streaming
- `get_server_status()`: Server health checking