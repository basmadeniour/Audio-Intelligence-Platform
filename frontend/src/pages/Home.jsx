import React, { useState, useRef } from "react";
import DragDropUpload from "../components/DragDropUpload";
import ResultTabs from "../components/ResultTabs";
import SearchBar from "../components/SearchBar";
import ProgressBar from "../components/ProgressBar";

export default function Home() {
  const [file, setFile] = useState(null);
  const [audioURL, setAudioURL] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState("results");

  const audioRef = useRef(null);

  const handleFileSelect = (file) => {
    setFile(file);
    setAudioURL(URL.createObjectURL(file));
    setResult(null);
  };

  const handleAnalyze = async () => {
    if (!file) return;

    setLoading(true);

    const formData = new FormData();
    formData.append("file", file);

    const res = await fetch("http://localhost:8000/api/v1/transcribe", {
      method: "POST",
      body: formData,
    });

    const data = await res.json();
    setResult(data);
    setLoading(false);
    setActiveTab("results");
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-black via-gray-900 to-black text-white">
      
      {/* HEADER */}
      <div className="border-b border-gray-800 px-6 py-4 flex justify-between items-center">
        <h1 className="text-xl font-semibold tracking-tight">
          🎧 Audio Intelligence
        </h1>
        <span className="text-sm text-gray-400">
          AI-powered insights
        </span>
      </div>

      <div className="max-w-7xl mx-auto px-6 py-8">

        {/* MAIN GRID */}
        <div className="grid lg:grid-cols-3 gap-6">

          {/* LEFT SIDE */}
          <div className="lg:col-span-2 space-y-4">

            <div className="bg-gray-900 border border-gray-800 rounded-2xl p-6">
              <h2 className="text-lg font-semibold mb-4">
                Upload Audio
              </h2>

              <DragDropUpload onFileSelect={handleFileSelect} />

              {audioURL && (
                <div className="mt-4">
                  <audio
                    ref={audioRef}
                    controls
                    src={audioURL}
                    className="w-full rounded-lg"
                  />
                </div>
              )}

              <button
                onClick={handleAnalyze}
                disabled={!file || loading}
                className={`mt-5 w-full py-3 rounded-xl font-medium transition ${
                  loading
                    ? "bg-gray-700"
                    : "bg-purple-600 hover:bg-purple-700"
                }`}
              >
                {loading ? "Processing..." : "Analyze Audio"}
              </button>

              <div className="mt-3">
                <ProgressBar isLoading={loading} />
              </div>
            </div>

          </div>

          {/* RIGHT SIDE */}
          <div className="space-y-4">

            <div className="bg-gray-900 border border-gray-800 rounded-2xl p-5">
              <h3 className="text-sm font-semibold mb-3 text-gray-300">
                File Info
              </h3>

              {file ? (
                <div className="text-sm text-gray-400 space-y-1">
                  <p>{file.name}</p>
                  <p>{(file.size / 1024 / 1024).toFixed(2)} MB</p>
                </div>
              ) : (
                <p className="text-gray-500 text-sm">
                  No file selected
                </p>
              )}
            </div>

            <div className="bg-gray-900 border border-gray-800 rounded-2xl p-5">
              <h3 className="text-sm font-semibold mb-3 text-gray-300">
                Actions
              </h3>

              <div className="space-y-2">
                <button
                  onClick={() => setActiveTab("results")}
                  className="w-full text-left px-3 py-2 rounded-lg bg-gray-800 hover:bg-gray-700"
                >
                  Results
                </button>

                <button
                  onClick={() => setActiveTab("search")}
                  className="w-full text-left px-3 py-2 rounded-lg bg-gray-800 hover:bg-gray-700"
                >
                  Search
                </button>

                <button
                  onClick={() => setActiveTab("qa")}
                  className="w-full text-left px-3 py-2 rounded-lg bg-gray-800 hover:bg-gray-700"
                >
                  Ask AI
                </button>
              </div>
            </div>

          </div>
        </div>

        {/* CONTENT */}
        {result && (
          <div className="mt-10 bg-gray-900 border border-gray-800 rounded-2xl p-6">

            {/* Tabs */}
            <div className="flex gap-3 mb-6">
              {["results", "search", "qa"].map((tab) => (
                <button
                  key={tab}
                  onClick={() => setActiveTab(tab)}
                  className={`px-4 py-2 rounded-lg text-sm ${
                    activeTab === tab
                      ? "bg-purple-600"
                      : "bg-gray-800 hover:bg-gray-700"
                  }`}
                >
                  {tab.toUpperCase()}
                </button>
              ))}
            </div>

            {/* TAB CONTENT */}
            {activeTab === "results" && (
              <ResultTabs result={result} />
            )}

            {activeTab === "search" && (
              <SearchBar onSearch={(q) => console.log(q)} />
            )}

            {activeTab === "qa" && (
              <div className="text-gray-400 text-sm">
                Ask functionality here...
              </div>
            )}

          </div>
        )}

      </div>
    </div>
  );
}