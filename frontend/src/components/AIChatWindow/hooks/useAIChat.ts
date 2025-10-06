import { useState, useCallback } from "react";

export interface AIResponse {
  answer: string;
  retrieved: Array<{ id: string; source: string; text_snippet: string }>;
}

interface UseAIChatOptions {
  onResponse?: (data: AIResponse) => void;
  onError?: (error: Error) => void;
}

const useAIChat = (endpoint: string, options?: UseAIChatOptions) => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const sendMessage = useCallback(
    async (message: string): Promise<string> => {
      setLoading(true);
      setError(null);

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

        options?.onResponse?.(data);

        return data.answer;
      } catch (err: any) {
        const message = err?.message || "Unknown error";
        setError(message);
        options?.onError?.(err);
        return "Oops, something went wrong!";
      } finally {
        setLoading(false);
      }
    },
    [endpoint, options]
  );

  return { sendMessage, loading, error };
};

export default useAIChat;
