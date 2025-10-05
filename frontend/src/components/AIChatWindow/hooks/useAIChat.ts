import { useState, useCallback } from "react";

interface AIResponse {
  answer: string;
  retrieved: any[];
}

const useAIChat = (endpoint: string) => {
  const [loading, setLoading] = useState(false);

  const sendMessage = useCallback(async (message: string): Promise<string> => {
    setLoading(true);
    try {
      const response = await fetch(endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: message }),
      });

      if (!response.ok) {
        throw new Error(`Server error: ${response.status}`);
      }

      const data: AIResponse = await response.json();
      return data.answer; // Only answer attribute
    } catch (err) {
      console.error("AI request failed:", err);
      return "Oops, something went wrong!";
    } finally {
      setLoading(false);
    }
  }, [endpoint]);

  return { sendMessage, loading };
};

export default useAIChat;
