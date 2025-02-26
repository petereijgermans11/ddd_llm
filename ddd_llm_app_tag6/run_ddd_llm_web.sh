#!/usr/bin/env bash
#docker run -it -e OPENAI_API_KEY="$OPENAI_API_KEY" -e ANTHROPIC_API_KEY="$ANTHROPIC_API_KEY" -e LOG_LEVEL="$LOG_LEVEL" -v $(pwd):/ddd_llm_data --rm ddd_llm ddd_llm_app "$@"
docker run -it --env-file .env -v $(pwd):/ddd_llm_data -p 5000:5000 --rm ddd_llm ddd_llm_web "$@"
