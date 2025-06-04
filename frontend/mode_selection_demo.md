# LangManus Manual Mode Selection

## 🎯 Overview
The LangManus frontend now supports **manual execution mode selection**, giving you full control over how workflows are executed.

## 🚀 New Features

### **Manual Mode Selection**
Choose from three execution modes in the sidebar:

1. **🔄 Auto** (Default)
   - Automatically selects the best available mode
   - Prefers API mode when server is available
   - Falls back to Direct mode if API is unavailable
   - **Best for most users**

2. **🌐 API Only**
   - Forces execution through the API server
   - Will fail with clear error if server is unavailable
   - **Best for production environments**

3. **🔧 Direct Only**
   - Forces local direct execution
   - Will fail with clear error if dependencies are missing
   - **Best for development/testing**

### **Visual Status Indicators**

#### Sidebar Indicators:
- 🟢 **Available**: Mode is ready to use
- ⚠️ **Selected but not available**: Mode is chosen but cannot be used
- ❌ **Not available**: Mode dependencies are missing

#### Status Panel:
- Real-time status of both API server and Direct mode
- Clear indication of current mode selection
- Helpful guidance for troubleshooting

## 🛠️ How It Works

### **Mode Selection Logic**
```
User Selection: Auto
├── API Server Available? → Use API Mode
├── Direct Mode Available? → Use Direct Mode
└── Neither Available? → Show Error

User Selection: API Only
├── API Server Available? → Use API Mode
└── API Server Unavailable? → Show Error + Suggest Alternatives

User Selection: Direct Only
├── Direct Mode Available? → Use Direct Mode
└── Direct Mode Unavailable? → Show Error + Suggest Alternatives
```

### **Error Handling**
- **Clear error messages** when selected mode is unavailable
- **Helpful suggestions** for resolving issues
- **User message protection** (removes unsent messages on error)

## 📋 Usage Examples

### **Scenario 1: Both Modes Available**
- **Auto**: Uses API Mode (preferred)
- **API Only**: Uses API Mode
- **Direct Only**: Uses Direct Mode

### **Scenario 2: Only API Available**
- **Auto**: Uses API Mode
- **API Only**: Uses API Mode
- **Direct Only**: ❌ Error with helpful message

### **Scenario 3: Only Direct Available**
- **Auto**: Uses Direct Mode (fallback)
- **API Only**: ❌ Error with helpful message
- **Direct Only**: Uses Direct Mode

### **Scenario 4: Neither Available**
- **Auto**: ❌ Error with setup instructions
- **API Only**: ❌ Error with server startup instructions
- **Direct Only**: ❌ Error with dependency installation instructions

## 🎨 UI Improvements

### **Enhanced Sidebar**
- Clean mode selection radio buttons
- Real-time status indicators for both modes
- Dynamic feedback based on selection
- Comprehensive help section

### **Improved Status Panel**
- Individual status cards for each mode
- Color-coded availability indicators
- Mode selection guidance
- Quick troubleshooting tips

## 🔧 Technical Details

### **Mode Detection**
- **API Mode**: Tests connection to `/docs` endpoint
- **Direct Mode**: Attempts to import `src.service.workflow_service`

### **Execution Flow**
1. User selects mode in sidebar
2. App validates selection against availability
3. Execution proceeds or shows helpful error
4. Status updates in real-time

### **Fallback Behavior**
- Only applies in **Auto** mode
- Clear indication when fallback is used
- No unexpected mode switches

## 🚀 Benefits

✅ **Full Control**: Choose exactly how you want to execute workflows
✅ **Clear Feedback**: Always know which mode is being used and why
✅ **Better Errors**: Helpful messages when things go wrong
✅ **Flexible**: Works in any environment configuration
✅ **User-Friendly**: Intuitive interface with helpful guidance

---

*Now you have complete control over your LangManus execution environment!* 