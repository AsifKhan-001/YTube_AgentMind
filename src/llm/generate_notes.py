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

from prompts.notes_prompts import NOTES_PROMPTS
from src.config import MODEL



def build_notes():

    text_notes = ""

    model = ChatOpenAI(
            api_key=os.getenv("NVIDIA_API_KEY"),
            base_url="https://integrate.api.nvidia.com/v1",
            model= MODEL
        )
    
    notes_Prompt_template =PromptTemplate(
        template= NOTES_PROMPTS,
        input_variables=['topic','context']
    )

    notes_chain = notes_Prompt_template | model

    return notes_chain