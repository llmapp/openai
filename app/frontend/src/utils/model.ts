import { ModelCard } from "../types";

const models: Record<string, ModelCard> = {
  "chatglm2-6b": {
    id: "chatglm2-6b",
    name: "ChatGLM2-6B",
    homepage: "https://github.com/THUDM/ChatGLM2-6B",
    favicon: "/assets/avatars/chatglm.png",
  },
  "chatglm3-6b": {
    id: "chatglm3-6b",
    name: "ChatGLM3-6B",
    homepage: "https://github.com/THUDM/ChatGLM3",
    favicon: "/assets/avatars/chatglm.png",
  },
  "baichuan2-13b": {
    id: "Baichuan2-13B-Chat",
    name: "Baichuan2-13B",
    homepage: "https://huggingface.co/baichuan-inc/Baichuan2-13B-Chat",
    favicon: "/assets/avatars/baichuan.png",
  },
  "baichuan-13b": {
    id: "Baichuan-13B-Chat",
    name: "Baichuan-13B",
    homepage: "https://huggingface.co/baichuan-inc/Baichuan-13B-Chat",
    favicon: "/assets/avatars/baichuan.png",
  },
  "qwen-7b": {
    id: "Qwen-7B-Chat",
    name: "Qwen-7B-Chat",
    homepage: "https://github.com/QwenLM/Qwen",
    favicon: "/assets/avatars/qwen.webp",
  },
  "qwen-14b": {
    id: "Qwen-14B-Chat",
    name: "Qwen-14B-Chat",
    homepage: "https://github.com/QwenLM/Qwen",
    favicon: "/assets/avatars/qwen.webp",
  },
  "llama2-13b": {
    id: "Llama-2-13b-chat",
    name: "Llama2-13B-Chat",
    homepage: "https://huggingface.co/meta-llama/Llama-2-13b-chat-hf",
    favicon: "/assets/avatars/llama.png",
  },
};

export default models;
