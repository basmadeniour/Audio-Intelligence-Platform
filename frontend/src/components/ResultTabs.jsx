import React, { useState } from "react";
import ResultCard from "./ResultCard";
import ChaptersList from "./ChaptersList";
import HighlightsList from "./HighlightsList";

export default function ResultTabs({ result, onSeek }) {
  const [activeTab, setActiveTab] = useState("transcript");

  const tabs = [
    { id: "transcript", label: "Transcript", component: (
      <ResultCard title="Transcript" content={result.transcript} />
    )},
    { id: "summary", label: "Summary", component: (
      <ResultCard title="Summary" content={result.summary} />
    )},
    { id: "keywords", label: "Keywords", component: (
      <ResultCard title="Keywords" content={result.keywords?.join(", ")} />
    )},
    { id: "highlights", label: "Highlights", component: (
      <HighlightsList highlights={result.highlights} />
    )},
    { id: "chapters", label: "Chapters", component: (
      <ChaptersList chapters={result.chapters} onSeek={onSeek} />
    )}
  ];

  if (result.translated_text) {
    tabs.splice(2, 0, { id: "translation", label: "Translation", component: (
      <ResultCard title="Translation" content={result.translated_text} />
    )});
  }

  return (
    <div>
      <div className="flex flex-wrap gap-2 border-b border-gray-800 mb-6">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`px-4 py-2 text-sm font-medium transition ${
              activeTab === tab.id
                ? "text-purple-400 border-b-2 border-purple-400"
                : "text-gray-400 hover:text-white"
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>
      <div>{tabs.find((t) => t.id === activeTab)?.component}</div>
    </div>
  );
}