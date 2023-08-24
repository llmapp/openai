import React, { Dispatch, SetStateAction, useEffect, useRef, useState } from "react";

import UserInput from "./input";
import Banner from "./banner";
import MessageList from "./messages";
import MessageComp, { CompletionMessage } from "./message";

import { Message, Plugin, PluginAgent } from "./types.d";

const rightWidth = "0rem";

const Chat = (props: ChatProps) => {
  const { model, appendMessage, messages, onSend, onFinish, avatars, streamChat } = props;

  const lastRef = useRef<HTMLDivElement>(null);
  const [outOfLastLineMode, setOutOfLastLineMode] = useState(false);

  const inputRef = useRef<HTMLDivElement>(null);
  const [input, setInput] = useState<string>();

  const [plugin, setPlugin] = useState<Plugin | undefined>();
  const [completion, setCompletion] = useState<string[]>([]);
  const [complete, setComplete] = useState(false);

  const [isTyping, setIsTyping] = useState(false);

  const handleSend = async (message: Message) => {
    setIsTyping(true);
    setOutOfLastLineMode(false);
    onSend?.(message);

    const newMessages = [...messages, message];
    appendMessage(message);

    setComplete(false);

    setPlugin(undefined);
    const chunks = await streamChat(model.id, newMessages, setCompletion, plugins, setPlugin);

    if (chunks && chunks.length > 0) {
      setComplete(true);
    }
    setIsTyping(false);
  };

  useEffect(() => {
    if (complete) {
      const newMessage: Message = { role: "assistant", content: completion.join(""), plugin };
      appendMessage(newMessage);
      setComplete(false);
      setCompletion([]);
      setPlugin(undefined);
      onFinish?.(newMessage);
    }
  }, [complete, completion, onFinish]);

  useEffect(() => {
    if (!outOfLastLineMode) {
      lastRef.current?.scrollIntoView();
    }
  }, [completion, outOfLastLineMode]);

  useEffect(() => {
    const element = document.getElementById("content");
    element?.addEventListener("wheel", (e) => {
      const toUp = e.deltaY < 0;
      if (toUp) {
        setOutOfLastLineMode(true);
      }
    });
  }, []);

  const [plugins, setPlugins] = useState<PluginAgent[]>();
  useEffect(() => {
    const loadPlugins = async () => {
      const json = await fetch("/api/v1/plugins").then((res) => res.json());
      const pluginAgents = json.map((p: any) => Object.assign(new PluginAgent(p.name, p.description, p.arguments), p));

      setPlugins(pluginAgents);
    };
    loadPlugins();
  }, []);

  const widthStyle = { width: `calc(100% - ${rightWidth})` };

  return (
    <div className="h-full flex flex-col overflow-auto pb-4 relative font-sans" style={widthStyle}>
      <div id="content" className="h-full flex flex-col text-sm overflow-auto pb-32 md:pb-44">
        {messages.length > 0 ? <MessageList messages={messages} avatars={avatars} /> : <Banner title={model.name} {...banner} onClickExample={(item: string) => setInput(item)} />}
        {completion?.length > 0 || plugin ? <CompletionMessage completions={completion} plugin={plugin} avatars={avatars} /> : isTyping && <MessageComp role="assistant" content={<Loading />} avatars={avatars} />}
        {messages.length > 0 && <div ref={lastRef}></div>}
      </div>

      <div ref={inputRef} className="absolute bottom-0 w-full flex flex-col justify-center items-center bg-gradient-to-b from-transparent via-white to-white">
        <UserInput value={input} messages={messages} onSend={handleSend} />

        <div className="px-3 pb-3 pt-2 text-center text-xs text-gray-600 md:px-4 md:pb-6 md:pt-3 hidden md:block">
          <span className="text-xs font-semibold">
            Free Research Preview. LLM models may produce inaccurate information about people, places, or facts.{" "}
            <a className="underline" href={model.homepage}>
              {model.name}
            </a>
          </span>
        </div>
      </div>
    </div>
  );
};

export default Chat;

const Loading = () => {
  return (
    <div className="pt-3 flex flex-row space-x-1 rounded-full items-center">
      <div className="bg-blue-400 w-2 h-2 rounded-full animate-bounce transition" style={{ animationDelay: "0.1s" }} />
      <div className="bg-green-400 w-2 h-2 rounded-full animate-bounce transition" style={{ animationDelay: "0.2s" }} />
      <div className="bg-red-400 w-2 h-2 rounded-full animate-bounce transition" style={{ animationDelay: "0.3s" }} />
    </div>
  );
};
type ChatProps = {
  title?: string;
  streamChat: (modelId: string, messages: Message[], setCompletion: Dispatch<SetStateAction<string[]>>, plugins?: PluginAgent[], setPlugin?: Dispatch<SetStateAction<Plugin | undefined>>) => Promise<string[] | undefined>;
  model: { id: string; name: string; homepage: string };
  avatars: { user: string | React.ReactNode; assistant: string | React.ReactNode };
  footnote?: string | React.ReactNode;

  loading?: boolean;
  messages: Message[];
  appendMessage: (message: Message) => void;
  onSend?: (message: Message) => void;
  onFinish?: (message: Message) => void;

  // renderNavbar?: (() => React.ReactNode) | undefined;
  // renderMessageContent?: (message: Message) => React.ReactNode;
};

const banner = {
  examples: ["Explain quantum computing in simple terms", "Got any creative ideas for a 10 year old’s birthday?", "How do I make an HTTP request in Javascript?"],
  capabilities: ["Remembers what user said earlier in the conversation", "Allows user to provide follow-up corrections", "Trained to decline inappropriate requests"],
  limitations: ["May occasionally generate incorrect information", "May occasionally produce harmful instructions or biased content", "Limited knowledge of world and events after 2021"],
};
