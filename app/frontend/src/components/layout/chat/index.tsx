import { useEffect } from "react";

import Sidebar from "./sidebar";
import Navbar from "./navbar";

import { useScreenStore } from "../../../store/screen";

type ChatLayoutProps = {
  children: React.ReactNode;
};

const ChatLayout = ({ children }: ChatLayoutProps) => {
  const isSmall = useScreenStore((state) => state.isSmall);
  const setIsSmall = useScreenStore((state) => state.setIsSmall);

  useEffect(() => {
    const handleResize = () => {
      setIsSmall(window.innerWidth < 768);
    };

    handleResize();
    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  });

  return (
    <>
      <div className="overflow-hidden w-screen h-screen relative flex z-0" style={isSmall ? { flexDirection: "column" } : {}}>
        {isSmall ? <Navbar /> : <Sidebar />}

        <div className="relative flex h-full max-w-full flex-1 overflow-hidden">
          <div className="flex h-full max-w-full flex-1 flex-col">
            <main className="relative h-full w-full transition-width flex flex-col overflow-auto items-stretch flex-1">
              <div className="flex-1 overflow-hidden">{children}</div>
            </main>
          </div>
        </div>
      </div>
    </>
  );
};

export default ChatLayout;
