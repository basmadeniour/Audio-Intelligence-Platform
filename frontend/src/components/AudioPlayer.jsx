import React from "react";

export default function AudioPlayer({ audioURL }) {
  if (!audioURL) return null;

  return (
    <div className="bg-gray-900 border border-gray-700 rounded-2xl p-4 mt-6">
      <p className="text-sm text-gray-400 mb-2">Audio Preview</p>
      <audio controls src={audioURL} className="w-full" />
    </div>
  );
}