from langchain_ollama import OllamaEmbeddings
from langchain_nvidia_ai_endpoints import NVIDIAEmbeddings
from dotenv import load_dotenv
import os

load_dotenv()

def load_embedding_model():
    # embeddingmodel = OllamaEmbeddings(
    # model = "embeddinggemma:latest"
    # )

    embeddingmodel = NVIDIAEmbeddings(
    model="nvidia/llama-nemotron-embed-1b-v2",
    api_key=os.getenv("NVIDIA_API_KEY"),
    )


    return embeddingmodel