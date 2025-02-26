# Domain Driven Development with LLM: App 

## Installation and use only
If you only want to install the application for usage and testing, follow the steps below.

Clone the repo to a location on your computer:
````
git clone https://github.com/uwieske/ddd_llm_app.git
````

Cd into the repo and in the root directory run the following command:
````
./build_ddd_llm.sh
````
**Note:** if you get an error when running the above script, you might probably need to make the file executable with this command:
````
chmod +x build_ddd_llm.sh
````

Verify whether a new Docker image has been created on your machine.
The application will run in container based on this image.


You will probably be setting different/multiple environment variables. A clean way to pass your environment variables is to use the `.env`, where environment variables can be listed in this file.

Create a file `.env` relative to the `run_ddd_llm_app.sh` script and put your environment variable in the `.env` file.

````.env
OPENAI_API_KEY=<paste here your API KEY>
ANTHROPIC_API_KEY=<paste here your API KEY>
LOG_LEVEL=DEBUG
# and other environment variables below...
```` 

To run the application use the script below:

**Mind you:** the script assumes that your input files are placed relative to the file location of `run_ddd_llm.sh`.

If you want your LLM Provider to be **OpenAI**:

````
./run_ddd_llm.sh --file=<filename containing the domain description> --outfile=<the output filename where the generated DDD-model will be saved> --provider=openai --config=user-config.yaml
````

Example:
````
./run_ddd_llm.sh --file=prorail_domain.md --outfile=examples/prorail_domain_response.md --provider=openai --config=user-config.yaml
````


If you want your LLM Provider to be **Anthropic**:

Example:
````
./run_ddd_llm.sh --file=<filename containing the domain description> --outfile=<the output filename where the generated DDD-model will be saved> --provider=anthropic --config=user-config.yaml
````

If you want the custom FLAN-T5 LLM Provider:

Example:
````
./run_ddd_llm.sh --file=<filename containing the domain description> --outfile=<the output filename where the generated DDD-model will be saved> --provider=flant5 --config=user-config.yaml
````

**Note:** if you get an error when running the above script, you might probably need to make the file executable with this command:
````
chmod +x run_ddd_llm.sh
````

**Note**: All generated files will be appended with a timestamp, e.g. `generated_output.md` `-->` `generated_output_20250112_224434.md`


### Optional: configuration and logging

You passed at commandline the `--config=user-config-yaml` option. 
You can change some configurable items of the application such as:
- Prompt specific configuration: template_file directory where you have stored your prompt templates and the filename of your own prompt template_file definition.  
- LLM parameters like the max_tokens and temperature.
- Logging items like your logfilename, log level for the defined loggers, etc. 

An example of a user-config.yaml file where default values of some configuration parameters have been overridden:

````yaml
# The default Prompt template_file configuration values are included in comments below.
#
#prompt:
#  template_dir: ~/ddd_llm_data
#  template_file: ddd_prompt.txt
#
# The Prompt Template Configuration overrides:
prompt:
  template_dir: ./
  template_file: ddd_prompt.txt

# The default LLM configuration values are included in comments below.
#
#openai:
#  max_tokens: 8192
#  temperature: 0.7
#anthropic:
#  max_tokens_to_sample: 4096
#  temperature: 0.7
#custom_provider:
#  max_input_length: 512
#  max_output_length: 512

# LLM Configuration overrides
openai:
  max_tokens: 16384

# The default Logging configuration values are included in comments below.
#
#logging:
#  version: 1
#  formatters:
#    simple:
#      format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
#    detailed:
#      format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
#
#  handlers:
#    consoleHandler:
#      class: logging.StreamHandler
#      level: INFO
#      formatter: detailed
#      stream: ext://sys.stdout
#    fileHandler:
#      class: logging.FileHandler
#      level: INFO
#      formatter: detailed
#      filename: ddd_llm_app.log
#
#  loggers:
#    __main__:
#      level: INFO
#      handlers: [ consoleHandler, fileHandler ]
#      propagate: false
#    ddd_llm_app.llm_providers.openai_provider:
#      level: INFO
#      handlers: [ consoleHandler, fileHandler ]
#      propagate: false
#  root:
#    level: INFO
#    handlers: [ consoleHandler, fileHandler ]
#
# The Logging Configuration overrides below:
logging:
  # Handlers
  handlers:
    consoleHandler:      
      level: DEBUG      
    fileHandler:      
      level: DEBUG
      filename: ddd_llm_app.log
  # Loggers - here you will configure the logger (log level)
  loggers:
    __main__:
      level: DEBUG
    ddd_llm_app.llm_providers.openai_provider:
      level: DEBUG
  # The root logger
  root:
    level: INFO

````


**----- END instructions: Installation and use only -----**


## Web interface for DDD with LLM

If you want to run the DDD with LLM continuously, you may want to run it as a webserver.

Make sure you have built an image above. 
There is a script which starts an in-container webserver.
Use the `docker-web-user-config.yaml` configuration with the web variant.
You may want to change some values if needed.
Put your template files `<some_template_name>.txt` in the templates directory.
Make sure you refresh your web page in order to trigger a fetch which pick up the change in the templates directory, which consequently updates the option's list of the templates dropdown control in your web page. 

In the root directory of your git repository run:

````
./run_ddd_llm_web.sh --config=docker-web-user-config.yaml
````
#### Note: `prompt.template_dir` in the config file defines the base directory for the `templates` directory. The `templates` directory is the location where template files are stored.

````
<promtp.templates_dir>+
                      |
                      |
                      +---templates--+
                      |              |
                      |              +---<some_template_name>.txt
                      |              |
                      |              +---<other_template_name>.txt
                      |              |
                      |              +---...
                      |
                      |
                      |
                      +---ddd_domain-+
                                     |
                                     +--<ddd_description>
                                     |
                                     +--...
                                                          
````

## Development and Programming


### Conda
**Assumption**:

It is assumed that you have already Conda installed on your machine.
If this is not the case, install Conda either through Miniconda or Anaconda.
Miniconda is the preferred way of installing Conda, since installing Anaconda would bring in many other features which is not nessesary for this development.


Create a new Conda environment named `ddd-ll-app` with Python version 3.12:

````
conda create -n ddd-ll-app python=3.12
````

To activate this environment:
````
conda activate ddd-ll-app
````

To deactivate this environment when you are in the environment:
````
conda deactivate
````


### Dependencies
Make sure you are already in the environment before proceeding.

````
pip install -r requirements.txt
````

### Configuration

#### OPENAI API
Create `.env` file in your project dir root.

Add environment variables (*name=value*) to the file.

For your OPENAI API key, add the following entry to `.env` file: 
````
OPENAI_API_KEY=<your API KEY from OPENAI>
````

## Chatbot: ProRail
You can chat with the chatbot and ask questions about ProRail's business activity.
However, currently the bot has mostly knowledge about the business on strategic level.

1. Run the LLM OpenAI/RAG API server as a Docker container
2. Run the frontend chatbot user interface locally on your host.

*Assumptions:*

- At this point it is assumed that you have already built an image.
- You have already created a `.env` file containing the necessary API KEYs.

Make sure you have changed directory to the project's root directory before you proceed.

### Run the LLM OpenAI/RAG API server
````
./run_ddd_llm_rag_api.sh --config=docker-web-user-config.yaml
````

### Run the frontend chatbot user interface
````
./run_chat_ui.sh
````