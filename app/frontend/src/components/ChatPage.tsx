import { useEffect, useState } from "react";

import Chat from "./lib/chat";
import Icon from "./lib/icon";
import ChatLayout from "./layout/chat";

import * as API from "../utils/api";
import { updateChat, getChatList, streamChat } from "../services/chat";

import { useChatStore } from "../store/chat";

import type { Message } from "./lib/chat/types";
import type { ModelCard } from "../types";
import type { CrudApi } from "../utils/crud/types";

type ChatPageProps = { id: string; model: ModelCard };

const ChatPage = ({ model }: ChatPageProps) => {
  const [messageAPI, setMessageAPI] = useState<CrudApi<API.RemoteMessage> | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState<boolean>(false);

  const current = useChatStore((state) => state.current);
  const setChats = useChatStore((state) => state.setChats);
  const addChat = useChatStore((state) => state.add);
  const updateChatInStore = useChatStore((state) => state.update);

  useEffect(() => {
    document.title = `${model.name} | Chat`;
    const favicon = document.getElementById("favicon") as HTMLLinkElement;
    if (favicon) {
      favicon.href = model.favicon ?? "";
    }
  }, [model]);

  useEffect(() => {
    const getChats = async () => setChats(await getChatList());
    getChats();
  }, [setChats]);

  useEffect(() => {
    const getMessagesWithAPI = async (api: CrudApi<API.RemoteMessage>) => {
      setLoading(true);
      const messages = await api.query({}, "dsc");
      setMessages(messages?.map((m) => m.message) ?? []);
      setLoading(false);
    };

    const api = API.message(current.id);
    setMessageAPI(api);
    if (current.saved !== false) {
      getMessagesWithAPI(api);
    } else {
      setMessages([]);
    }
  }, [current.id]);
  const onSend = async (message: Message) => {
    if (current.saved === false) {
      const chat = await updateChat(current, model.id, message);
      addChat(chat);
      updateChatInStore({ ...chat });
    }

    await messageAPI?.create(message2remote(message));
  };

  const onFinish = async (message: Message) => await messageAPI?.create(message2remote(message));
  const appendMessage = (message: Message) => setMessages((prev) => [...prev, message]);
  const assistantAvatar = <img src={model.favicon} alt={model.name} className="w-8 h-8 rounded" />;
  return <ChatLayout>{loading ? <div className="w-full h-full flex justify-center items-center text-gray-700">Loading ...</div> : <Chat key={current.id} streamChat={streamChat} model={model} loading={loading} avatars={{ assistant: assistantAvatar, user: <Icon name="user" size={32} /> }} messages={messages} appendMessage={appendMessage} onSend={onSend} onFinish={onFinish} />}</ChatLayout>;
};

export default ChatPage;

const message2remote = (message: Message) => {
  const now = new Date();
  return { message, createTime: now, updateTime: now };
};
