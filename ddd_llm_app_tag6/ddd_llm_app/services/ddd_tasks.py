from ddd_llm_app.services.llm_service import LLMService



class DDDTasks:
    def __init__(self):
        self.llm_service = LLMService()


    def generate_ddd_model_definition(self, prompt: str) -> str:
        return self.llm_service.generate_completion(prompt)
