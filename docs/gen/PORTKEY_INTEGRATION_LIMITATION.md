# Portkey Integration Limitation - Global Interference Issue

## Problem Summary

The biomedical researcher agent **cannot function when Portkey AI is installed** due to a critical global interference issue.

## Root Cause

**Portkey globally monkey-patches the OpenAI client** at the Python module level, causing a `NotGiven` serialization error that prevents any PydanticAI agents from working.

### Technical Details

1. **Global Import Replacement**: Portkey replaces the entire OpenAI module with its own vendored version (`portkey_ai/_vendor/openai/`)

2. **Serialization Conflict**: The vendored OpenAI client produces `NotGiven` objects that cannot be JSON serialized, causing this error:
   ```
   TypeError: Object of type NotGiven is not JSON serializable
   ```

3. **No Workaround Possible**: Even creating "direct" OpenAI providers still routes through Portkey's vendored client:
   ```python
   # This STILL goes through Portkey despite appearing to be direct OpenAI
   provider = OpenAIProvider(api_key=api_key, base_url="https://api.openai.com/v1")
   ```

## Evidence

The stack trace clearly shows the issue:
```
File ".../portkey_ai/_vendor/openai/resources/chat/completions/completions.py", line 2028, in create
```

Even when configured for "direct OpenAI", all calls route through Portkey's vendored client.

## Impact

- ✅ **Other Agents**: Work fine with Portkey (coordinator, planner, researcher, etc.)
- ❌ **Biomedical Researcher**: Cannot function with Portkey installed
- 🔄 **Workflow**: Continues with graceful error handling, other agents take over

## Current Solution

The biomedical researcher uses graceful error handling:

```python
except Exception as e:
    logger.error(f"Error in biomedical research: {e}")
    return BiomedicalResearchOutput(
        summary=f"Error occurred during biomedical research: {str(e)}",
        key_findings=[],
        sources=[],
        recommendations=["Please check the configuration and try again"],
        confidence_level=0.0
    )
```

## Alternatives

### Option 1: Separate Environment
Run biomedical researcher in a separate Python environment without Portkey:
- Pros: Fully functional biomedical researcher
- Cons: Complex deployment, separate API management

### Option 2: Alternative Biomedical Tools
Use the regular research agent with biomedical search tools:
- Pros: Works with Portkey, simpler deployment
- Cons: Less specialized biomedical capabilities

### Option 3: Wait for Portkey Fix
Monitor Portkey releases for fixes to global monkey-patching:
- Pros: Would restore full functionality
- Cons: Timeline uncertain, dependency on external fix

## Recommendation

**For Production**: Use the current graceful error handling. The workflow continues successfully with the regular researcher agent providing biomedical research capabilities.

**For Development**: If biomedical researcher functionality is critical, consider Option 1 with a separate environment.

## Status

- **Date**: 2025-01-16
- **Portkey Version**: 1.14.1
- **PydanticAI Version**: Latest
- **Issue Status**: Confirmed limitation, workaround implemented
- **Production Impact**: Minimal (graceful fallback functional) 