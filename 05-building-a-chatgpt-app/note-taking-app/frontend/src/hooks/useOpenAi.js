import { useState, useEffect, useSyncExternalStore, useCallback } from 'react';

const SET_GLOBALS_EVENT_TYPE = 'openai:set_globals';

export const useOpenAiGlobal = (key) => {
  return useSyncExternalStore(
    (onChange) => {
      const handleSetGlobal = (event) => {
        const value = event.detail?.globals?.[key];
        if (value === undefined) {
          return;
        }
        onChange();
      };

      window.addEventListener(SET_GLOBALS_EVENT_TYPE, handleSetGlobal, {
        passive: true,
      });

      return () => {
        window.removeEventListener(SET_GLOBALS_EVENT_TYPE, handleSetGlobal);
      };
    },
    () => window.openai?.[key]
  );
};

export const useToolOutput = () => {
  return useOpenAiGlobal('toolOutput');
};

export const useWidgetState = (defaultState) => {
  const widgetStateFromWindow = useOpenAiGlobal('widgetState');
  
  const [widgetState, _setWidgetState] = useState(() => {
    if (widgetStateFromWindow != null) {
      return widgetStateFromWindow;
    }
    
    return typeof defaultState === 'function' ? defaultState() : defaultState ?? null;
  });
  
  useEffect(() => {
    if (widgetStateFromWindow != null) {
      _setWidgetState(widgetStateFromWindow);
    }
  }, [widgetStateFromWindow]);
  
  const setWidgetState = useCallback(
    (state) => {
      _setWidgetState((prevState) => {
        const newState = typeof state === 'function' ? state(prevState) : state;
        
        if (newState != null && window.openai?.setWidgetState) {
          window.openai.setWidgetState(newState);
        }
        
        return newState;
      });
    },
    []
  );
  
  return [widgetState, setWidgetState];
};
