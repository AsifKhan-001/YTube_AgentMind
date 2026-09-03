from fastapi import APIRouter, Depends
from langchain_core.messages import HumanMessage, ToolMessage

from .. import models, schemas, auth

from src.ingestion.youtube_loader import load_youtube_transcript
from src.chunking.splitter import create_chunks
from src.embeddings.embedding_model import load_embedding_model
from src.vectorstore.faiss_store import create_vector_store
from src.retrieval.retriever import get_retriever
from src.llm.generator_langgraph import build_rag_graph

router = APIRouter(prefix="/chat", tags=["chat"])

# Cache one built graph per video so we don't re-embed on every message
_graph_cache: dict = {}

def _get_or_build_graph(youtube_url: str):
    if youtube_url in _graph_cache:
        return _graph_cache[youtube_url]

    transcript_data = load_youtube_transcript(youtube_url)
    chunks = create_chunks(transcript_data["transcript_text"])
    embeddings = load_embedding_model()
    vector_store = create_vector_store(chunks, embeddings)
    retriever = get_retriever(vector_store)

    graph = build_rag_graph(retriever, transcript_data["transcript_text"], youtube_url)
    _graph_cache[youtube_url] = graph
    return graph


@router.post("/ask", response_model=schemas.ChatResponse)
def ask(request: schemas.ChatRequest, current_user: models.User = Depends(auth.get_current_user)):
    graph = _get_or_build_graph(request.youtube_url)
    result = graph.invoke({"messages": [HumanMessage(content=request.message)]})

    raw_answer = result["messages"][-1].content
    final_answer = raw_answer if isinstance(raw_answer, str) else "".join(
        part.get("text", "") if isinstance(part, dict) else str(part)
        for part in raw_answer
    )
    response = schemas.ChatResponse(answer=final_answer)

    # Walk any ToolMessages to see if notes_tool or flashcard_tool fired
    for msg in result["messages"]:
        if not isinstance(msg, ToolMessage):
            continue
        content = msg.content

        if isinstance(content, str) and content.endswith(".pdf"):
            # See Step 8 (static files) for why this URL works even though
            # `content` is a path on YOUR disk, not the user's.
            filename = content.split("/")[-1]
            response.pdf_download_url = f"/files/pdf/{filename}"

        elif isinstance(content, list):  # flashcard_tool's output
            response.flashcards = content

    return response