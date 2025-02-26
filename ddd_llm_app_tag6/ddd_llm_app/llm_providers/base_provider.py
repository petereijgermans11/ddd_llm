from abc import ABC, abstractmethod
from typing import Type

from ddd_llm_app.config import Config


class PromptBuilder(ABC):

    def __init__(self, config: Config = None):
        self._config = config

    @abstractmethod
    def template_file(self, filename: str) -> 'PromptBuilder':
        pass

    @abstractmethod
    def domain_description_file(self, dom_desc_text: str) -> 'PromptBuilder':
        pass

    @abstractmethod
    def domain_description_text(self, dom_desc_text: str) -> 'PromptBuilder':
        pass

    @abstractmethod
    def build(self) -> str:
        pass


class BaseProvider(ABC):
    @abstractmethod
    def generate_completion(self, prompt: str) -> str:
        """Generates a text completion based on the given prompt."""
        pass

    @abstractmethod
    def createPromptBuilder(self,config: Type[Config] = None) -> PromptBuilder:
        pass