from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import tempfile
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
import fal_client
from dotenv import load_dotenv
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter
from pypdf import PdfReader
from docx import Document
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from typing import Optional
import logging


load_dotenv()

app = FastAPI()

# CORS settings to allow requests from frontend
origins = [
    "https://podcast-generator-app.vercel.app/",  # Replace with your Next.js frontend URL in production
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Data model for the response data
class PodcastResponse(BaseModel):
    conversation: str
    audio_url: Optional[str] = None
    error: Optional[str] = None


# Data model for request body
class TopicPodcastRequest(BaseModel):
    topic: str


class UrlPodcastRequest(BaseModel):
    url: str
    podcast_title: str


def extract_text_from_pdf(file_path):
    """Extract text from a PDF file using pypdf."""
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text


def extract_text_from_docx(file_path):
    """Extract text from a DOCX file."""
    doc = Document(file_path)
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + '\n'
    return text


def extract_text(file_path, file_type):
    """Extract text based on file type."""
    if file_type == "pdf":
        return extract_text_from_pdf(file_path)
    elif file_type == "txt":
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    elif file_type == "docx":
        return extract_text_from_docx(file_path)
    else:
        return "Unsupported file type."


# --- Function for Generating Podcast Transcript with RAG---
def generate_podcast_transcript_with_rag(topic, text=None):

    if text:

        # Split the document into chunks
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000)
        docs = text_splitter.split_text(text)

        # Create a vector store
        vectorstore = Chroma.from_texts(
            texts=docs, embedding=GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        )

        # Create a retriever
        retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 10})

        # Initialize Gemini model (ensure API key is set)
        llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0, max_tokens=None, timeout=None)

        # Define prompt template
        system_prompt = (
            """
Create an engaging conversation between two speakers discussing the topic: {topic}, based on the provided context.

Requirements:
- Generate exactly 5 back-and-forth exchanges
- Make it natural and conversational
- Include specific details about the {topic} based on the provided context.
- Each line should start with either "Speaker 1:" or "Speaker 2:"

Here's an example of the format (but create NEW content about {topic} based on the given context, don't copy this example):
Speaker 1: [First speaker's line]
Speaker 2: [Second speaker's line]

The response of the each speaker should be at most 20 words. The conversation has to be insightful, engaging, explanatory, deep diving and educational.

It should be in the style of a podcast where one speaker slightly is more knowledgeable than the other.

You are allowed to write only in the below format. Just give the output in the below format in a single string. No additional delimiters.

The content should be explanatory, deep diving and educational.

Speaker 1: Hey, did you catch the game last night?
Speaker 2: Of course! What a match—it had me on the edge of my seat.
Speaker 1: Same here! That last-minute goal was unreal. Who's your MVP?
Speaker 2: Gotta be the goalie. Those saves were unbelievable.

Remember: Create completely new dialogue about {topic} based on the given context, don't use the above example.

\n\n
{context}
"""
        )

        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                ("human", "{input}"),
            ]
        )

       # Create and run RAG chain
        question_answer_chain = create_stuff_documents_chain(llm, prompt)
        rag_chain = create_retrieval_chain(retriever, question_answer_chain)

        response = rag_chain.invoke({"input": topic, "topic": topic})

        # Initialize Deepseek model
        deepseek_llm = ChatOpenAI(
            model="deepseek/deepseek-chat",
            openai_api_key=os.getenv("OPENROUTER_API_KEY"),
            openai_api_base="https://openrouter.ai/api/v1"
        )

         # Create a prompt for deepseek
        deepseek_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),

            ]
        )

        deepseek_chain =  deepseek_prompt | deepseek_llm

        deepseek_response = deepseek_chain.invoke({"topic": topic, "context": response["answer"]})
        return deepseek_response.content
    else:
        podcast_template = ChatPromptTemplate.from_template("""
Create an engaging conversation between two speakers discussing the topic: {topic}.

Requirements:
- Generate exactly 5 back-and-forth exchanges
- Make it natural and conversational
- Include specific details about the {topic}.
- Each line should start with either "Speaker 1:" or "Speaker 2:"

Here's an example of the format (but create NEW content about {topic}, don't copy this example):
Speaker 1: [First speaker's line]
Speaker 2: [Second speaker's line]

The response of the each speaker should be at most 20 words. The conversation has to be insightful, engaging, explanatory, deep diving and educational.

It should be in the style of a podcast where one speaker slightly is more knowledgeable than the other.

You are allowed to write only in the below format. Just give the output in the below format in a single string. No additional delimiters.

The content should be explanatory, deep diving and educational.

Speaker 1: Hey, did you catch the game last night?
Speaker 2: Of course! What a match—it had me on the edge of my seat.
Speaker 1: Same here! That last-minute goal was unreal. Who's your MVP?
Speaker 2: Gotta be the goalie. Those saves were unbelievable.

Remember: Create completely new dialogue about {topic}, don't use the above example.
""")

        llm = ChatOpenAI(
            model="deepseek/deepseek-chat",
            openai_api_key=os.getenv("OPENROUTER_API_KEY"),
            openai_api_base="https://openrouter.ai/api/v1"
        )



    chain = podcast_template | llm
    response = chain.invoke({"topic": topic})
    return response.content


# --- Function for Generating Podcast with Audio ---
def generate_podcast(topic, text=None) -> PodcastResponse:
    print(f"\n🎙️ Generating podcast transcript about: {topic}")
    print("-" * 50)

    # Get transcript first
    try:
        if text:
            transcript_result = generate_podcast_transcript_with_rag(topic, text)
        else:
            transcript_result = generate_podcast_transcript_with_rag(topic)
    except Exception as e:
        print(f"Error generating transcript: {e}")
        return PodcastResponse(conversation="", audio_url=None, error=str(e))

    print("\n✍️ Generated transcript:")
    print("-" * 50)
    print(transcript_result)

    print("\n🔊 Converting transcript to audio...")
    print("-" * 50)

    # Progress callback for fal-client
    def on_queue_update(update):
        if isinstance(update, fal_client.InProgress):
            for log in update.logs:
                print(f"🎵 {log['message']}")

    # Generate audio using fal-client
    try:
        fal_api_key = "e8efb1d2-1537-4bc5-996d-78b75a08aab2:c98b25ab01dff2d68257130e6d1b643a" #Hardcoded FAL API Key

        result = fal_client.subscribe(
            "fal-ai/playht/tts/ldm",
            {
                "input": transcript_result,
                "voices": [
                    {
                        "voice": "Jennifer (English (US)/American)",
                        "turn_prefix": "Speaker 1: ",
                    },
                    {
                        "voice": "Dexter (English (US)/American)",
                        "turn_prefix": "Speaker 2: ",
                    },
                ],
            },
            api_key=fal_api_key,
            with_logs=True,
            on_queue_update=on_queue_update,
        )

        print("\n✅ Audio generation complete!")
        print(f"🔗 Audio URL: {result['audio']['url']}")
        return PodcastResponse(conversation=transcript_result, audio_url=result['audio']['url'], error=None)

    except Exception as e:
        print(f"\n❌ Error generating audio: {str(e)}")
        return PodcastResponse(conversation=transcript_result, audio_url=None, error=str(e))


@app.post("/generate_podcast_topic", response_model=PodcastResponse)
async def create_podcast_topic(request: TopicPodcastRequest):
    openrouter_key = os.getenv("OPENROUTER_API_KEY")
    if not  openrouter_key:
        raise HTTPException(status_code=500, detail="Please set OPENROUTER_API_KEY as environment variables or in .env file.")

    os.environ["OPENROUTER_API_KEY"] = openrouter_key

    podcast_data = generate_podcast(request.topic)
    return podcast_data


@app.post("/generate_podcast_url", response_model=PodcastResponse)
async def create_podcast_url(request: UrlPodcastRequest):
    openrouter_key = os.getenv("OPENROUTER_API_KEY")
    if not openrouter_key:
        raise HTTPException(status_code=500, detail="Please set OPENROUTER_API_KEY as environment variables or in .env file.")

    os.environ["OPENROUTER_API_KEY"] = openrouter_key

    try:
        loader = WebBaseLoader(request.url)
        data = loader.load()
        text = data[0].page_content
        podcast_data = generate_podcast(request.podcast_title, text)
        return podcast_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error scraping URL or generating podcast: {str(e)}")


@app.post("/generate_podcast_document", response_model=PodcastResponse)
async def create_podcast_document(
    podcast_title: str = File(...),
    uploaded_file: UploadFile = File(...)
):
    openrouter_key = os.getenv("OPENROUTER_API_KEY")
    if not openrouter_key:
        raise HTTPException(status_code=500, detail="Please set OPENROUTER_API_KEY as environment variables or in .env file.")
    os.environ["OPENROUTER_API_KEY"] = openrouter_key
    logging.info(f"File Upload Started")

    try:
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(await uploaded_file.read())
            temp_file_path = tmp_file.name

        file_extension = uploaded_file.filename.split('.')[-1].lower()
        text = extract_text(temp_file_path, file_extension)
        if text == "Unsupported file type":
           raise HTTPException(status_code=400, detail="Unsupported file type")

        podcast_data = generate_podcast(podcast_title, text)

        os.remove(temp_file_path)
        return podcast_data

    except Exception as e:
        logging.error(f"Error in file upload", exc_info = True)
        raise HTTPException(status_code=500, detail=f"Error loading document or generating podcast: {str(e)}")
