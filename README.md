# Podcast Generator Application
This application  allows you to generate podcasts from various sources: a topic, a URL, or a document (txt, pdf, or docx). It leverages Langchain, OpenAI's DeepSeek, Google Gemini, and fal-client for text processing, transcript generation, and audio conversion.

## Usage

1.  **Start the Backend and Frontend:** Follow the steps above to start both the backend (FastAPI) and the frontend (Next.js) servers.
2.  **Open the Frontend:** Access the frontend application in your web browser using `http://localhost:3000`
3.  **Generate Podcasts:**
    -   **Topic-Based:** Enter a topic in the text field and submit to generate a podcast based on it.
    -   **URL-Based:** Paste a URL and a podcast title and submit to generate a podcast based on the content found there.
    -   **Document-Based:** Upload a document (.txt, .pdf, or .docx) along with the desired podcast title to generate a podcast based on the document content.

4.  **Audio Playback:** Once generated, the audio output will be displayed on the frontend to play in your browser.
