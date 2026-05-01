import React from "react";

export default function ResultCard({ title, content }) {
  return (
    <div className="bg-gray-900 border border-gray-700 rounded-2xl p-6 shadow-sm">
      <h3 className="text-lg font-semibold text-white mb-4">
        {title}
      </h3>

      <div className="text-gray-300 text-sm leading-relaxed whitespace-pre-wrap max-h-64 overflow-y-auto pr-2">
        {content || "No content available"}
      </div>
    </div>
  );
}