import logging
import os

from langchain_core.messages import SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI

from ddd_llm_app.config.settings import DEEPSEEK_API_KEY, DEEPSEEK_MODEL, DEEPSEEK_BASE_URL

from .base_provider import BaseProvider, PromptBuilder
from ..config import Config
from ..utils import read_file

logger = logging.getLogger(__name__)


class DeepSeekPromptBuilder(PromptBuilder):

    def __init__(self, config:Config = None):
        super().__init__(config)
        self._templ_file = None
        self._dom_desc_file = None
        self._dom_desc_text = None


    def template_file(self, templ_file: str) -> 'DeepSeekPromptBuilder':
        self._templ_file = templ_file
        return self

    def domain_description_file(self, dom_desc_file: str) -> 'DeepSeekPromptBuilder':
        self._dom_desc_file = dom_desc_file
        return self

    def domain_description_text(self, dom_desc_text: str) -> 'DeepSeekPromptBuilder':
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

        # template = read_file(tmpl_file)
        # domain_description = read_file(dom_desc_file)

        return template.format(domain_description=domain_description)







class DeepSeekProvider(BaseProvider):
    def __init__(self):
        self.llm = ChatOpenAI(
            model=DEEPSEEK_MODEL,
            openai_api_key=DEEPSEEK_API_KEY,
            max_tokens= Config.config['deepseek']['max_tokens'], #8192,
            temperature=Config.config['deepseek']['temperature'], #0.7
            base_url=DEEPSEEK_BASE_URL
        )

    def generate_completion(self, prompt: str) -> str:
        # Define system behavior and user input
        messages = [
            SystemMessage(content="You are an expert in Domain-Driven Design."),
            HumanMessage(content=prompt)
        ]

        # Generate the response
        response = self.llm.invoke(messages)
        return response.content

    def createPromptBuilder(self,config: Config = None) -> PromptBuilder:
        return DeepSeekPromptBuilder(config)

