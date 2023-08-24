import React from "react";
import ReactDOM from "react-dom/client";

import ChatPage from "./components/ChatPage";
import reportWebVitals from "./reportWebVitals";
import models from "./utils/model";

import "./index.css";

const ErrorPage = ({ id }: { id?: string }) => {
  return (
    <div className="w-screen h-screen flex flex-col justify-center items-center">
      <span className="flex flex-row space-x-2 text-2xl">
        <p>Model</p>
        <p className="text-red-700 font-bold">{`${id}`}</p> <p>not supported!</p>
      </span>
      <span className="mt-8 font-bold text-gray-700 text-3xl">Valid Models</span>
      <ol className="flex flex-col list-decimal sm:flex-row">
        {Object.keys(models).map((modelId) => {
          return (
            <a key={modelId} className="mx-4 text-green-700 text-xl font-bold" href={`?model=${modelId}`}>
              {modelId}
            </a>
          );
        })}
      </ol>
    </div>
  );
};

const App = () => {
  const modelId = window.location.search.split("=").pop();
  if (!modelId || !models[modelId]) {
    return <ErrorPage id={modelId} />;
  }
  const model = models[modelId];

  return <ChatPage id="modelId" model={model} />;
};

const root = ReactDOM.createRoot(document.getElementById("root") as HTMLElement);

root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

reportWebVitals();
