import { useState } from "react";

import Icon from "../icon";
import type { Plugin } from "./types";

type PluginProps = {
  plugin: Plugin;
};

const PluginComp = ({ plugin }: PluginProps) => {
  const [show, setShow] = useState(false);

  const onClick = () => {
    setShow(!show);
  };

  const bgColor = plugin.status === "working" ? "bg-green-100" : "bg-gray-200";
  return (
    <div className="flex flex-col items-start">
      <div className={`flex items-center text-xs ${bgColor} rounded p-3 text-gray-900`}>
        {plugin.status === "working" && <PluginWorking plugin={plugin} />}
        {plugin.status === "done" && <PluginResult plugin={plugin} />}

        <div className="ml-12 flex items-center gap-2 w-4 h-4" role="button" onClick={onClick}>
          {show ? <Icon name="up" /> : <Icon name="down" />}
        </div>
      </div>

      {show && (
        <div className="my-3 flex w-full max-w-full flex-col gap-3">
          <CodeBlock type="request" name={plugin.name ?? ""} code={plugin.request} />
          <CodeBlock type="response" name={plugin.name ?? ""} code={plugin.response} />
        </div>
      )}
    </div>
  );
};

export default PluginComp;

const PluginWorking = ({ plugin }: PluginProps) => {
  return (
    <>
      <div>
        <div className="flex items-center gap-3">
          <div>
            Using <b>{plugin.name}</b>...
          </div>
        </div>
      </div>
      <span className="w-4 h-4 flex items-center justify-center animate-spin text-center shrink-0 ml-1">
        <Icon name="spin" size={15} />
      </span>
    </>
  );
};

const PluginResult = ({ plugin }: PluginProps) => {
  return (
    <div className="flex items-center gap-3">
      <div>
        Used <b>{plugin.name}</b>
      </div>
    </div>
  );
};

const CodeBlock = ({ name, code, type }: { name: string; code: string; type: "request" | "response" }) => {
  const typeName = type === "request" ? "Request to" : "Response from";
  return (
    <div className="bg-black rounded-md w-full text-xs text-white/80">
      <div className="flex items-center relative text-gray-200 bg-gray-800 px-4 py-2 text-xs font-sans justify-between rounded-t-md">
        <span>
          <span className="uppercase">
            {typeName} {name}
          </span>
        </span>
        <span className="text-white/50">
          <Icon name="info" />
        </span>
      </div>
      <div className="p-4 overflow-y-auto">
        <code className="!whitespace-pre-wrap">{code}</code>
      </div>
    </div>
  );
};
