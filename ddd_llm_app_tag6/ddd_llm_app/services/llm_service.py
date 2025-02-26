from ddd_llm_app.llm_providers import LLMProviderFactory


class LLMService:
    def __init__(self):
        self.provider = LLMProviderFactory.create()

    
    def generate_completion(self, prompt: str) -> str:
        return self.provider.generate_completion(prompt)


