from prompts.flashcard_prompt import FLASHCARD_PROMPT
from src.config import MODEL

from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
import os


def build_flashcard():

    model = ChatOpenAI(
        api_key=os.getenv("NVIDIA_API_KEY"),
        base_url="https://integrate.api.nvidia.com/v1",
        model= MODEL
    )

    flashcard_prompt = PromptTemplate(
        template= FLASHCARD_PROMPT,
        input_variables= ['transcript']
    )

    parser = StrOutputParser()

    flashcard_chain = flashcard_prompt | model | parser

    return flashcard_chain
