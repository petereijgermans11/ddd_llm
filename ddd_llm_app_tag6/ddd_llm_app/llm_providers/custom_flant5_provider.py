import os

from transformers import T5Tokenizer, T5ForConditionalGeneration

from ddd_llm_app.config.settings import CUSTOM_PROVIDER_MODEL
from ddd_llm_app.llm_providers.base_provider import BaseProvider, PromptBuilder
from ..config import Config
from ..utils import read_file


class CustomFlant5PromptBuilder(PromptBuilder):

    def __init__(self, config:Config = None):
        super().__init__(config)
        self._templ_file = None
        self._dom_desc_file = None
        self._dom_desc_text = None


    def template_file(self, templ_file: str) -> 'CustomFlant5PromptBuilder':
        self._templ_file = templ_file
        return self

    def domain_description_file(self, dom_desc_file: str) -> 'CustomFlant5PromptBuilder':
        self._dom_desc_file = dom_desc_file
        return self

    def domain_description_text(self, dom_desc_text: str) -> 'CustomFlant5PromptBuilder':
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


class CustomFLANProvider(BaseProvider):
    def __init__(self):
        model_path = CUSTOM_PROVIDER_MODEL
        self.tokenizer = T5Tokenizer.from_pretrained(model_path)
        self.model = T5ForConditionalGeneration.from_pretrained(model_path)

        self.max_input_length = Config.config['custom_provider']['max_input_length'] #512
        self.max_output_length = Config.config['custom_provider']['max_output_length'] #512

    def _chunk_text(self, text: str, max_length: int):
        tokens = self.tokenizer(text, return_tensors="pt", truncation=False)["input_ids"][0]
        return [
            tokens[i: i + max_length]
            for i in range(0, len(tokens), max_length)
        ]

    def generate_response(self, prompt: str) -> str:
        chunks = self._chunk_text(prompt, self.max_input_length)
        responses = []

        for chunk in chunks:
            input_ids = chunk.unsqueeze(0)  # Add batch dimension
            outputs = self.model.generate(
                input_ids,
                max_length=self.max_output_length,
                num_beams=5,
                early_stopping=True
            )
            responses.append(self.tokenizer.decode(outputs[0], skip_special_tokens=True))

        return " ".join(responses)

    def generate_completion(self, prompt: str) -> str:
        """Generates a text completion based on the given prompt."""
        return self.generate_response(prompt)

    def createPromptBuilder(self,config: Config = None) -> PromptBuilder:
        return CustomFlant5PromptBuilder(config)