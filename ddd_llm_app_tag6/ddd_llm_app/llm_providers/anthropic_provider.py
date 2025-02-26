import os

from langchain_anthropic import ChatAnthropic

from ddd_llm_app.config.settings import ANTHROPIC_API_KEY, ANTHROPIC_MODEL

from .base_provider import BaseProvider, PromptBuilder
from ..config import Config
from ..utils import read_file


class AnthropicPromptBuilder(PromptBuilder):

    def __init__(self, config:Config = None):
        super().__init__(config)
        self._templ_file = None
        self._dom_desc_file = None
        self._dom_desc_text = None


    def template_file(self, templ_file: str) -> 'AnthropicPromptBuilder':
        self._templ_file = templ_file
        return self

    def domain_description_file(self, dom_desc_file: str) -> 'AnthropicPromptBuilder':
        self._dom_desc_file = dom_desc_file
        return self

    def domain_description_text(self, dom_desc_text: str) -> 'AnthropicPromptBuilder':
        self._dom_desc_text = dom_desc_text
        return self


    def build(self) -> str:

        if self._config:
            if self._templ_file:
                # tmpl_file = os.path.expanduser(self._templ_file)
                tmpl_file = os.path.realpath(os.path.expanduser(
                    os.path.join(Config.config['prompt']['template_dir'],
                                 'templates',
                                 self._templ_file
                                 )))
                print(tmpl_file)
            else:
                tmpl_file = os.path.expanduser(
                        os.path.join(Config.config['prompt']['template_dir'],
                                     'templates',
                                     Config.config['prompt']['template_file']
                                     ))
            template = read_file(tmpl_file)

            if self._dom_desc_text:
                domain_description = self._dom_desc_text
            else:
                if self._dom_desc_file.startswith("/"):
                    dom_desc_file = self._dom_desc_file
                else:
                    dom_desc_file = os.path.expanduser(
                        os.path.join(Config.config['prompt']['template_dir'],
                                     'ddd_domain',
                                     self._dom_desc_file
                                     ))
                domain_description = read_file(dom_desc_file)
        else:
            tmpl_file = os.path.expanduser(self._templ_file)
            template = read_file(tmpl_file)
            if self._dom_desc_text:
                domain_description = self._dom_desc_text
            else:
                dom_desc_file = self._dom_desc_file
                domain_description = read_file(dom_desc_file)


        return template.format(domain_description=domain_description)





class AnthropicProvider(BaseProvider):
    def __init__(self):
        self.llm = ChatAnthropic(
            model=ANTHROPIC_MODEL,
            anthropic_api_key=ANTHROPIC_API_KEY,
            max_tokens_to_sample=Config.config['anthropic']['max_tokens_to_sample'], #4096
            temperature=Config.config['anthropic']['temperature'] # 0.7
        )

    def generate_completion(self, prompt: str) -> str:
        return self.llm.invoke(prompt).content

    def createPromptBuilder(self,config: Config = None) -> PromptBuilder:
        return AnthropicPromptBuilder(config)
