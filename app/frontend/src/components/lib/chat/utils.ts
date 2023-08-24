import { Dispatch, SetStateAction } from "react";

import type { Message, Plugin, PluginAgent } from "./types";

export const getRawCompletions = async (apiBase: string, model: string, messages: Message[], setCompletion: Dispatch<SetStateAction<string[]>>, plugins?: PluginAgent[], setPlugin?: Dispatch<SetStateAction<Plugin | undefined>>) => {
  const chunks: string[] = [];
  setCompletion([]);
  const body = { model, messages, stream: true } as any;
  if (plugins && plugins.length > 0) {
    body["functions"] = plugins.map((p) => p.toFunction());

    const plugin: Plugin = {};
    const pluginProcessor = (delta: any) => processPluginChat(delta, plugin, setPlugin, chunks, setCompletion);
    while (true) {
      const finishReason = await streamRequest(apiBase, body, pluginProcessor);
      // add the function call message to messages
      if (finishReason === "function_call") {
        const assistantMessage: Message = { role: "assistant", function_call: { name: plugin.name ?? "", arguments: plugin.request } };
        body.messages.push(assistantMessage);
        const agent = plugins.find((p) => p.name === plugin.name);
        const result = await agent?.run(plugin.request);
        setPlugin?.((prev) => ({ ...prev, status: "done", response: JSON.stringify(result) }));
        const newMessage: Message = { role: "function", name: plugin.name, content: JSON.stringify(result) };
        body.messages.push(newMessage);
        plugin.request = undefined;
        plugin.status = undefined;
        plugin.response = undefined;
        plugin.name = undefined;
      } else {
        break;
      }
    }
  } else {
    const normalProcessor = (delta: any) => processNormalChat(delta, setCompletion, chunks);
    await streamRequest(apiBase, body, normalProcessor);
  }
  return chunks;
};

const processNormalChat = (delta: any, setCompletion: Dispatch<SetStateAction<string[]>>, chunks: string[]) => {
  if (delta?.content) {
    const chunk = delta?.content ?? "";
    setCompletion((prev) => [...prev, chunk]);
    chunks.push(chunk);
  }
};

const processPluginChat = (delta: any, plugin: Plugin, setPlugin?: Dispatch<SetStateAction<Plugin | undefined>>, chunks?: string[], setCompletion?: Dispatch<SetStateAction<string[]>>) => {
  if (delta.function_call) {
    const { name, arguments: args } = delta?.function_call;
    if (name) {
      plugin.name = name;
      plugin.status = "working";
      setPlugin?.({ ...plugin });
    }
    if (args) {
      const newArgs = `${plugin?.request ?? ""}${args}`;
      plugin.request = newArgs;
      setPlugin?.({ ...plugin });
    }
  }
  if (delta?.content) {
    const chunk = delta?.content ?? "";
    setCompletion?.((prev) => [...prev, chunk]);
    chunks?.push(chunk);
  }
};

const streamRequest = async (apiBase: string, body: any, deltaProcessor: (delta: any) => void, onFinish?: () => void) => {
  const response = await fetch(`${apiBase}/chat/completions`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });

  const stream = response.body;
  if (!stream) return;

  let finishReason = "stop";
  const reader = stream.getReader();
  try {
    while (true) {
      const { done, value } = await reader.read();
      if (done) {
        onFinish?.();
        break;
      }
      const text = new TextDecoder("utf-8").decode(value);
      const choices = getChoices(text);
      for (let choice of choices) {
        deltaProcessor(choice?.delta ?? {});
        if (choice["finish_reason"] && choice["finish_reason"] !== null) {
          finishReason = choice?.finish_reason;
        }
      }
    }
  } catch (error) {
    console.error(error);
  } finally {
    reader.releaseLock();
  }
  return finishReason;
};

const getChoices = (value: string) => {
  const candidates = value
    .split("data:")
    .map((c) => c.trim())
    .filter((c) => c.length > 0 && c !== "[DONE]");
  const choices = candidates.map((c) => {
    try {
      return JSON.parse(c).choices[0] ?? {};
    } catch (error) {
      return {};
    }
  });
  return choices;
};
