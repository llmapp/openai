import { useEffect, useRef, useState } from "react";

import Icon from "../../../lib/icon";
import UpgradeModal from "../../../Upgrade";
import { useAccountStore } from "../../../../store/account";

const Footer = () => {
  return (
    <div className="border-t border-white/20 pt-2 empty:hidden">
      <Upgrade />
      <Settings />
    </div>
  );
};
export default Footer;

const Upgrade = () => {
  const [show, setShow] = useState<boolean>(false);

  return (
    <>
      {/* <a onClick={() => setShow(true)} className="flex p-3 items-center gap-3 transition-colors duration-200 text-white cursor-pointer text-sm hover:bg-gray-800 rounded-md"> */}
      <a href="https://github.com/huajianmao/openai.mini" className="flex p-3 items-center gap-3 transition-colors duration-200 text-white cursor-pointer text-sm hover:bg-gray-800 rounded-md" target="_blank" rel="noreferrer">
        <span className="flex w-full flex-row justify-between">
          <span className="gold-new-button flex items-center gap-3">
            <Icon name="star" />
            OpenAI.mini
          </span>
          <span className="rounded-md bg-yellow-200 px-1.5 py-0.5 text-xs font-medium uppercase text-gray-800">github</span>
        </span>
      </a>

      {show && <UpgradeModal onClose={() => setShow(false)} />}
    </>
  );
};

const Settings = () => {
  const user = useAccountStore((state) => state.current);

  const ref = useRef<HTMLDivElement>(null);
  const [settings, setSettings] = useState<boolean>(false);

  const toggleSettings = () => {
    setSettings(!settings);
  };

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (ref.current && !ref.current.contains(event.target as Node)) {
        setSettings(false);
      }
    };

    document.addEventListener("mousedown", handleClickOutside);

    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, [ref]);

  return user ? (
    <div className="group relative" ref={ref} data-headlessui-state>
      <button onClick={toggleSettings} className="flex w-full items-center gap-2.5 rounded-md px-3 py-3 text-sm transition-colors duration-200 hover:bg-gray-800 group-ui-open:bg-gray-800">
        <div className="flex-shrink-0">
          <div className="relative flex">
            <span className="relative box-border inline-block overflow-hidden w-[initial] h-[initial] bg-none opacity-100 border-0 m-0 p-0 max-w-full">
              <img className="rounded-sm" src={user.avatar} alt="avatar" width={28} height={28} />
            </span>
          </div>
        </div>
        <div className="grow overflow-hidden text-ellipsis whitespace-nowrap text-left text-white">{user.account}</div>
        <Icon name="dots" color="gray" />
      </button>

      {settings && (
        <div className="absolute bottom-full left-0 z-20 mb-2 w-full overflow-hidden rounded-md bg-gray-950 pb-1.5 pt-1 outline-none opacity-100 translate-y-0" tabIndex={0}>
          <nav role="none">
            <MenuItem icon="help" title="Help &amp; FAQ" />
            <MenuItem icon="settings" title="Settings" />
            <div className="my-1.5 h-px bg-white/20" role="none"></div>
            <MenuItem icon="logout" title="Log out" />
          </nav>
        </div>
      )}
    </div>
  ) : (
    <></>
  );
};

const MenuItem = ({ icon, title }: { icon: string; title: string }) => {
  return (
    <a className="flex p-3 items-center gap-3 transition-colors duration-200 text-white cursor-pointer text-sm hover:bg-gray-700" role="menuitem" tabIndex={-1} data-headlessui-state="">
      <Icon name={icon} /> {title}
    </a>
  );
};
