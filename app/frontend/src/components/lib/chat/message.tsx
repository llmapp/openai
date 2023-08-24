import { useEffect } from "react";
import Icon from "../icon";
import Markdown from "../markdown";
// import Interpreter from "./interpreter";
import Plugin from "./plugin";
import type { Plugin as PluginType } from "./types";

type MessageProps = {
  role: string;
  content: string | React.ReactNode;
  plugin?: PluginType;
  avatars?: { user?: string | React.ReactNode; assistant: string | React.ReactNode };
};

const Message = ({ role, content, plugin, avatars }: MessageProps) => {
  const bgColor = role === "assistant" ? "bg-gray-50" : "";
  const avatar = role === "assistant" ? avatars?.assistant : avatars?.user;

  return (
    <div className={`group w-full text-gray-800 border-b border-black/10 ${bgColor}`}>
      <div className="flex p-4 gap-4 text-base md:gap-6 md:max-w-2xl lg:max-w-[38rem] xl:max-w-3xl md:py-6 lg:px-0 m-auto">
        <div className="flex-shrink-0 flex flex-col relative items-end">
          <div className="w-[30px]">
            {typeof avatar === "string" ? (
              <div className="relative p-1 rounded-sm h-[30px] w-[30px] text-white flex items-center justify-center" style={{ backgroundColor: "rgb(25, 195, 125)" }}>
                <Icon name={avatar} />
              </div>
            ) : (
              <div className="relative flex">
                <span className="m-0 p-0 inline-block box-border border-0 max-w-full bg-none opacity-100 overflow-hidden">{avatar}</span>
              </div>
            )}
          </div>
        </div>
        <div className="relative flex w-[calc(100%-50px)] flex-col gap-1 md:gap-3 lg:w-[calc(100%-115px)]">
          <div className="flex flex-grow flex-col gap-3">
            {plugin && <Plugin plugin={plugin} />}
            {/* <Interpreter interpreter={{ code: "print('hello')", lang: "python", status: "working" }} /> */}
            <div className="min-h-[20px] flex items-start overflow-x-auto whitespace-pre-wrap break-words flex-col gap-2">
              <div className="markdown prose w-full break-words dark:prose-invert light">{typeof content === "string" ? <Markdown content={content} /> : content}</div>
            </div>
          </div>
          <div className="flex justify-between lg:block">
            <div className="text-gray-400 flex self-end lg:self-center justify-center mt-2 gap-2 md:gap-3 lg:gap-1 lg:absolute lg:top-0 lg:translate-x-full lg:right-0 lg:mt-0 lg:pl-2 visible">{role === "user" ? <IconsForUser /> : <IconsForAssistant />}</div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Message;

type CompletionMessageProps = {
  completions: string[];
  plugin?: PluginType;
  avatars?: { user?: string | React.ReactNode; assistant: string | React.ReactNode };
};

export const CompletionMessage = ({ completions, plugin, avatars }: CompletionMessageProps) => {
  return <Message role="assistant" content={completions.join("")} plugin={plugin} avatars={avatars} />;
};

const IconsForAssistant = () => {
  return (
    <>
      <button className="flex ml-auto gap-2 rounded-md p-1 hover:bg-gray-100 hover:text-gray-700">
        <Icon name="copy" />
      </button>
      <div className="flex gap-1">
        <button className="p-1 rounded-md hover:bg-gray-100 hover:text-gray-700">
          <Icon name="thumb-up" />
        </button>
        <button className="p-1 rounded-md hover:bg-gray-100 hover:text-gray-700">
          <Icon name="thumb-down" />
        </button>
      </div>
    </>
  );
};

const IconsForUser = () => {
  return (
    <button className="p-1 rounded-md hover:bg-gray-100 hover:text-gray-700 md:invisible md:group-hover:visible">
      <Icon name="edit-o" />
    </button>
  );
};
