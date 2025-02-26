import argparse
from flask import Flask, request, jsonify, render_template, send_from_directory
from werkzeug.utils import secure_filename
import os
import time
import threading

from ddd_llm_app.config import Config
from ddd_llm_app.llm_providers import LLMProviderFactory
from ddd_llm_app.services.ddd_tasks import DDDTasks


# Mock LLM Inference Function
def llm_inference(model_name, template_title, domain_description, max_tokens):
    # Simulate a long-running process
    # time.sleep(5)
    # return f"Mock result from {model_name} using {template_title} with max tokens {max_tokens}: {domain_description_file[:50]}..."

    LLMProviderFactory.config_and_create(model_name)
    # Config.load_user_config(args.config)
    # print(Config.config)
    if max_tokens is not None:
        Config.config['openai']['max_tokens'] = max_tokens


    print(f"DDD domain description: {domain_description}")
    prompt = (LLMProviderFactory.instance.createPromptBuilder(config=Config)
     .template_file(template_title + '.txt')
     .domain_description_text(domain_description)
     .build())

    ddd_tasks = DDDTasks()
    # Execute the task
    print("\nGenerating DDD model Definition...")
    ddd_model_definition = ddd_tasks.generate_ddd_model_definition(prompt)
    return f"Result from {model_name} using {template_title} with max tokens {max_tokens}: {ddd_model_definition}"


# Flask App Configuration
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# # Locate the templates directory relative to the package
# TEMPLATES_FOLDER = pkg_resources.resource_filename("ddd_llm_app", "templates")
# STATIC_FOLDER = pkg_resources.resource_filename("ddd_llm_app", "static")
#
# app = Flask(__name__, template_folder=TEMPLATES_FOLDER, static_folder=STATIC_FOLDER)
app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# Route for the HTML page
@app.route("/", methods=["GET"])
def index():
    TEMPLATE_DIR = os.path.realpath(os.path.expanduser(os.path.join(Config.config['prompt']['template_dir'], 'templates')))
    templates = [
        os.path.splitext(filename)[0]
        for filename in os.listdir(TEMPLATE_DIR)
        if os.path.isfile(os.path.join(TEMPLATE_DIR, filename))
    ]
    # return render_template("index.html")
    return render_template('index.html', templates=templates)

# Route to handle the form submission
@app.route("/submit", methods=["POST"])
def submit():
    # Get form data
    model_name = request.form.get("model_name")
    template_title = request.form.get("template_title")
    max_tokens = int(request.form.get("max_tokens"))
    # Handle file upload
    uploaded_file = request.files.get("domain_description")
    if not uploaded_file:
        return jsonify({"error": "No file uploaded"}), 400

    filename = secure_filename(uploaded_file.filename)
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    uploaded_file.save(file_path)

    # Read the uploaded file content
    with open(file_path, "r") as f:
        domain_description = f.read()

    # Run LLM inference
    result = llm_inference(model_name, template_title, domain_description, max_tokens)

    # Return result to client
    return jsonify({"result": result})


# Serve static files (e.g., spinner image)
@app.route("/static/<path:path>")
def serve_static(path):
    return send_from_directory("static", path)

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Generate a DDD model from a domain description.")
    parser.add_argument("--config", type=str, help="The config file containing user config.", required=False)
    args = parser.parse_args()
    Config.load_user_config(args.config)

    app.run(host="0.0.0.0", port=5000)

if __name__ == "__main__":
    main()