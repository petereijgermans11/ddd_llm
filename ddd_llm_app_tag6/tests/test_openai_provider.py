import os.path

import pytest

from ddd_llm_app.config import Config
from ddd_llm_app.llm_providers import LLMProviderFactory

@pytest.fixture
def configuration():
    Config.load_user_config('test-user-config.yaml')
    return Config

@pytest.fixture
def instance_openai_llmprovider():
    LLMProviderFactory.config_and_create('openai')
    return LLMProviderFactory.instance

def test_builder(configuration, instance_openai_llmprovider):

    prompt_builder = instance_openai_llmprovider.createPromptBuilder(config=configuration)
    prompt = (prompt_builder
              .domain_description_file('test_dom_desc_1.txt')
              .build())
    assert prompt == 'abc\nxyz'

def test_builder_with_template_override(configuration, instance_openai_llmprovider):

    prompt_builder = instance_openai_llmprovider.createPromptBuilder(config=configuration)
    prompt = (prompt_builder
              .template_file('test_1.txt')
              .domain_description_file('test_dom_desc_1.txt')
              .build())
    assert prompt == 'rst\nxyz'

def test_builder_with_template_override_and_abs_path_dom_desc_file(configuration, instance_openai_llmprovider):

    rel_filepath = 'test_dom_desc_1.txt'
    abs_path_dom_desc_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'ddd_domain', rel_filepath)

    prompt_builder = instance_openai_llmprovider.createPromptBuilder(config=configuration)
    prompt = (prompt_builder
              .template_file('test_1.txt')
              .domain_description_file(abs_path_dom_desc_file)
              .build())
    assert prompt == 'rst\nxyz'

def test_builder_with_template_override_and_dom_desc_text(configuration, instance_openai_llmprovider):

    rel_filepath = 'test_dom_desc_1.txt'
    abs_path_dom_desc_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'ddd_domain', rel_filepath)

    prompt_builder = instance_openai_llmprovider.createPromptBuilder(config=configuration)
    prompt = (prompt_builder
              .template_file('test_1.txt')
              .domain_description_text('ggg')
              .build())
    assert prompt == 'rst\nggg'

def test_builder_with_no_config(configuration, instance_openai_llmprovider):
    rel_filepath_templ_file = 'test_1.txt'
    abs_path_templ_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'templates',
                                          rel_filepath_templ_file)
    rel_filepath_dom_desc = 'test_dom_desc_1.txt'
    abs_path_dom_desc_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'ddd_domain', rel_filepath_dom_desc)

    prompt_builder = instance_openai_llmprovider.createPromptBuilder()
    prompt = (prompt_builder
              .template_file(abs_path_templ_file)
              .domain_description_file(abs_path_dom_desc_file)
              .build())
    assert prompt == 'rst\nxyz'