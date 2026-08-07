from langchain_core.documents import Document

from src.ingestion.youtube_loader import load_youtube_transcript
from src.config import URL


def fetch_timestamps(URL):
    print("Timestamps saving start")
    
    transcript_data = load_youtube_transcript(URL)
    transcript_list = transcript_data["transcript_list"]

    timestamp_docs = []

    for i in range(len(transcript_list)):
        timestamp_docs.append(
            Document(
                page_content=transcript_list[i].text,
                metadata={
                    "start": round(transcript_list[i].start / 60, 2),
                    "end": round(
                        (transcript_list[i].start + transcript_list[i].duration) / 60,
                        2
                    )
                }
            )
        )


    large_trans_window = []

    for i in range(0,len(transcript_list),10):
        # print(f"i is {i}")
        page_text_content = ""
        k = i+10
        if(k>=len(transcript_list)):
            k=len(transcript_list) - 1
        for j in range(i,k):
            # print(f"j is {j}")
            page_text_content = f"{page_text_content + transcript_list[j].text} "

        large_trans_window.append(
            Document(
                page_content=page_text_content,
                metadata={
                    "start": round(transcript_list[i].start / 60, 2),
                    "end": round(
                        (transcript_list[k].start + transcript_list[k].duration) / 60,2)
                }
            )
        )

    context_with_timestamp = ""

    for doc in large_trans_window:
        # Safely extract the start and end times from the metadata dictionary
        start_time = doc.metadata.get('start', 'N/A')
        end_time = doc.metadata.get('end', 'N/A')
        
        # Format with the timestamp on top, followed by the text and a blank line
        context_with_timestamp += f"[Timestamp: {start_time} - {end_time}]\n{doc.page_content}\n\n"

    # You can print it to verify the clean output
    # print(context_with_timestamp)
        
    print('timestamps added to context_with_timestamps')

    return context_with_timestamp