export const AppSDK = {
  callTool: async (toolName, args = {}) => {
    if (window.openai?.callTool) {
      try {
        const result = await window.openai.callTool(toolName, args);
        return result?.structuredContent ?? result ?? null;
      } catch (e) {
        throw new Error(`Tool call failed: ${e.message}`);
      }
    }

    throw new Error('ChatGPT host is not available.');
  },

};
