import { useEffect } from "react";
import { Widget, addResponseMessage, renderCustomComponent, toggleInputDisabled, deleteMessages } from "react-chat-widget";
import "react-chat-widget/lib/styles.css";

import "./styles/AIChatWindow.css";
import robotAvatar from "./resources/robot-24.png";
import useAIChat from "./hooks/useAIChat.ts";
import AIChatLoader from "./AIChatLoader.tsx"

const AIChatWindow = () => {
  const { sendMessage } = useAIChat("http://localhost:8000/ask");

  const handleNewUserMessage = async (newMessage: string) => {
    console.log("User message:", newMessage);
    toggleInputDisabled();
    const loaderId = Date.now().toString();
    renderCustomComponent(AIChatLoader, {}, true, loaderId);

    const aiResponse = await sendMessage(newMessage);

    deleteMessages(1, loaderId);
    toggleInputDisabled();
    addResponseMessage(aiResponse);
  };

  useEffect(() => {
    addResponseMessage("Hi there! 👋 I'm your AI shopping assistant. How can I help you find the perfect product today?");
  }, []);

  return (
    <div>
      <Widget
        handleNewUserMessage={handleNewUserMessage}
        title="AI assistant"
        subtitle="🟢 Online"
        profileAvatar={robotAvatar}
        launcherOpenLabel="Talk to AI"
        showTimeStamp={true}
        launcherAccentColor="#458447"
        senderPlaceHolder="Type your message..."
      />
    </div>
  );
};

export default AIChatWindow;
