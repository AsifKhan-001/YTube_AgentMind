from langchain_core.prompts import PromptTemplate
from langchain_core.prompts import ChatPromptTemplate


TOPIC_PROMPT = """
You are an expert educational content analyst and curriculum designer.

Your task is to analyze the lecture transcript and extract a HIGHLY GRANULAR list of every single teachable topic. 

=========================
IMPORTANT LANGUAGE INSTRUCTIONS (STRICT):
=========================
- The transcript may be written in ANY language but you need to Give the all kind of Respone Only in English Language.
- You must internally translate everything to English.
- ALWAYS return the final topics in 100% professional, standard English.
- NEVER output any transliterated words or original language vocabulary.
- Do not mix languages. The output must be purely English.

=========================
TOPIC EXTRACTION RULES (STRICT):
=========================
1. BE EXHAUSTIVE: This is a long lecture. Extract EVERY specific concept, method, technique, framework, and theory. 
2. DO NOT GROUP: Do not merge distinct concepts. Every specific mechanism, step, or sub-topic must be extracted as its own separate topic But if a topic is short or Easily merge to the other topics then merge it with other most related topic.
3. VOLUME EXPECTATION: For long transcripts, you MUST extract approx 10 main most relevant topics to the video transceipt if need then increase the topic but not more try to merge most related topic and make it one most relevant topic.
4. NAMING CONVENTION: Use precise, dense technical names. Topic names MUST be between 2 and 7 words long. Do not use full sentences.
5. TEACHABILITY TEST: Only extract a topic if there is enough context in the transcript to write detailed notes about it. Do not extract passing mentions.
6. AVOID REDUNDANCY: If a topic is discussed multiple times, extract it only once when it is primarily taught. Do not list the same concept twice.
7. ORDER: Return topics in the exact chronological order they first appear in the transcript.
8. EXCLUSIONS: Ignore greetings, Q&A that goes off-topic, sponsor messages, general examples, and motivational talk.

BAD EXAMPLES (Too Broad or Too Long):
- AI
- understanding how loops work in python programming
- chatgpt examples

GOOD EXAMPLES (Specific & Granular):
- Retrieval-Augmented Generation (RAG) Architecture
- LangChain Expression Language (LCEL)
- Multi-head Attention Mechanism
- Similarity Search in ChromaDB

Transcript:
{transcript}
"""

