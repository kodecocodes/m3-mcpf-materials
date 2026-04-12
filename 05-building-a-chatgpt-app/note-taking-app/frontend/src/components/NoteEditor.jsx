import React, { useState, useEffect } from 'react';

export default function NoteEditor({ note, onSave, onCancel }) {
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');

  useEffect(() => {
    setTitle(note?.title || '');
    setContent(note?.content || '');
    
  }, [note]);


  const handleSave = () => {
    onSave({ 
      ...note, 
      title: title.trim(), 
      content: content.trim()
    });
  };

  return (
    <div className="flex flex-col gap-3">
      <input 
        className="w-full text-lg font-bold bg-transparent border-b border-gray-200 focus:outline-none focus:border-black py-1"
        placeholder="Note Title"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
      />
      
      <textarea 
        className="w-full h-48 resize-none bg-white p-2 rounded border border-gray-200 focus:outline-none focus:ring-1 focus:ring-black text-sm"
        placeholder="Start typing..."
        value={content}
        onChange={(e) => setContent(e.target.value)}
      />
      
      
      <div className="flex justify-between">
        <div></div>
        
        <div className="flex gap-2">
          <button 
            onClick={onCancel} 
            className="text-sm text-gray-500 px-3 py-1"
          >
            Cancel
          </button>
          <button 
            onClick={handleSave}
            disabled={!title.trim()}
            className="bg-blue-600 text-white text-sm px-4 py-1 rounded hover:bg-blue-700 disabled:bg-gray-300"
          >
            Save
          </button>
        </div>
      </div>
    </div>
  );
}
