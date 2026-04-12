import React from 'react';

export default function NoteDetail({ note, onBack }) {
  if (!note) return null;

  return (
    <div className="flex flex-col gap-4">
      <div>
        <h2 className="text-lg font-bold text-gray-900">{note.title}</h2>
        {note.created_at && (
          <div className="text-xs text-gray-400 mt-1">
            {new Date(note.created_at).toLocaleDateString()}
          </div>
        )}
      </div>

      <div className="text-sm text-gray-800 whitespace-pre-wrap">
        {note.content || 'No content.'}
      </div>

      <div>
        <button
          type="button"
          onClick={onBack}
          className="text-sm text-gray-500 px-3 py-1"
        >
          Back
        </button>
      </div>
    </div>
  );
}
