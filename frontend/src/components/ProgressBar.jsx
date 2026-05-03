import React from "react";

export default function ProgressBar({ isLoading }) {
  if (!isLoading) return null;

  return (
    <div className="w-full bg-gray-800 rounded-full h-1 overflow-hidden">
      <div className="bg-purple-600 h-1 rounded-full animate-pulse w-full" />
    </div>
  );
}