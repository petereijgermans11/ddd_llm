from ddd_llm_app.config.settings import LLM_PROVIDER
from ddd_llm_app.llm_providers.anthropic_provider import AnthropicProvider
from ddd_llm_app.llm_providers.base_provider import BaseProvider
from ddd_llm_app.llm_providers.custom_flant5_provider import CustomFLANProvider
from ddd_llm_app.llm_providers.openai_provider import OpenAIProvider
from ddd_llm_app.llm_providers.deepseek_provider import DeepSeekProvider



class LLMProviderFactory:
    provider = None
    instance: BaseProvider = None
    # @staticmethod
    @classmethod
    def create(cls):
        if cls.instance is not None:
            return cls.instance

        if LLMProviderFactory.provider.lower() == "openai":
            cls.instance = OpenAIProvider()
            return cls.instance
        elif LLMProviderFactory.provider.lower() == "anthropic":
            cls.instance = AnthropicProvider()
            return cls.instance
        elif LLMProviderFactory.provider.lower() == "flant5":
            cls.instance = CustomFLANProvider()
            return cls.instance
        elif LLMProviderFactory.provider.lower() == "deepseek":
            cls.instance = DeepSeekProvider()
            return cls.instance
        else:
            raise ValueError(f"Unsupported LLM provider: {LLM_PROVIDER}")

    @classmethod
    # @staticmethod
    def configure(cls, provider: str):
        if (provider.lower() == "openai" or provider.lower() == "anthropic" or
                provider.lower() == "flant5" or provider.lower() == "deepseek"):
            cls.provider = provider
        else:
            raise ValueError(f"Unsupported LLM provider: {LLM_PROVIDER}")

    @classmethod
    def config_and_create(cls, provider: str):
        cls.configure(provider)
        return cls.create()
