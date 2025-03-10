# FastAPI Backend API with Model Loading

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Literal
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from groq import Groq
import os
import re

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
app.add_middleware(
    CORSMiddleware,  
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AnalyzeRequest(BaseModel):
    text: str
    model: Literal["custom", "llama"]

class AnalyzeResponse(BaseModel):
    sentiment: Literal["positive", "negative", "neutral"]
    confidence_score: float

# Load Models (Step 7)
try:
    custom_model_name = "artisokka/imdb-fine-tuned-distilbert"
    custom_tokenizer = AutoTokenizer.from_pretrained(custom_model_name)
    custom_model = AutoModelForSequenceClassification.from_pretrained(custom_model_name)
    print("Custom model loaded successfully.")
except Exception as e:
    print(f"Error loading custom model: {e}")
    custom_tokenizer = None
    custom_model = None

GROQ_API_KEY = "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" # Ensure correct environment variable name

def get_llama_response(text: str):
    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY environment variable not set.")
    try:
        client = Groq(api_key=GROQ_API_KEY)
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": f"Analyze the sentiment of the following text: '{text}'. Respond with only 'positive' or 'negative' and a confidence score between 0 and 1. Do not include any other text."}],
            temperature=1,
            max_completion_tokens=20,
            top_p=1,
            stream=False,
            stop=None,
        )
        return completion.choices[0].message.content.lower()
    except Exception as e:
        print(f"Error calling Groq API: {e}")
        return None

def analyze_custom_model(text: str) -> AnalyzeResponse:
    if custom_model and custom_tokenizer:
        inputs = custom_tokenizer(text, return_tensors="pt")
        outputs = custom_model(**inputs)
        probabilities = outputs.logits.softmax(dim=1)
        predicted_class = probabilities.argmax().item()
        confidence = probabilities[0, predicted_class].item()

        if predicted_class == 1:
            sentiment = "positive"
        else:
            sentiment = "negative"

        return AnalyzeResponse(sentiment=sentiment, confidence_score=confidence)
    else:
        return AnalyzeResponse(sentiment="neutral", confidence_score=0.5)

def analyze_llama_model(text: str) -> AnalyzeResponse:
    llama_response = get_llama_response(text)
    if llama_response:
        content = llama_response.lower()
        if "positive" in content:
            sentiment = "positive"
        elif "negative" in content:
            sentiment = "negative"
        else:
            sentiment = "neutral"
        match = re.search(r"(\d+(\.\d+)?)", content)
        if match:
            try:
                confidence = float(match.group(1))
                if confidence > 1:
                    confidence = 1
                if confidence < 0:
                    confidence = 0
            except ValueError:
                confidence = 0.5
        else:
            confidence = 0.5

        return AnalyzeResponse(sentiment=sentiment, confidence_score=confidence)
    else:
        return AnalyzeResponse(sentiment="neutral", confidence_score=0.5)

@app.post("/analyze/", response_model=AnalyzeResponse)
async def analyze(request: AnalyzeRequest):
    if request.model == "custom":
        return analyze_custom_model(request.text)
    elif request.model == "llama":
        return analyze_llama_model(request.text)
    else:
        raise HTTPException(status_code=400, detail="Invalid model specified")