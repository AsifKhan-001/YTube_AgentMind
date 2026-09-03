# from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
# from langchain_core.runnables import RunnableParallel,RunnablePassthrough,RunnableLambda
# from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
# from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
# from langchain_nvidia_ai_endpoints import NVIDIAEmbeddings
from langchain_core.tools import tool
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_core.messages import HumanMessage, BaseMessage
from langgraph.prebuilt import ToolNode, tools_condition
from urllib.parse import urlparse, parse_qs
from typing import List
from pydantic import BaseModel, Field
from typing import TypedDict, Annotated
from pydantic import BaseModel
from typing import List
import os

from prompts.qa_doubt_prompts import QA_PROMPT
from src.config import URL,MODEL,MISTRALMODEL
from src.config import LLM_MODEL,TEMPERATURE
from src.utils.file_manager import create_markdown_files
from src.llm.generate_topic_list import build_topic_list
from src.ingestion.youtube_loader import load_youtube_transcript
from prompts.notes_prompts import NOTES_PROMPTS
from src.utils.file_manager import create_markdown_files
from src.llm.generate_topic_list import build_topic_list
from src.llm.generate_notes import build_notes
from src.utils.save_markdown import save_markdown
from src.utils.file_manager import create_pdf_files
from src.utils.save_markdown import save_markdown
from src.utils.save_pdf import save_pdf
from src.llm.generate_flashcards import build_flashcard

from langchain_mistralai import ChatMistralAI
from mistralai.client import Mistral

from langchain_google_genai import ChatGoogleGenerativeAI



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


def build_rag_graph(retriever,original_transcript,video_url):

    # model = ChatOllama(
    #     model= LLM_MODEL,
    #     temperature= TEMPERATURE
    # )

    # original_transcript = load_youtube_transcript(URL)["transcript_text"]
    
    
    #mistral_model
    
    # from langchain_mistralai import ChatMistralAI

    # model = ChatMistralAI(
    #     api_key=os.getenv("MISTRAL_API_KEY"),
    #     model=MISTRALMODEL,    
    #     temperature=0
    # )

    
    model = ChatGoogleGenerativeAI(
        model="gemini-3.5-flash-lite",
        google_api_key=os.getenv("GOOGLE_API_KEY"),
        temperature=0.2
    )


    # model = ChatOpenAI(
    #     api_key=os.getenv("NVIDIA_API_KEY"),
    #     base_url="https://integrate.api.nvidia.com/v1",
    #     model= MODEL
    # )

    prompt = PromptTemplate(
        template=QA_PROMPT,
        input_variables=["context", "question"]

    )
    


    class TimestampReference(BaseModel):

        start_time: int = Field(
            description="Start timestamp in seconds in the context the timestamp provided in minutes so convert it into seconds."
        )

        end_time: int = Field(
            description="End timestamp in seconds."
        )

        reason: str = Field(
            description="Why this section is relevant."
        )


    class QAResponse(BaseModel):

        answer: str = Field(
            description=(
                "A complete answer generated ONLY from the provided transcript. "
                "If the transcript is insufficient, say you don't know."
            )
        )

        timestamps: List[TimestampReference] = Field(
            default_factory=list,
            description=(
                "Relevant timestamp ranges sorted in ascending order. "
                "Return an empty list if no timestamps are useful."
            )
        )


    structured_model = model.with_structured_output(QAResponse)

    #tool for Notes:
    @tool
    def notes_tool(query: str) -> str:

        """
        use this tool when the user ask for Generate a Detailed Notes of this Video or related to that
        Get the Whole Transcript of the video and 
        that might be make the notes on the basis of the Transcript of the video and the output is the markdown texts.
        """

        print("=" * 50)
        print("NOTES TOOL CALLED")
        print("=" * 50)
        
        filename = create_markdown_files()
        topic_list = build_topic_list(original_transcript)
        notes_chain = build_notes()
        print("Notes Generation END")

        text_notes = ""

        for i in range(0,len(topic_list)):
            notes = notes_chain.invoke({
                "topic": topic_list[i],
                "context": original_transcript
            })
            note_text = notes.content if isinstance(notes.content, str) else "".join(
            part.get("text", "") if isinstance(part, dict) else str(part)
            for part in notes.content)
            text_notes += note_text + "\n\n"
            markdown_path = save_markdown(note_text,filename)
        
        pdf_path = create_pdf_files()
        try:
            save_pdf(markdown_path, pdf_path)
        except Exception as e:
            return f"Failed to generate PDF: {e}"

        return pdf_path



    @tool
    def flashcard_tool():

        """
        use this tool when the user ask for Generate a Flashcards of this Video or related to that
        Get the Whole Transcript of the video and 
        that might be make the Flashcards on the basis of the Transcript of the video and the output is the markdown texts.
        """
        # transcript = load_youtube_transcript(URL)
        # original_transcript = 

        flashcards_chain = build_flashcard()
        flashcards = flashcards_chain.invoke({
            "transcript": original_transcript
        })

        return flashcards





    
    #tool for RAG:
    @tool
    def rag_tool(query: str) -> str:

        """
        Retriever relevant information from the pdf document.
        Use this tool when the user asks factual / conceptual questions,doubts and about Timestamps
        that might be answered from the stored documents.
        """
        # url_id = parse_qs(urlparse(URL).query).get("v", [None])[0]    #Its use for when you run on terminal
        url_id = parse_qs(urlparse(video_url).query).get("v", [None])[0]     #its for the Backend URL given by user

        result = retriever.invoke(query)

        context_text = "\n\n".join(doc.page_content for doc in result)
        # metadata = [doc.metadata for doc in result]

        chain = prompt | structured_model

        response = chain.invoke({

            "context": context_text,
            "question": query,
        })
        
        answer = response.answer
        answer += "\n\n***Video Timestamps Links***\n"

        def format_timestamp(total_seconds: int) -> str:       #its just help us to convert a time in second to proper order like 345 sec then 05:75
            hours, remainder = divmod(total_seconds, 3600)
            minutes, seconds = divmod(remainder, 60)

            if hours > 0:
                return f"{hours}:{minutes:02}:{seconds:02}"
            else:
                return f"{minutes:02}:{seconds:02}"

        links = []
        
        for ts in response.timestamps:

            links.append({
                "start_time": ts.start_time,
                "end_time": ts.end_time,
                "reason": ts.reason,
                "url": f"https://www.youtube.com/watch?v={url_id}&t={ts.start_time}s"
            })


            start = format_timestamp(ts.start_time)
            end = format_timestamp(ts.end_time)
            answer += (
                f"\n• {ts.reason}\n"
                f" - {start} - {end}\n"
                f"https://www.youtube.com/watch?v={url_id}&t={ts.start_time}s"
                )
            

        


        #Debug:
        print("===========================links print==========================")
        for link in links:

            
            # answer += (
            # f"\n• {link['reason']}\n"
            # f" - {start} - {end}\n"
            # f"\n{link['url']}\n"
            # )
            
            # print(link['"start_time"'])
            print(link['reason'])
            print(link['url'])
            

        # return {
        #     "answer": response.answer,
        #     "timestamps": response.timestamps,
        #     "links": links
        # }

        return answer


    

    tools = [rag_tool,notes_tool,flashcard_tool]
    model_with_tools = model.bind_tools(tools)

    class ChatState(TypedDict):
        messages: Annotated[list[BaseMessage], add_messages]

    def chat_node(state: ChatState):

        messages = state['messages']
        response = model_with_tools.invoke(messages)

        return {'messages':[response]}

    tool_node = ToolNode(tools)

    graph = StateGraph(ChatState)

    graph.add_node('chat_node',chat_node)
    graph.add_node('tools',tool_node)

    graph.add_edge(START,'chat_node')
    graph.add_conditional_edges('chat_node',tools_condition)
    graph.add_edge('tools','chat_node')

    rag_graph = graph.compile()
    # result = rag_graph.invoke(
    #     {
    #         "messages": [HumanMessage(content=question)]
    #     }
    # )
    return rag_graph
