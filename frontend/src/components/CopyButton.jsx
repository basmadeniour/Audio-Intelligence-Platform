import React, { useState } from "react";

export default function CopyButton({ text }) {
  const [copied, setCopied] = useState(false);

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(text);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      console.error("Failed to copy:", err);
    }
  };

  return (
    <button
      onClick={handleCopy}
      className="text-xs px-3 py-1 rounded bg-gray-800 hover:bg-gray-700 transition"
    >
      {copied ? "Copied!" : "Copy"}
    </button>
  );
}