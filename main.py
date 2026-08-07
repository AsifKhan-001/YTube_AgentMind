from src.ingestion.youtube_loader import load_youtube_transcript
from src.chunking.splitter import create_chunks
from src.embeddings.embedding_model import load_embedding_model
from src.vectorstore.faiss_store import create_vector_store
from src.retrieval.retriever import get_retriever
from src.llm.generator import build_rag_chain
from src.llm.generator_langgraph import build_rag_graph
from src.utils.timestamps import fetch_timestamps
from langchain_core.messages import ToolMessage
from src.config import URL


from langgraph.graph.message import add_messages
from langchain_core.messages import HumanMessage, BaseMessage

def main():

    url = URL

    transcript_data = load_youtube_transcript(url)
    # transcript_text = transcript_data["transcript_text"]
    # chunks = create_chunks(transcript_text)
    context_with_timestamp = fetch_timestamps(url)
    chunks = create_chunks(context_with_timestamp)
    embeddings = load_embedding_model()
    vector_store = create_vector_store(chunks,embeddings)
    retriever = get_retriever(vector_store)
    # rag_chain = build_rag_chain(retriever)      # Use any one langchain or langgraph
    rag_graph = build_rag_graph(retriever,transcript_data)

    while True:

        question = input("Ask Question: ")
        if question.lower() == "exit":
            break
        # answer_chain = rag_chain.invoke(question)
        answer_graph = rag_graph.invoke(
                {
                    "messages": [HumanMessage(content=question)],
                    
                }
            )
        # print(answer_chain)
        
        # print(answer_graph['messages'][-1].content)

        for msg in answer_graph["messages"]:
            # print("=" * 60)
            print(type(msg))

            if isinstance(msg, ToolMessage):
                print(msg.content)

            # To print the the every message like HumanMessage which is my query and ToolMessaages and AiMessgaes
            # if hasattr(msg, "content"):
            #     print(msg.content)

        


if __name__ == "__main__":
    main()