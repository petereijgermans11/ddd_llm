#!/usr/bin/env bash
docker run -it --env-file .env -v $(pwd):/ddd_llm_data -p 8000:8000 --rm ddd_llm ddd_llm_rag_api "$@"
