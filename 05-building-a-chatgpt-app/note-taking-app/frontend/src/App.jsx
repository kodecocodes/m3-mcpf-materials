import React, { useState, useEffect, useRef } from 'react';
import { AppSDK } from './lib/sdk';
import { useToolOutput, useWidgetState } from './hooks/useOpenAi';
import NoteList from './components/NoteList';
import NoteEditor from './components/NoteEditor';
import NoteDetail from './components/NoteDetail';

export default function App() {
  const toolOutput = useToolOutput();
  const isInChatGPT = typeof window.openai !== 'undefined';
  
  const [widgetState, setWidgetState] = useWidgetState(() => ({
    view: 'list'
  }));
  
  const [notes, setNotes] = useState([]);
  const [activeNote, setActiveNote] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const hasHydratedFromToolOutput = useRef(false);

  useEffect(() => {
    if (toolOutput?.notes && !hasHydratedFromToolOutput.current) {
      setNotes(toolOutput.notes);
      setError(null);
      hasHydratedFromToolOutput.current = true;
      return;
    }
    if (isInChatGPT && !hasHydratedFromToolOutput.current) {
      refreshNotes();
    }
  }, [toolOutput, isInChatGPT]);


  const refreshNotes = async () => {
    setLoading(true);
    setError(null);
    try {
      if (!isInChatGPT) {
        setNotes([]);
        return;
      }
      const data = await AppSDK.callTool('list_notes');
      if (data?.notes && Array.isArray(data.notes)) {
        setNotes(data.notes);
      } else {
        setNotes([]);
      }
    } catch (err) {
      setError('Error loading notes: ' + err.message);
      setNotes([]);
    }
    setLoading(false);
  };

  const handleCreate = () => {
    setActiveNote({ title: '', content: '' });
    setWidgetState(prev => ({ ...prev, view: 'create' }));
  };

  const handleSelect = (note) => {
    setActiveNote(note);
    setWidgetState(prev => ({ ...prev, view: 'detail' }));
  };

  const handleSave = async (note) => {
    setLoading(true);
    setError(null);
    try {
      const createParams = {
        title: note.title,
        content: note.content
      };
      const result = await AppSDK.callTool('create_note', createParams);

      if (result?.notes && Array.isArray(result.notes)) {
        setNotes(result.notes);
      } else {
        await refreshNotes();
      }

      setWidgetState(prev => ({ ...prev, view: 'list' }));
    } catch (err) {
      setError('Error creating note: ' + err.message);
    }
    setLoading(false);
  };


  const handleCancel = () => {
    setWidgetState(prev => ({ ...prev, view: 'list' }));
  };

  const handleBack = () => {
    setActiveNote(null);
    setWidgetState(prev => ({ ...prev, view: 'list' }));
  };

  const currentView = widgetState?.view || 'list';

  return (
    <div className="min-h-screen bg-gray-50 text-gray-800 p-4 font-sans">
      <header className="mb-4 flex justify-between items-center">
        <h1 className="text-xl font-bold text-gray-900">AI Notes</h1>
        {currentView === 'list' && (
          <button 
            onClick={handleCreate}
            className="bg-black text-white px-3 py-1 rounded text-sm hover:bg-gray-800"
            disabled={loading}
          >
            + New
          </button>
        )}
      </header>

      {loading && <div className="text-center text-xs text-gray-500 my-2">Syncing with MCP...</div>}
      {error && (
        <div className="bg-red-100 border border-red-300 text-red-700 px-3 py-2 rounded text-xs mb-3">
          {error}
        </div>
      )}

      {currentView === 'list' && (
        <NoteList 
          notes={notes}
          onSelect={handleSelect}
        />
      )}

      {currentView === 'create' && (
        <NoteEditor 
          note={activeNote} 
          onSave={handleSave} 
          onCancel={handleCancel}
        />
      )}

      {currentView === 'detail' && (
        <NoteDetail
          note={activeNote}
          onBack={handleBack}
        />
      )}
    </div>
  );
}
