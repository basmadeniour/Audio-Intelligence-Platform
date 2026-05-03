import React, { useCallback, useState } from "react";

export default function DragDropUpload({ onFileSelect, accept = "audio/*" }) {
  const [isDragging, setIsDragging] = useState(false);

  const handleDragEnter = useCallback((e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(true);
  }, []);

  const handleDragLeave = useCallback((e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
  }, []);

  const handleDragOver = useCallback((e) => {
    e.preventDefault();
    e.stopPropagation();
  }, []);

  const handleDrop = useCallback(
    (e) => {
      e.preventDefault();
      e.stopPropagation();
      setIsDragging(false);
      const files = e.dataTransfer.files;
      if (files && files[0]) {
        onFileSelect(files[0]);
      }
    },
    [onFileSelect]
  );

  const handleFileInput = useCallback(
    (e) => {
      const files = e.target.files;
      if (files && files[0]) {
        onFileSelect(files[0]);
      }
    },
    [onFileSelect]
  );

  return (
    <div
      onDragEnter={handleDragEnter}
      onDragLeave={handleDragLeave}
      onDragOver={handleDragOver}
      onDrop={handleDrop}
      className={`border-2 border-dashed rounded-2xl p-10 text-center transition ${
        isDragging
          ? "border-purple-500 bg-purple-900/20"
          : "border-gray-600 hover:border-purple-500 hover:bg-gray-900"
      }`}
    >
      <input
        type="file"
        accept={accept}
        onChange={handleFileInput}
        className="hidden"
        id="dragDropInput"
      />
      <label htmlFor="dragDropInput" className="cursor-pointer block">
        <p className="text-lg text-white mb-2">Drag & Drop or Click to Upload</p>
        <p className="text-gray-400 text-sm">Supported formats: MP3, WAV, M4A, MP4</p>
      </label>
    </div>
  );
}