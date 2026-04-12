import React from 'react';

export default function NoteList({ notes, onSelect }) {
  if (notes.length === 0) return <div className="text-gray-400 text-sm">No notes found.</div>;

  return (
    <div className="space-y-2">
      {notes.map((note) => (
        <div 
          key={note.id} 
          className="bg-white p-3 rounded shadow-sm border border-gray-100 hover:border-blue-500 transition-colors group"
        >
          <div className="flex justify-between items-start">
            <div className="flex-1">
              <h3 className="font-semibold text-sm">{note.title}</h3>
              {note.created_at && (
                <div className="text-xs text-gray-400 mt-1">
                  {new Date(note.created_at).toLocaleDateString()}
                </div>
              )}
            </div>
            {onSelect && (
              <button
                type="button"
                onClick={() => onSelect(note)}
                className="text-xs text-blue-600 hover:text-blue-800"
              >
                View
              </button>
            )}
          </div>
        </div>
      ))}
    </div>
  );
}
