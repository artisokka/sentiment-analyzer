# README: Sentiment Analyzer

Analyzes and categorizes movie reviews as either positive or negative. Uses either a DistilBERT model that has been fine-tuned with an IMDB sentiment analysis dataset or stock Llama 3.

This project was bootstrapped with [Create React App](https://github.com/facebook/create-react-app).

## About the project

This project consists of a React-based frontend and a FastAPI backend for sentiment analysis.

## Project Structure

```bash
sentiment-analyzer/
├── api-backend/
│   └── api-backend.py       # FastAPI backend API
├── public/
│   └── ...                   # Public assets for React app
├── src/
│   ├── App.js                # Main React component
│   ├── SentimentAnalyzer.js  # Sentiment analysis component
│   ├── index.js              # React entry point
│   ├── ...                   # Other React components and files
├── package.json              # Node.js project dependencies
├── package-lock.json         # Lock file for npm dependencies
└── README.md                 # This file
```

## Backend (FastAPI)

The backend API is built using FastAPI and is located in the `api-backend/api-backend.py` file.

### Setup

1.  **Navigate to the backend directory:**
    ```bash
    cd api-backend
    ```
2.  **Create a virtual environment (recommended):**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On macOS/Linux
    venv/Scripts/activate     # On Windows
    ```
3.  **Install dependencies:**
    ```bash
    pip install fastapi uvicorn transformers pydantic groq python-dotenv
    ```
4.  **Set your Groq API key:**
    * Create a `.env` file in the `api-backend` directory.
    * Add your Groq API key: `GROQ_API_KEY=your_groq_api_key`
5.  **Run the API:**
    ```bash
    uvicorn api-backend:app --reload
    ```
    The API will be available at `http://127.0.0.1:8000`.

### API Endpoints

* **`POST /analyze/`**: Analyzes the sentiment of a given text.
    * **Request Body:**
        ```json
        {
          "text": "Your text here",
          "model": "custom" or "llama"
        }
        ```
    * **Response Body:**
        ```json
        {
          "sentiment": "positive" or "negative",
          "confidence_score": 0.0 - 1.0
        }
        ```

## Frontend (React)

The frontend is a React application that provides a user interface for sentiment analysis.

### Setup

1.  **Navigate to the project's root directory:**
    ```bash
    cd .. #if currently in api-backend directory
    ```
2.  **Install dependencies:**
    ```bash
    npm install
    ```
3.  **Run the React application:**
    ```bash
    npm start
    ```
    The application will be available at `http://localhost:3000`.

### Usage

1.  Enter the text you want to analyze in the text area.
2.  Select the model to use (`Custom Model` or `Llama 3`).
3.  Click the "Analyze Sentiment" button.
4.  The sentiment analysis result will be displayed below the button.

## Dependencies

### Backend

* FastAPI
* Uvicorn
* Transformers
* Pydantic
* Groq
* python-dotenv

### Frontend

* React
* Axios

## Notes

* Ensure that the backend API is running before starting the React application.
* The `GROQ_API_KEY` environment variable must be set for the Llama 3 model to work.
* The custom model is `artisokka/imdb-fine-tuned-distilbert` from Hugging Face.
* The front end requires the backend to be running on localhost:8000.


