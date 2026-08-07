from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.config import CHUNK_SIZE,CHUNK_OVERLAP

def create_chunks(transcript_text):

    splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE,chunk_overlap=CHUNK_OVERLAP)
    chunks = splitter.create_documents([transcript_text])

    return chunks