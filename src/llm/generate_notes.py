from pydantic import BaseModel
from typing import List
from langchain_core.prompts import PromptTemplate
from langchain_core.prompts import ChatPromptTemplate
from prompts.topic_prompts import TOPIC_PROMPT
from src.ingestion.youtube_loader import load_youtube_transcript
from src.config import URL
from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableParallel,RunnablePassthrough,RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
import os
from langchain_mistralai import ChatMistralAI
from mistralai.client import Mistral

from langchain_google_genai import ChatGoogleGenerativeAI


from prompts.notes_prompts import NOTES_PROMPTS
from src.config import MODEL,MISTRALMODEL



def build_notes():
    print("Notes Generation Start")

    text_notes = ""

    # model = ChatMistralAI(
    #     api_key=os.getenv("MISTRAL_API_KEY"),
    #     model=MISTRALMODEL,    
    #     temperature=0
    # )


    # model = ChatOpenAI(
    #     api_key=os.getenv("NVIDIA_API_KEY"),
    #     base_url="https://integrate.api.nvidia.com/v1",
    #     model= MODEL
    # )

    model = ChatGoogleGenerativeAI(
        model="gemini-3.5-flash-lite",
        google_api_key=os.getenv("GOOGLE_API_KEY"),
        temperature=0.2
    )

    
    notes_Prompt_template =PromptTemplate(
        template= NOTES_PROMPTS,
        input_variables=['topic','context']
    )

    notes_chain = notes_Prompt_template | model

    return notes_chain