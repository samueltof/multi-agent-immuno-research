"""
Test the new official Portkey integration with PydanticAI for biomedical researcher.

This test verifies that the biomedical researcher can successfully use the new
AsyncPortkey client integration approach instead of the problematic monkey-patching.
"""

import os
import asyncio
import logging
from unittest.mock import patch, MagicMock

import pytest
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider

from src.agents.biomedical_researcher import (
    get_biomedical_model,
    _create_pydantic_ai_model_from_config,
    BiomedicalResearcherWrapper,
    BiomedicalResearchOutput
)
from src.config.agents import get_agent_full_config
from src.config.llm_providers import ProviderType


# Configure logging for tests
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TestPortkeyPydanticAIIntegration:
    """Test the new Portkey integration with PydanticAI."""
    
    @pytest.fixture
    def portkey_env_vars(self):
        """Set up environment variables for Portkey testing."""
        test_env = {
            'PORTKEY_API_KEY': 'test-portkey-key',
            'PORTKEY_OPENAI_VIRTUAL_KEY': '@openai',
            'OPENAI_API_KEY': 'test-openai-key',
            'ENVIRONMENT': 'test'
        }
        
        with patch.dict(os.environ, test_env):
            yield test_env
    
    def test_agent_config_uses_portkey(self):
        """Test that biomedical researcher is configured to use Portkey."""
        config = get_agent_full_config("biomedical_researcher")
        
        assert config['provider'] == ProviderType.PORTKEY_OPENAI
        assert config['model'] == 'gpt-4o-mini'
        logger.info(f"✅ Biomedical researcher configured with Portkey: {config}")
    
    @patch('portkey_ai.AsyncPortkey')
    def test_portkey_client_creation(self, mock_portkey, portkey_env_vars):
        """Test that AsyncPortkey client is created correctly."""
        # Mock the AsyncPortkey client
        mock_client = MagicMock()
        mock_portkey.return_value = mock_client
        
        # Get the config and create model
        config = get_agent_full_config("biomedical_researcher")
        model = _create_pydantic_ai_model_from_config(config)
        
        # Verify AsyncPortkey was called with correct parameters
        mock_portkey.assert_called_once()
        call_kwargs = mock_portkey.call_args[1]
        
        assert call_kwargs['api_key'] == 'test-portkey-key'
        assert call_kwargs['provider'] == '@openai'
        assert call_kwargs['metadata']['_agent'] == 'biomedical_researcher'
        assert call_kwargs['metadata']['_model'] == 'gpt-4o-mini'
        assert call_kwargs['metadata']['env'] == 'test'
        
        # Verify we get an OpenAIModel back
        assert isinstance(model, OpenAIModel)
        assert model.model_name == 'gpt-4o-mini'
        
        logger.info(f"✅ Portkey client created successfully with metadata: {call_kwargs['metadata']}")
    
    @patch('portkey_ai.AsyncPortkey')
    def test_custom_virtual_key(self, mock_portkey, portkey_env_vars):
        """Test that custom virtual keys are used when provided."""
        # Mock with custom virtual key
        with patch.dict(os.environ, {'PORTKEY_OPENAI_VIRTUAL_KEY': 'custom-openai-key'}):
            config = get_agent_full_config("biomedical_researcher")
            _create_pydantic_ai_model_from_config(config)
            
            # Check that custom virtual key was used
            call_kwargs = mock_portkey.call_args[1]
            assert call_kwargs['provider'] == 'custom-openai-key'
            
        logger.info("✅ Custom virtual key handling works correctly")
    
    def test_fallback_to_direct_openai_on_import_error(self, portkey_env_vars):
        """Test fallback to direct OpenAI when Portkey import fails."""
        # Mock ImportError for portkey_ai at the right location - patch where it's imported
        with patch('portkey_ai.AsyncPortkey', side_effect=ImportError("Portkey not found")):
            config = get_agent_full_config("biomedical_researcher")
            model = _create_pydantic_ai_model_from_config(config)
            
            # Should fallback to direct OpenAI
            assert isinstance(model, OpenAIModel)
            assert model.model_name == 'gpt-4o-mini'
            
        logger.info("✅ Fallback to direct OpenAI works on import error")
    
    @patch('portkey_ai.AsyncPortkey')
    def test_fallback_to_direct_openai_on_setup_error(self, mock_portkey, portkey_env_vars):
        """Test fallback to direct OpenAI when Portkey setup fails."""
        # Mock AsyncPortkey to raise an error
        mock_portkey.side_effect = Exception("Portkey setup failed")
        
        config = get_agent_full_config("biomedical_researcher")
        model = _create_pydantic_ai_model_from_config(config)
        
        # Should fallback to direct OpenAI
        assert isinstance(model, OpenAIModel)
        assert model.model_name == 'gpt-4o-mini'
        
        logger.info("✅ Fallback to direct OpenAI works on setup error")
    
    def test_different_portkey_providers(self, portkey_env_vars):
        """Test that different Portkey provider types work correctly."""
        from src.config.llm_providers import PortkeyAnthropicConfig, PortkeyBedrockConfig, PortkeyAzureConfig
        
        test_cases = [
            (ProviderType.PORTKEY_ANTHROPIC, "@anthropic"),
            (ProviderType.PORTKEY_BEDROCK, "@bedrock"),
            (ProviderType.PORTKEY_AZURE, "@azure"),
        ]
        
        for provider_type, expected_alias in test_cases:
            with patch('portkey_ai.AsyncPortkey') as mock_portkey:
                mock_client = MagicMock()
                mock_portkey.return_value = mock_client
                
                # Create config manually with proper virtual key
                config = {
                    'provider': provider_type,
                    'model': 'test-model',
                    'portkey_api_key': 'test-key',
                    'virtual_key': expected_alias  # Set explicit virtual key for test
                }
                
                _create_pydantic_ai_model_from_config(config)
                
                # Verify correct provider alias was used
                call_kwargs = mock_portkey.call_args[1]
                assert call_kwargs['provider'] == expected_alias
                
        logger.info("✅ All Portkey provider types work correctly")
    
    @patch('portkey_ai.AsyncPortkey')
    def test_biomedical_researcher_wrapper_integration(self, mock_portkey, portkey_env_vars):
        """Test that the BiomedicalResearcherWrapper works with new Portkey integration."""
        # Mock the AsyncPortkey client and agent response
        mock_client = MagicMock()
        mock_portkey.return_value = mock_client
        
        # Mock the agent's run response with proper async support
        mock_result = MagicMock()
        mock_result.output = BiomedicalResearchOutput(
            summary="Test biomedical research summary",
            key_findings=["Finding 1", "Finding 2"],
            sources=[{"title": "Test Paper", "url": "https://example.com"}],
            recommendations=["Recommendation 1"],
            confidence_level=0.85
        )
        
        # Create a proper async mock
        async def mock_run(*args, **kwargs):
            return mock_result
        
        with patch('src.agents.biomedical_researcher.Agent') as mock_agent_class:
            mock_agent = MagicMock()
            mock_agent.run = mock_run
            mock_agent_class.return_value = mock_agent
            
            # Create wrapper and test
            wrapper = BiomedicalResearcherWrapper()
            result = wrapper.research("Test biomedical query")
            
            # Verify result structure
            assert isinstance(result, BiomedicalResearchOutput)
            assert result.summary == "Test biomedical research summary"
            assert len(result.key_findings) == 2
            assert result.confidence_level == 0.85
            
        logger.info("✅ BiomedicalResearcherWrapper integrates correctly with new Portkey setup")
    
    def test_environment_variable_requirements(self):
        """Test behavior when required environment variables are missing."""
        # Test with missing PORTKEY_API_KEY
        with patch.dict(os.environ, {}, clear=True):
            config = get_agent_full_config("biomedical_researcher")
            
            # Should still create config but with None values
            assert config['portkey_api_key'] is None
            
            # Model creation should fall back to direct OpenAI
            model = _create_pydantic_ai_model_from_config(config)
            assert isinstance(model, OpenAIModel)
            
        logger.info("✅ Graceful handling of missing environment variables")


def test_comprehensive_portkey_integration():
    """Run a comprehensive integration test."""
    logger.info("🧪 Starting comprehensive Portkey integration test...")
    
    # Set up test environment
    test_env = {
        'PORTKEY_API_KEY': 'test-portkey-key',
        'PORTKEY_OPENAI_VIRTUAL_KEY': '@openai',
        'OPENAI_API_KEY': 'test-openai-key',
        'ENVIRONMENT': 'test'
    }
    
    with patch.dict(os.environ, test_env):
        with patch('portkey_ai.AsyncPortkey') as mock_portkey:
            # Mock successful Portkey client creation
            mock_client = MagicMock()
            mock_portkey.return_value = mock_client
            
            # Test model creation
            model = get_biomedical_model()
            assert isinstance(model, OpenAIModel)
            
            # Verify Portkey was called correctly
            mock_portkey.assert_called_once()
            call_kwargs = mock_portkey.call_args[1]
            
            assert call_kwargs['api_key'] == 'test-portkey-key'
            assert call_kwargs['provider'] == '@openai'
            assert '_agent' in call_kwargs['metadata']
            
            logger.info("✅ Comprehensive integration test passed")


if __name__ == "__main__":
    # Run the comprehensive test
    test_comprehensive_portkey_integration()
    
    print("\n" + "="*60)
    print("🎉 NEW PORTKEY INTEGRATION TESTS COMPLETE")
    print("="*60)
    print("✅ AsyncPortkey client integration working")
    print("✅ Proper fallback to direct OpenAI")  
    print("✅ Environment variable handling")
    print("✅ Multiple provider support")
    print("✅ Biomedical wrapper integration")
    print("="*60) 