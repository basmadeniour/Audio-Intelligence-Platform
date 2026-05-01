import React from "react";

export default function UploadBox({ setFile, setAudioURL }) {
  const handleChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setFile(file);
      setAudioURL(URL.createObjectURL(file));
    }
  };

  return (
    <div className="border border-dashed border-gray-600 rounded-2xl p-10 text-center hover:border-purple-500 hover:bg-gray-900 transition">
      <input
        type="file"
        accept="audio/*"
        onChange={handleChange}
        className="hidden"
        id="fileInput"
      />

      <label htmlFor="fileInput" className="cursor-pointer block">
        <p className="text-lg text-white mb-2">
          Upload Audio File
        </p>
        <p className="text-gray-400 text-sm">
          Supported formats: MP3, WAV, M4A, MP4
        </p>
      </label>
    </div>
  );
}