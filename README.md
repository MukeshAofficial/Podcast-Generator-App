# Podcast Generator

This application allows you to generate podcasts from various sources: a topic, a URL, or a document (txt, pdf, or docx). It leverages Langchain, OpenAI's DeepSeek, Google Gemini, and `fal-client` for text processing, transcript generation, and audio conversion.

## Features

*   **Topic-Based Podcasts:** Generate a podcast transcript and audio based on a user-provided topic.
*   **URL-Based Podcasts:** Scrape content from a URL and generate a podcast based on the scraped content.
*   **Document-Based Podcasts:** Upload a document (txt, pdf, or docx) and generate a podcast based on the document's content.
*   **Conversational Style:** The generated podcasts use a conversational format between two speakers, making them engaging and informative.
*   **RAG (Retrieval-Augmented Generation):** Uses RAG for more context-aware podcast generation.
*   **Audio Output:** Provides a playable audio output in the app.

## Architecture

This application is built using a **Next.js** frontend and a **FastAPI** backend.

*   **Frontend (Next.js):** Handles the user interface, form submissions, and display of generated content and audio.
*   **Backend (FastAPI):** Handles the core logic of podcast generation, utilizing Langchain, LLMs (DeepSeek, Gemini), `fal-client`, and data processing.

## Setup

### Prerequisites

*   **Node.js and npm (or yarn)**: Ensure you have Node.js and npm (or yarn) installed for the Next.js frontend.
*   **Python 3.7+:** Ensure you have Python installed for the FastAPI backend.

### Installation

1.  **Clone the repository:**

    ```bash
    git clone [<repository_url>](https://github.com/MukeshAofficial/Podcast-Generator-App.git)
    cd podcast-generator
    ```

2.  **Backend Setup (FastAPI):**

    a. Navigate to the backend directory:

    ```bash
    cd backend
    ```

    b. Install dependencies using Pip(recommended):



    or using pip

    ```bash
    pip install -r requirements.txt
    ```

    c. Create a `.env` file in the `backend` directory.

    d. Add the following environment variables to the `.env` file:
        ```
        FAL_KEY="your_fal_key"
        OPENROUTER_API_KEY="your_openrouter_api_key"
        GOOGLE_API_KEY="your_google_api_key"
        ```

        Replace `"your_fal_key"`, `"your_openrouter_api_key"`, and `"your_google_api_key"` with your actual API keys.

        *   You can find your `fal-client` API key on the [Fal.ai dashboard](https://fal.ai).
        *   For `OPENROUTER_API_KEY`, you need to register on [openrouter.ai](https://openrouter.ai/) and generate an API key.
        *    `GOOGLE_API_KEY`

3.  **Frontend Setup (Next.js):**

    a. Navigate to the frontend directory:

    ```bash
    cd ../frontend
    ```

    b. Install dependencies:

    ```bash
    npm install
    # or
    yarn install
    ```

  


## Running the Application

1.  **Start the Backend (FastAPI):**

    a.  Navigate to the `backend` directory if you're not already there:

        ```bash
        cd backend
        ```
    b. Run the FastAPI application using uvicorn:
    ```bash
       uvicorn main:app --reload
    ```

    This will start the server on `http://127.0.0.1:8000` or `http://localhost:8000`. The `--reload` flag will restart the server on code changes.

2.  **Start the Frontend (Next.js):**

    a. Navigate to the `frontend` directory:
    ```bash
    cd ../frontend
    ```

    b. Run the Next.js application:
    ```bash
    npm run dev
    # or
    yarn dev
    ```
    This will launch the app in your default web browser at `http://localhost:3000`

## Usage

1.  **Navigate to Different Sections:** Use the navigation bar to switch between "Topic-Based Podcast", "URL-Based Podcast", and "Document-Based Podcast".

2.  **Topic-Based Podcast:**
    *   Enter a topic in the text input field.
    *   Click the "Generate Podcast" button.
    *   The app will display the generated transcript and audio output.

3.  **URL-Based Podcast:**
    *   Enter a URL to scrape content from.
    *   Enter a title for the podcast.
    *   Click the "Generate Podcast from URL" button.
    *   The app will display the generated transcript and audio output.

4.  **Document-Based Podcast:**
    *   Upload a document (txt, pdf, or docx) using the file uploader.
    *   Enter a title for the podcast.
    *   Click the "Generate Podcast from Document" button.
    *   The app will display the generated transcript and audio output.

5. **Audio Output:** The app provides a playable audio output

