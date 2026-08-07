from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableParallel,RunnablePassthrough,RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
from langchain_nvidia_ai_endpoints import NVIDIAEmbeddings
import os

from prompts.qa_doubt_prompts import QA_PROMPT
from src.config import LLM_MODEL,TEMPERATURE

load_dotenv()

def format_docs(retriever_docs):
    # print("\n========== RETRIEVED DOCS ==========")
    # print("Number of docs:", len(retriever_docs))

    # for i, doc in enumerate(retriever_docs):
    #     print(f"\nDoc {i+1}:")
    #     print(doc.page_content[:500])

    context_text = "\n\n".join(doc.page_content for doc in retriever_docs)

    # print("\nContext Length:", len(context_text))
    # print("===================================\n")

    return context_text

def build_rag_chain(retriever):

    # model = ChatOllama(
    #     model= LLM_MODEL,
    #     temperature= TEMPERATURE
    # )

    model = ChatOpenAI(
        api_key=os.getenv("NVIDIA_API_KEY"),
        base_url="https://integrate.api.nvidia.com/v1",
        model="nvidia/nemotron-3-ultra-550b-a55b"
    )

    prompt = PromptTemplate(
        template=QA_PROMPT,
        input_variables=["context", "question"]

)

    parser = StrOutputParser()

    parallel_chain  = RunnableParallel({
    'context':retriever | RunnableLambda(format_docs),
    'question':RunnablePassthrough()
    })

    main_chain = parallel_chain | prompt | model | parser

    return main_chain


