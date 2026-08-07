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
from src.config import MODEL
import os


def build_topic_list():

    model = ChatOpenAI(
        api_key=os.getenv("NVIDIA_API_KEY"),
        base_url="https://integrate.api.nvidia.com/v1",
        model= MODEL
    )
    topic_prompt = PromptTemplate(
        template=TOPIC_PROMPT,
        input_variables=["transcript"]
    )

    class Topics(BaseModel):
        topics: List[str]

    original_transcript = load_youtube_transcript(URL)["transcript_text"]

    structured_model = model.with_structured_output(Topics)
    topic_chain = topic_prompt | structured_model
    result = topic_chain.invoke({
        "transcript": original_transcript
    })

    topic_list = result.topics

    return topic_list

