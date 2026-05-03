import React from "react";

export default function ChaptersList({ chapters, onSeek }) {
  if (!chapters || chapters.length === 0) return null;

  return (
    <div className="space-y-3">
      <h3 className="text-lg font-semibold text-white">Chapters</h3>
      <div className="space-y-2">
        {chapters.map((chapter, idx) => (
          <button
            key={idx}
            onClick={() => onSeek && onSeek(chapter.start)}
            className="w-full text-left p-4 rounded-xl bg-gray-900 border border-gray-800 hover:border-purple-500 transition"
          >
            <p className="text-sm text-purple-400">
              {formatTime(chapter.start)} - {formatTime(chapter.end)}
            </p>
            <p className="text-sm text-gray-300 mt-1">{chapter.topic || chapter.text?.substring(0, 100)}...</p>
          </button>
        ))}
      </div>
    </div>
  );
}

function formatTime(seconds) {
  if (!seconds) return "0:00";
  const mins = Math.floor(seconds / 60);
  const secs = Math.floor(seconds % 60);
  return `${mins}:${secs.toString().padStart(2, "0")}`;
}