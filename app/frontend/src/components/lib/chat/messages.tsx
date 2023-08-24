import MessageComp from "./message";

import type { Message, Plugin } from "./types";

type MessageListProps = {
  messages: Message[];
  avatars: { user: string | React.ReactNode; assistant: string | React.ReactNode };
};

const MessageList = ({ messages, avatars }: MessageListProps) => {
  return (
    <>
      {messages?.map((message, index) => {
        // let plugin = undefined;

        // if (message.role === "assistant") {
        //   plugin = {
        //     name: "WebPilot",
        //     status: "done" as any,
        //     request: dummyRequest,
        //     response: dummyResponse,
        //   } as Plugin;
        // }

        return <MessageComp key={index} role={message?.role} content={message?.content} plugin={message.plugin} avatars={avatars} />;
      })}
    </>
  );
};

export default MessageList;

const dummyRequest = `
{
  "link": "https://www.google.com/search?q=2022年8月9日天气",
  "lp": false,
  "ur": "2022年8月9日天气",
  "l": "zh-CN",
  "rt": false
}
`;

const dummyResponse = `
{
  "title": "",
  "content": "本周迎来超长伏天天气湿热_抚顺市人民政府",
}
`;
