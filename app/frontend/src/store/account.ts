import { create } from "zustand";

import type { User } from "../types";

const MOCK_USER = { account: "you@openai.mini", avatar: "/assets/avatars/logo.jpg" };

declare type AccountStore = {
  current?: User;

  login: () => void;
  logout: () => void;
};

export const useAccountStore = create<AccountStore>((set) => ({
  current: MOCK_USER,
  login: () => set({ current: MOCK_USER }),
  logout: () => set({ current: undefined }),
}));
