from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound
from youtube_transcript_api._errors import TranscriptsDisabled
from urllib.parse import urlparse, parse_qs



def load_youtube_transcript(url):

    url_id = parse_qs(urlparse(url).query).get("v", [None])[0]
    

    try:
        youtube_api = YouTubeTranscriptApi()
        # transcript_list = youtube_api.fetch(url_id,languages=["hi"])

        # Transcript object
        # original_trans_list = next(iter(transcript_list))

        # print(f"\nLanguage: {transcript_list.language}")

        # original_transcript = " ".join(chunk.text for chunk in transcript_list)

        # print("\n👉 Original Transcript:\n")
        # print(original_transcript)

        # Get all available transcripts
        transcript_data = youtube_api.list(url_id)
        
        # Get the first available transcript (regardless of language)
        transcript = next(iter(transcript_data))
        
        # Fetch transcript
        transcript_list = transcript.fetch()
        
        # Convert to text
        original_transcript = " ".join(chunk.text for chunk in transcript_list)


        # English translation

        # english_trans_list = youtube_api.fetch(url_id,languages=["en"])
        # english_transcript = " ".join(chunk.text for chunk in english_trans_list)

        # print(f"\nLanguage: {english_trans_list.language}")
        # print("\n👉 English Translation:\n")
        # print(english_transcript)

        # # Hindi translation

        # hindi_trans_list = youtube_api.fetch(url_id,languages=["hi"])
        # hindi_transcript = " ".join(chunk.text for chunk in hindi_trans_list)

        # print(f"\nLanguage: {hindi_trans_list.language}")
        # print("\n👉 Hindi Translation:\n")
        # print(hindi_transcript)

    except TranscriptsDisabled:
        print("❌ Captions are disabled for this video.")


    return {
        "transcript_text": original_transcript,
        "transcript_list": transcript_list
    }

