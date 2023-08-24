import { Dispatch, SetStateAction } from "react";

import { getRawCompletions } from "../components/lib/chat/utils";
import * as API from "../utils/api";

import type { Chat, Message, Plugin, PluginAgent } from "../components/lib/chat/types";

export const OPENAI_API_BASE = "/api/v1";

export const getChatList = async () => {
  const fetched = await API.chat.query({}, "asc");
  return fetched?.map((c) => c as Chat) ?? [];
};

export const updateChat = async (chat: Chat, modelId: string, message: Message) => {
  const title = await summaryToTitle(message, modelId);
  chat = {
    ...chat,
    title,
    model: modelId,
    updateTime: new Date(),
    createTime: new Date(),
    saved: true,
  };
  await API.chat.create(chat);

  return chat;
};

const summaryToTitle = async (message: Message, modelId: string) => {
  const content = `请你根据下面的内容用中文总结成少于10个字的标题，内容是： \n\n${message.content}`;
  const summary = [{ role: "user", content }] as Message[];
  const completion = await getRawCompletions(OPENAI_API_BASE, modelId, summary, () => {});
  return completion?.join("").replaceAll('"', "") ?? "Untitled";
};

export const streamChat = async (modelId: string, messages: Message[], setCompletion: Dispatch<SetStateAction<string[]>>, plugins?: PluginAgent[], setPlugin?: Dispatch<SetStateAction<Plugin | undefined>>) => {
  return await getRawCompletions(OPENAI_API_BASE, modelId, messages, setCompletion, plugins, setPlugin);
};
