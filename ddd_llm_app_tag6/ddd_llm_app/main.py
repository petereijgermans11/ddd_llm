import argparse
import logging
import os
import platform

from ddd_llm_app import logging_config
from ddd_llm_app.config.config import Config
from ddd_llm_app.services.ddd_tasks import DDDTasks
from ddd_llm_app.llm_providers import LLMProviderFactory
from ddd_llm_app.utils import save_text_with_timestamp

def initialize_data_dir():
    """

    :return:
    """
    os_platform = platform.system()
    if os_platform == "Darwin":
        app_data_dir = os.path.expanduser("~/ddd_llm_data")
    elif os_platform == "Linux":
        app_data_dir = '/usr/local/var/ddd_llm_data'
    elif os_platform == "Windows":
        app_data_dir = os.path.expanduser("~\\ddd_llm_data")
    else:
        raise Exception("Unsupported OS platform")
    if not os.path.exists(app_data_dir):
        os.makedirs(app_data_dir)
    print(f"Directory '{app_data_dir}' created successfully.")
    # logging(f"Directory '{app_data_dir}' created successfully.")


def main():
    """
    The main function of the script.
    :return:
    """

    print(Config.config)

    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Generate a DDD model from a domain description.")
    parser.add_argument("--file", type=str, help="Path to a file containing the domain description.", required=True)
    parser.add_argument("--outfile", type=str, help="Path to a file containing the DDD model description.",
                        required=True)
    parser.add_argument("--provider", type=str, help="The LLM provider to use.",
                        choices=["openai", "anthropic", "flant5", "deepseek"], required=False, default="openai")
    parser.add_argument("--config", type=str, help="The config file containing user config.", required=False)
    args = parser.parse_args()
    provider = args.provider or os.getenv("LLM_PROVIDER", "openai")

    if args.config:
        Config.load_user_config(args.config)
        print("User config\n")
        print(Config.config)

    # Set up the logger
    logging_config.setup_logger2()
    logger = logging.getLogger(__name__)

    # Initialize the data directory structure
    initialize_data_dir()

    # Configure the LLM provider factory
    LLMProviderFactory.config_and_create(provider)
    logger.debug(f"LLM provider configured and created: {LLMProviderFactory.provider}")

    # Create a prompt builder
    prompt_builder = LLMProviderFactory.instance.createPromptBuilder(Config)
    logger.debug(
        f"Prompt builder created: {prompt_builder.__class__.__name__}",
        )

    # Read the domain description from the file
    try:
        prompt = prompt_builder.domain_description_file(args.file).build()
        # print(f"Prompt text has been generated:\n\n {prompt}")
        # exit(0)
    except FileNotFoundError as fnfe:
        print(f"File not found: {fnfe.filename}")
        logger.error(f"File not found: {fnfe.filename}", fnfe)
        return

    # Instantiate a DDDTask object containing different types of tasks
    ddd_tasks = DDDTasks()
    logger.debug("DDDTasks object instantiated.")

    # Execute the task
    print("\nGenerating DDD model Definition...")
    logger.debug(f"Prompt text has been generated:\n\n {prompt}")
    ddd_model_definition = ddd_tasks.generate_ddd_model_definition(prompt)
    logger.debug(
        f"DDD model definition generated:\n\n {ddd_model_definition}"
    )

    # Save the DDD model definition to a file
    filepath = save_text_with_timestamp(ddd_model_definition, args.outfile)
    logger.info(
        f"DDD model definition saved to file: {filepath}",
    )


if __name__ == "__main__":
    main()
