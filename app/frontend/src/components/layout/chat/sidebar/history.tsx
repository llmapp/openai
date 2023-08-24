import Icon from "../../../lib/icon";

import * as API from "../../../../utils/api";
import { useChatStore } from "../../../../store/chat";
import { groupChats } from "../../../../utils/chat";

import type { Chat } from "../../../lib/chat/types";
import type { ChatGroup } from "../../../../utils/chat";
import { useScreenStore } from "../../../../store/screen";

const History = () => {
  const chats = useChatStore((state) => state.chats);
  const { thisMonth, prevMonths, prevYears } = groupChats(chats);

  return (
    <div className="flex-col flex-1 transition-opacity duration-500 overflow-y-auto -mr-6 pr-4">
      <div className="flex flex-col gap-2 pb-2 text-gray-100 text-sm">
        <div>
          <ChatGroups groups={thisMonth} />
          <ChatGroups groups={prevMonths} />
          <ChatGroups groups={prevYears} />
        </div>
      </div>
    </div>
  );
};

export default History;

type ChatGroupsProps = { groups: ChatGroup[] };
const ChatGroups = ({ groups }: ChatGroupsProps) => {
  return (
    <span>
      {(groups ?? [])
        .filter((g) => g.chats?.length > 0)
        .map((group) => {
          return <GroupItem key={group.title} group={group} />;
        })}
    </span>
  );
};

type GroupItemProps = { group: ChatGroup };
const GroupItem = ({ group }: GroupItemProps) => {
  const isScreenSmall = useScreenStore((state) => state.isSmall);
  return (
    <div className="relative h-auto opacity-100 transform-none transition-all duration-500 ease-in-out" style={isScreenSmall ? { marginRight: "20px" } : {}}>
      <div className="sticky top-0 z-[16] transform-none opacity-100 transition-all duration-500 ease-in-out">
        <h3 className="h-9 pb-2 pt-3 px-3 text-xs text-gray-500 font-medium text-ellipsis overflow-hidden break-all bg-gray-900">{group.title}</h3>
      </div>
      <ol>
        {group.chats?.map((chat) => (
          <ChatItem key={chat.id} chat={chat} />
        ))}
      </ol>
    </div>
  );
};

type ChatItemProps = { chat: Chat };
const ChatItem = ({ chat }: ChatItemProps) => {
  const current = useChatStore((state) => state.current);
  const onSelectChat = useChatStore((state) => state.select);
  const onRemoveChat = useChatStore((state) => state.remove);

  const isActive = current.id === chat.id;

  const commonClass = "flex py-3 px-3 items-center gap-3 relative rounded-md cursor-pointer break-all group mr-1";
  const activeClass = `${commonClass} pr-[3.5rem] bg-gray-800 hover:bg-gray-800`;
  const inactiveClass = `${commonClass} hover:bg-[#2A2B32] hover:pr-4 bg-gray-900`;

  const commonTailClass = "absolute inset-y-0 right-0 w-8 z-10 bg-gradient-to-l group-hover:from-[#2A2B32]";
  const activeTailClass = `${commonTailClass} from-gray-800`;
  const inactiveTailClass = `${commonTailClass} from-gray-900`;

  const handleRemoveChat = async () => {
    await API.chat.delete(chat.id, "message");
    onRemoveChat(chat);
  };

  return (
    <li onClick={() => onSelectChat(chat)} className="relative z-[15] opacity-100 h-auto transform-none transition-all duration-500 ease-in-out">
      <a className={isActive ? activeClass : inactiveClass}>
        <Icon name="message" />

        <div className="flex-1 text-ellipsis max-h-5 overflow-hidden break-all relative">
          <div className="flex-1 text-ellipsis max-h-5 overflow-hidden break-all relative">
            {chat.title}
            <div className="absolute inset-y-0 right-0 w-8 z-10 bg-gradient-to-l from-gray-800"></div>
          </div>
          <div className={isActive ? activeTailClass : inactiveTailClass}></div>
        </div>

        {isActive && (
          <div className="absolute flex right-1 z-10 text-gray-300">
            <button className="p-1 hover:text-white">
              <Icon name="edit" />
            </button>
            {/*
            <button className="p-1 hover:text-white">
              <Icon name="share" />
            </button>
            */}
            <button className="p-1 hover:text-white" onClick={handleRemoveChat}>
              <Icon name="delete" />
            </button>
          </div>
        )}
      </a>
    </li>
  );
};
