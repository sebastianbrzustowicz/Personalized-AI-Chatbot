import { useEffect } from "react";
import { Widget, addResponseMessage, renderCustomComponent, toggleInputDisabled, deleteMessages } from "react-chat-widget";
import "react-chat-widget/lib/styles.css";

import "./styles/AIChatWindow.css";
import robotAvatar from "./resources/robot-24.png";
import useAIChat from "./hooks/useAIChat";
import AIChatLoader from "./AIChatLoader";

const AIChatWindow = () => {
  const { sendMessage } = useAIChat("http://localhost:8000/ask");

  const handleNewUserMessage = async (newMessage: string) => {
    toggleInputDisabled();
    const loaderId = Date.now().toString();
    renderCustomComponent(AIChatLoader, {}, true, loaderId);

    try {
      const aiResponse = await sendMessage(newMessage);
      addResponseMessage(aiResponse);
    } catch (error) {
      addResponseMessage("Oops, something went wrong! 🤖");
    } finally {
      deleteMessages(1, loaderId);
      toggleInputDisabled();
    }
  };

  useEffect(() => {
    addResponseMessage(
      "Hi there! 👋 I'm your AI shopping assistant. How can I help you find the perfect product today?"
    );
  }, []);

  return (
    <Widget
      handleNewUserMessage={handleNewUserMessage}
      title="AI Assistant"
      subtitle="🟢 Online"
      profileAvatar={robotAvatar}
      launcherOpenLabel="Talk to AI"
      showTimeStamp
      launcherAccentColor="#458447"
      senderPlaceHolder="Type your message..."
    />
  );
};

export default AIChatWindow;
