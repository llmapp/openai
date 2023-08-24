import { useRef } from "react";
import { ReactMarkdown } from "react-markdown/lib/react-markdown";
import RemarkBreaks from "remark-breaks";
import RemarkMath from "remark-math";
import RehypeKatex from "rehype-katex";
import RemarkGfm from "remark-gfm";
import RehypeHighlight from "rehype-highlight";

import Icon from "../icon";

import "katex/dist/katex.min.css";

const Markdown = ({ content }: { content: string }) => {
  return (
    <ReactMarkdown
      components={{ code: Code, br: BR, ol: OL, ul: UL }}
      remarkPlugins={[RemarkMath, RemarkGfm, RemarkBreaks]}
      rehypePlugins={[
        RehypeKatex,
        [
          RehypeHighlight,
          {
            detect: false,
            ignoreMissing: true,
          },
        ],
      ]}
    >
      {content}
    </ReactMarkdown>
  );
};

export default Markdown;

const BR = () => <></>;
const OL = ({ children }: { children: React.ReactNode }) => <ol className="list-decimal list-inside">{children}</ol>;
const UL = ({ children }: { children: React.ReactNode }) => <ol className="list-disc list-inside">{children}</ol>;
const Code = ({ className, children }: any) => {
  const codeRef = useRef(null);

  const copyToClipboard = () => {
    const el = codeRef.current;

    if (el) {
      const range = document.createRange();
      range.selectNodeContents(el);

      const selection = window.getSelection();
      selection?.removeAllRanges();
      selection?.addRange(range);

      document.execCommand("copy");
    }
  };

  return className?.includes("language-") ? (
    <div className="border rounded-md">
      <div className="flex items-center relative text-gray-200 bg-gray-700 px-4 py-2 text-xs font-sans justify-between rounded-t-md">
        <div className="">{className?.replace(/.*language-/, "")}</div>
        <button className="flex flex-row space-x-1 rounded-md px-2" onClick={copyToClipboard}>
          <Icon name="copy" /> <span>Copy code</span>
        </button>
      </div>

      <pre className={`px-4 pt-2 pb-4 ${className} text-sm rounded-b-md overflow-auto`}>
        <code ref={codeRef} className={`rounded-b-md font-mono`}>
          {children}
        </code>
      </pre>
    </div>
  ) : (
    children
  );
};
