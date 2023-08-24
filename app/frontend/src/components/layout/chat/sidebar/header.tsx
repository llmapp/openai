import React from "react";

import Icon from "../../../lib/icon";
import { useChatStore } from "../../../../store/chat";

type HeaderProps = {
  hideIcon?: React.ReactNode;
};

const Header = ({ hideIcon }: HeaderProps) => {
  const onNewChat = useChatStore((state) => state.onNewChat);

  return (
    <>
      <div className="mb-1 flex flex-row gap-2">
        <a onClick={onNewChat} className="flex p-3 items-center gap-3 transition-colors duration-200 text-white cursor-pointer text-sm rounded-md border border-white/20 hover:bg-gray-500/10 h-11 flex-shrink-0 flex-grow">
          <Icon name="plus" size={16} />
          New chat
        </a>
        <span>{hideIcon}</span>
      </div>

      <div className="absolute left-0 top-14 z-20 overflow-hidden transition-all duration-500 invisible max-h-0">
        <div className="bg-gray-900 px-4 py-3"></div>
        <div className="h-24 bg-gradient-to-t from-gray-900/0 to-gray-900"></div>
      </div>
    </>
  );
};

export default Header;
