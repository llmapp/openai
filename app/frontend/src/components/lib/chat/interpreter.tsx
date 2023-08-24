import { useState } from "react";

import Icon from "../icon";

type InterpreterProps = {
  interpreter: { status?: "working" | "done"; code: string; lang: string };
};

const InterpreterComp = ({ interpreter }: InterpreterProps) => {
  const [show, setShow] = useState(false);

  const onClick = () => {
    setShow(!show);
  };

  const bgColor = interpreter.status === "working" ? "bg-green-100" : "bg-gray-200";
  return (
    <div className="flex flex-col items-start">
      <div className={`flex items-center text-xs ${bgColor} rounded p-3 text-gray-900`}>
        {interpreter.status === "working" && <PluginWorking interpreter={interpreter} />}
        {interpreter.status === "done" && <PluginResult interpreter={interpreter} />}

        <div className="ml-12 flex items-center gap-2" role="button" onClick={onClick}>
          <div className="text-xs text-gray-600">{show ? "Hide" : "Show"} work</div>
          <span className="w-4 h-4">{show ? <Icon name="up" size={16} /> : <Icon name="down" size={16} />}</span>
        </div>
      </div>

      {show && (
        <div className="my-3 flex w-full max-w-full flex-col gap-3">
          <CodeBlock lang={interpreter.lang} code={interpreter.code ?? "python"} />
        </div>
      )}
    </div>
  );
};

export default InterpreterComp;

const PluginWorking = ({ interpreter }: InterpreterProps) => {
  return (
    <>
      <div>
        <div className="flex items-center gap-3">
          <div>Working...</div>
        </div>
      </div>
      <span className="w-4 h-4 flex items-center justify-center animate-spin text-center shrink-0 ml-1">
        <Icon name="spin" size={15} />
      </span>
    </>
  );
};

const PluginResult = ({ interpreter }: InterpreterProps) => {
  return (
    <div className="flex items-center gap-3">
      <div>Finished working</div>
    </div>
  );
};

const CodeBlock = ({ lang, code }: { code: string; lang: string }) => {
  return (
    <div className="bg-black rounded-md w-full text-xs text-white/80">
      <div className="flex items-center relative text-gray-200 bg-gray-800 px-4 py-2 text-xs font-sans justify-between rounded-t-md">
        <span>
          <span className="uppercase">{lang}</span>
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
