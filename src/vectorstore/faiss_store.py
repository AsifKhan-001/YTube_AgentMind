from langchain_community.vectorstores import FAISS

def create_vector_store(chunks,embeddingmodel):

    vector_store = FAISS.from_documents(chunks,embeddingmodel)

    return vector_store