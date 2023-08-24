import { useState } from "react";

import Icon from "../../../lib/icon";
import { useScreenStore } from "../../../../store/screen";

import History from "./history";
import Footer from "./footer";
import Header from "./header";

const Sidebar = () => {
  const isScreenSmall = useScreenStore((state) => state.isSmall);

  const sidebarWidth = "260px";

  const [show, setShow] = useState(true);

  const onToggle = () => {
    setShow(!show);
  };

  return show ? (
    <div className="flex-shrink-0 overflow-x-hidden bg-gray-900" style={!isScreenSmall ? { width: sidebarWidth } : {}}>
      <div className="w-full h-full">
        <div className="flex h-full min-h-0 flex-col ">
          <div className="scrollbar-trigger relative h-full w-full flex-1 items-start border-white/20">
            <h2 className="absolute border-0 w-0 h-0 p-0 m-[-1px] overflow-hidden clip-rect-0 whitespace-nowrap overflow-wrap-normal">Chat history</h2>
            <nav className="flex h-full w-full flex-col p-2" aria-label="Chat history">
              <Header hideIcon={!isScreenSmall && <SidebarTrigger onToggle={onToggle} color="text-white border-white/20 hover:bg-gray-500/10" />} />
              <History />
              <Footer />
            </nav>
          </div>
        </div>
      </div>
    </div>
  ) : (
    <div className="absolute left-2 top-2 z-20">
      <SidebarTrigger onToggle={onToggle} color="bg-white border-black/10 hover:bg-gray-100" />
    </div>
  );
};

export default Sidebar;

const SidebarTrigger = ({ color, onToggle }: { color?: string; onToggle: () => void }) => {
  return (
    <span className="" data-state="closed">
      <a onClick={() => onToggle()} className={`flex p-3 gap-3 transition-colors duration-200 ${color} cursor-pointer text-sm rounded-md border h-11 w-11 flex-shrink-0 items-center justify-center`}>
        <Icon name="sidebar" size={16} />
        <span className="absolute border-0 w-[1px] h-[1px] p-0 m-[-1px] overflow-hidden clip-rect-0 whitespace-nowrap overflow-wrap-normal">Close sidebar</span>
      </a>
    </span>
  );
};
