import { useEffect, useRef, useState } from "react";

import Icon from "../../lib/icon";
import Sidebar from "./sidebar";

import { useChatStore } from "../../../store/chat";

const Navbar = () => {
  const current = useChatStore((state) => state.current);
  const onNewChat = useChatStore((state) => state.onNewChat);

  const [show, setShow] = useState(false);

  useEffect(() => {
    if (current.saved === false) return;
    setShow(false);
  }, [current]);

  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (ref.current && !ref.current.contains(event.target as Node)) {
        setShow(false);
      }
    };

    document.addEventListener("mousedown", handleClickOutside);

    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, [ref, setShow]);

  return (
    <>
      {show && (
        <div className="relative z-20">
          <div className="fixed inset-0 bg-gray-600 bg-opacity-75 opacity-100"></div>
          <div className="fixed inset-0 flex">
            <div className="relative flex w-full max-w-xs flex-1 flex-col bg-gray-900 translate-x-0">
              <div className="scrollbar-trigger absolute right-0 top-0 -mr-12 pt-2 opacity-100">
                <button onClick={() => setShow(false)} className="ml-1 flex h-10 w-10 items-center justify-center focus:outline-none focus:ring-2 focus:ring-inset focus:ring-white">
                  <span className="sr-only">Close sidebar</span>
                  <span className="text-white">
                    <Icon name="close" />
                  </span>
                </button>
              </div>
              <div ref={ref} className="relative h-full w-full flex-1 items-start border-white/20">
                <Sidebar />
              </div>
            </div>
            <div className="w-14 flex-shrink-0"></div>
          </div>
        </div>
      )}

      <div className="sticky top-0 z-10 flex items-center border-b border-white/20 bg-gray-800 py-1 px-3 text-gray-200">
        <button onClick={() => setShow(true)} className="-ml-0.5 -mt-0.5 inline-flex h-10 w-10 items-center justify-center rounded-md hover:text-gray-900 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-white dark:hover:text-white">
          <span className="sr-only">Open sidebar</span>
          <Icon name="menu" />
        </button>

        <h1 className="flex-1 text-center text-base font-normal">{current.saved === false ? "New chat" : current.title}</h1>

        <button className="h-10 w-10 flex items-center justify-center" onClick={onNewChat}>
          <Icon name="plus" />
        </button>
      </div>
    </>
  );
};

export default Navbar;
