import argparse

from dotenv import load_dotenv
from langchain.chains import RetrievalQA
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from langserve import add_routes
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.schema import HumanMessage, AIMessage
import json
import asyncio
from ddd_llm_app.config import Config

load_dotenv()


# Parse command-line arguments
parser = argparse.ArgumentParser(description="ProRail OpenAI RAG API")
parser.add_argument("--config", type=str, help="The config file containing user config.", required=False)
args = parser.parse_args()


if args.config:
    Config.load_user_config(args.config)
    print("User config\n")
    print(Config.config)


# VECTOR_STORE_PATH = os.environ['VECTOR_STORE_PATH']
VECTOR_STORE_PATH = Config.config['rag_api']['vector_store_path']

embedding_model = OpenAIEmbeddings()
vector_store = FAISS.load_local(VECTOR_STORE_PATH, embedding_model, allow_dangerous_deserialization=True)

# ✅ Initialize FastAPI
app = FastAPI(title="ProRail RAG API", version="1.0")

# ✅ Store chat memory per session (temporary in-memory storage)
chat_memory_store = {}

# ✅ Create function to fetch or create session memory
def get_memory(session_id: str):
    if session_id not in chat_memory_store:
        chat_memory_store[session_id] = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    return chat_memory_store[session_id]

# ✅ Setup LLM & Conversational Chain
def create_qa_chain(session_id: str):
    memory = get_memory(session_id)
    retriever = vector_store.as_retriever(search_kwargs={"k": 5})

    return ConversationalRetrievalChain.from_llm(
        llm=ChatOpenAI(model_name="gpt-4o", temperature=0, streaming=True),
        retriever=retriever,
        memory=memory
    )

# ✅ Streaming generator function
async def stream_response(chain, question):
    async for chunk in chain.astream({"question": question}):
        if chunk and "answer" in chunk:
            yield chunk["answer"]

# ✅ Chat Endpoint (Streaming + Memory)
@app.post("/query")
async def query_rag(request: Request):
    data = await request.json()
    session_id = data.get("session_id", "default_session")
    question = data.get("question", "")

    # ✅ Create memory-aware chain
    qa_chain = create_qa_chain(session_id)

    return StreamingResponse(stream_response(qa_chain, question), media_type="text/event-stream")

# ✅ Serve LangChain chain using LangServe
add_routes(app, create_qa_chain("default_session"), path="/langchain")

# ✅ Start function for pyproject.toml
def start():
    uvicorn.run("ddd_llm_app.rag_api:app", host="0.0.0.0", port=8000, reload=True)

if __name__ == "__main__":
    start()