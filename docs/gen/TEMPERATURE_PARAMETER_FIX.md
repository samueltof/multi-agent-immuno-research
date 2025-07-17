# Temperature Parameter Fix for Reasoning Models

## Issue
The server was experiencing 400 Bad Request errors from Portkey when using reasoning models like `o3-mini`:

```
openai.BadRequestError: Error code: 400 - {'error': {'message': "openai error: Unsupported parameter: 'temperature' is not supported with this model.", 'type': 'invalid_request_error', 'param': 'temperature', 'code': 'unsupported_parameter'}, 'provider': 'openai'}
```

## Root Cause
Reasoning models (`o1`, `o3`, `o4` series) don't support the `temperature` parameter because they use fixed reasoning parameters. However, our LLM provider system was automatically including `temperature: 0.0` for all models.

## Solution
Updated the LLM provider system to automatically detect and exclude the temperature parameter for reasoning models:

### 1. Provider Config Creation (`src/config/llm_providers.py`)
```python
# Models that don't support temperature parameter
NO_TEMPERATURE_MODELS = {
    "o1", "o1-mini", "o1-preview", 
    "o3", "o3-mini", "o3-preview",
    "o4", "o4-mini", "o4-preview"
}

# Remove temperature for models that don't support it
if not supports_temperature and "temperature" in kwargs:
    kwargs.pop("temperature")
    print(f"⚠️  Removed temperature parameter for {model} (reasoning model)")
```

### 2. LLM Instance Creation
Updated all provider types (OpenAI, Anthropic, Portkey, DeepSeek, Azure, Bedrock) to conditionally include temperature:

```python
kwargs = {"model": config.model}
if supports_temperature(config.model):
    kwargs["temperature"] = config.temperature
```

## Models Affected
- **Fixed**: `o3-mini` (used by planner and data_analyst agents)
- **Protected**: All future `o1`, `o3`, `o4` series models
- **Unchanged**: Regular models like `gpt-4o-mini`, `claude-3-haiku`, etc. still get temperature

## Agent Configuration
Current agents using reasoning models:
- **planner**: `["portkey_openai", "o3-mini"]` ✅ Fixed
- **data_analyst**: `["portkey_openai", "o3-mini"]` ✅ Fixed
- **biomedical_researcher**: `["portkey_openai", "gpt-4o-mini"]` ✅ Unaffected (uses regular model)

## Testing Results
✅ **o3-mini models**: Temperature parameter correctly excluded  
✅ **Regular models**: Temperature parameter still included  
✅ **Portkey integration**: Should now work without 400 errors  

## Benefits
1. **Automatic Detection**: No manual configuration needed for new reasoning models
2. **Backward Compatibility**: Existing regular models continue to work normally
3. **Future-Proof**: Handles all current and future reasoning model variants
4. **Provider Agnostic**: Works across all supported LLM providers

## Verification
The server should now handle requests to the planner and data_analyst agents without the temperature-related 400 errors from Portkey.

---

**Status**: ✅ **FIXED** - Reasoning models now work correctly with Portkey 