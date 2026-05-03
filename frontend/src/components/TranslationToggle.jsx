import React from "react";

export default function TranslationToggle({ showTranslation, onToggle }) {
  return (
    <div className="flex items-center justify-end gap-3">
      <span className="text-sm text-gray-400">Show Translation</span>
      <button
        onClick={onToggle}
        className={`w-12 h-6 rounded-full transition ${
          showTranslation ? "bg-purple-600" : "bg-gray-700"
        } relative`}
      >
        <div
          className={`absolute top-1 w-4 h-4 rounded-full bg-white transition ${
            showTranslation ? "left-7" : "left-1"
          }`}
        />
      </button>
    </div>
  );
}