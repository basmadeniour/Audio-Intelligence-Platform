import React from "react";

export default function HighlightsList({ highlights }) {
  if (!highlights || highlights.length === 0) return null;

  return (
    <div className="space-y-3">
      <h3 className="text-lg font-semibold text-white">Key Highlights</h3>
      <div className="space-y-2">
        {highlights.map((highlight, idx) => (
          <div key={idx} className="p-4 rounded-xl bg-gray-900 border-l-4 border-purple-500">
            <p className="text-sm text-gray-300">{highlight}</p>
          </div>
        ))}
      </div>
    </div>
  );
}