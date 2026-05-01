import React, { useState } from "react";
import UploadBox from "../components/UploadBox";
import AudioPlayer from "../components/AudioPlayer";
import ResultCard from "../components/ResultCard";

export default function Home() {
  const [file, setFile] = useState(null);
  const [audioURL, setAudioURL] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleAnalyze = async () => {
    if (!file) {
      setError("Please upload an audio file first.");
      return;
    }

    setError(null);
    setLoading(true);
    setResult(null);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch("http://localhost:8000/api/v1/transcribe", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`Request failed with status ${response.status}`);
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-black text-white px-6 py-10">
      <div className="max-w-5xl mx-auto">

        {/* Header */}
        <div className="mb-10 text-center">
          <h1 className="text-4xl font-bold tracking-tight">
            Audio Intelligence Platform
          </h1>
          <p className="text-gray-400 mt-3">
            Transform audio into structured insights using AI
          </p>
        </div>

        {/* Upload */}
        <UploadBox setFile={setFile} setAudioURL={setAudioURL} />

        {/* Player */}
        {audioURL && <AudioPlayer audioURL={audioURL} />}

        {/* Button */}
        <button
          onClick={handleAnalyze}
          disabled={loading}
          className={`mt-6 w-full py-3 rounded-xl font-medium transition ${
            loading
              ? "bg-gray-700 cursor-not-allowed"
              : "bg-purple-600 hover:bg-purple-700"
          }`}
        >
          {loading ? "Processing..." : "Analyze Audio"}
        </button>

        {/* Error */}
        {error && (
          <div className="mt-6 border border-red-500 bg-red-900/20 rounded-xl p-4 text-red-300 text-sm">
            {error}
          </div>
        )}

        {/* Results */}
        {result && (
          <div className="mt-10 grid md:grid-cols-2 gap-6">

            <div className="md:col-span-2">
              <ResultCard
                title="Transcript"
                content={result.transcript}
              />
            </div>

            <ResultCard
              title="Summary"
              content={result.summary}
            />

            <ResultCard
              title="Keywords"
              content={result.keywords?.join(", ")}
            />

          </div>
        )}

      </div>
    </div>
  );
}