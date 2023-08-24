import { create } from "zustand";

type ScreenStore = {
  isSmall: boolean;
  setIsSmall: (isSmall: boolean) => void;
};

export const useScreenStore = create<ScreenStore>((set) => ({
  isSmall: false,
  setIsSmall: (isSmall) => set({ isSmall }),
}));
