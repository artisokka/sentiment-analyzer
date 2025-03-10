import React, { useState } from 'react';
import axios from 'axios';

function SentimentAnalyzer() {
  const [inputText, setInputText] = useState('');
  const [selectedModel, setSelectedModel] = useState('custom');
  const [sentimentResult, setSentimentResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleInputChange = (e) => {
    setInputText(e.target.value);
  };

  const handleModelChange = (e) => {
    setSelectedModel(e.target.value);
  };

  const handleAnalyzeSentiment = async () => {
    setLoading(true);
    setSentimentResult(null);

    try {
      const response = await axios.post('http://127.0.0.1:8000/analyze/', {
        text: inputText,
        model: selectedModel,
      });
      setSentimentResult(response.data);
    } catch (error) {
      console.error('Error analyzing sentiment:', error);
      setSentimentResult({ sentiment: 'Error', confidence_score: 0 });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gradient-to-r from-blue-100 to-purple-100">
      <div className="bg-white p-10 shadow-2xl w-full max-w-lg">
        <h1 className="text-4xl font-extrabold text-purple-950 mb-8 text-center tracking-tight">
          Sentiment Analyzer
        </h1>

        <textarea
          placeholder="Enter text for sentiment analysis..."
          value={inputText}
          onChange={handleInputChange}
          className="w-full p-3 border border-gray-300 rounded-lg mb-6 focus:outline-none focus:ring-2 focus:ring-pink-400"
          rows="6"
        />

        <select
          value={selectedModel}
          onChange={handleModelChange}
          className="w-full p-3 border border-purple-400 rounded-lg mb-6 focus:outline-none focus:ring-2 focus:ring-pink-400"
        >
          <option value="custom">Custom Model</option>
          <option value="llama">Llama 3</option>
        </select>

        <button
          onClick={handleAnalyzeSentiment}
          disabled={loading}
          className={`w-full p-3 rounded-lg text-lg font-semibold text-white ${
            loading
              ? 'bg-gray-400 cursor-not-allowed'
              : 'bg-gradient-to-r from-pink-400 to-purple-400 hover:from-purple-400 hover:to-pink-400 transition-colors duration-300'
          }`}
        >
          {loading ? 'Analyzing...' : 'Analyze Sentiment'}
        </button>

        {sentimentResult && (
          <div className="mt-8">
            <h2 className="text-2xl font-semibold text-gray-700 mb-4">Sentiment Analysis Result:</h2>
            <p className="text-lg">
              Sentiment: <span className="font-bold text-pink-400">{sentimentResult.sentiment}</span>
            </p>
            {sentimentResult.confidence_score !== undefined && (
              <p className="text-lg">
                Confidence Score: <span className="font-bold text-purple-600">{sentimentResult.confidence_score}</span>
              </p>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

export default SentimentAnalyzer;