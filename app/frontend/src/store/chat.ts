import { create } from "zustand";
import { nanoid } from "nanoid";

import type { Chat, Message } from "../components/lib/chat/types";

const newChat = (): Chat => {
  return {
    id: nanoid(10),
    title: "",
    model: "",
    updateTime: new Date(),
    createTime: new Date(),
    saved: false,
  };
};

declare type ChatStore = {
  current: Chat;
  chats: Chat[];
  messages: Message[];

  select: (chat: Chat) => void;
  add: (chat: Chat) => void;
  remove: (chat: Chat) => void;
  update: (values: { [key: string]: any }) => void;
  setChats: (chats: Chat[]) => void;
  onNewChat: () => void;
};

export const useChatStore = create<ChatStore>((set) => ({
  current: newChat(),
  chats: [],
  messages: [],

  select: (chat) => set({ current: chat }),
  add: (chat) => set((state) => ({ chats: [chat, ...state.chats] })),
  remove: (chat) => set((state) => ({ chats: state.chats.filter((c) => c.id !== chat.id), current: newChat() })),
  update: (values) => set((state) => ({ current: { ...state.current, ...values } })),
  setChats: (chats) => set({ chats }),
  onNewChat: () => set({ current: newChat() }),
}));
