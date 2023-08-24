import { useEffect, useRef, useState } from "react";
import TextareaAutosize from "react-textarea-autosize";

import Icon from "../icon";

import type { Message } from "./types";

const UserInput = (props: UserInputProps) => {
  const { value, messages, onSend } = props;

  const [input, setInput] = useState(value ?? "");
  const textarea = useRef<HTMLTextAreaElement>(null);

  const regenerate = async () => {
    alert("Not implemented yet");
  };

  const sendMessage = async () => {
    if (!input) return;

    if (textarea.current) {
      textarea.current.value = "";
    }

    onSend({ role: "user", content: input });
    setInput("");
  };

  useEffect(() => {
    setInput(value ?? "");
    textarea.current?.focus();
  }, [value]);

  return (
    <>
      {messages?.length > 0 && (
        <div className="h-10 flex flex-row space-x-2 text-base items-center cursor-pointer border bg-white text-gray-500 px-4 mb-3 rounded-lg" onClick={() => regenerate()}>
          <Icon name="sync" color="" size={14} />
          <span>Regenerate response</span>
        </div>
      )}

      <div className="max-w-[840px] w-full md:w-4/5 flex flex-row items-center justify-between shadow-xl pl-4 py-1 bg-white text-gray-300 border md:rounded-lg relative" style={{ minHeight: "3rem" }}>
        <TextareaAutosize
          maxRows={8}
          ref={textarea}
          placeholder="Send a message."
          className="flex-1 text-black bg-transparent items-center resize-none outline-none py-3 pr-8"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter" && !e.shiftKey) {
              e.preventDefault();
              sendMessage();
            }
          }}
        />
        <div onClick={sendMessage} className="absolute bottom-4 right-4 text-gray-400 cursor-pointer">
          <Icon name="send" size={26} color={input.length > 0 ? "green" : ""} />
        </div>
      </div>
    </>
  );
};

export default UserInput;

type UserInputProps = {
  messages: Message[];
  onSend: (message: Message) => void;
  value?: string;
};
