import { useEffect, useRef } from "react";

import Icon from "./lib/icon";

const Upgrade = ({ onClose }: { onClose: () => void }) => {
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (ref.current && !ref.current.contains(event.target as Node)) {
        onClose();
      }
    };

    document.addEventListener("mousedown", handleClickOutside);

    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, [ref, onClose]);

  return (
    <div className="absolute insect-0 z-20">
      <div data-state="open" className="fixed inset-0 bg-gray-500/90 pointer-events-auto">
        <div className="grid-cols-[10px_1fr_10px] grid h-full w-full grid-rows-[minmax(10px,_1fr)_auto_minmax(10px,_1fr)] md:grid-rows-[minmax(20px,_1fr)_auto_minmax(20px,_1fr)] overflow-y-auto">
          <div className="relative col-auto col-start-2 row-auto row-start-2 w-full rounded-lg text-left transition-all left-1/2 -translate-x-1/2 bg-white !bg-transparent md:w-[672px] lg:w-[896px] xl:w-[1024px] pointer-events-auto" tabIndex={-1}>
            <div className="">
              <div className="focus-none flex h-full flex-col items-center justify-start outline-none">
                <div ref={ref} className="relative">
                  <div className="flex grow justify-center bg-white rounded-md flex-col items-start overflow-hidden border shadow-md">
                    <div className="flex w-full flex-row items-center justify-between border-b px-4 py-3">
                      <span className="text-base font-semibold sm:text-base">Your plan</span>
                      <button className="text-gray-700 opacity-50 transition hover:opacity-75" onClick={() => onClose()}>
                        <Icon name="close" />
                      </button>
                    </div>
                    <div className="grid sm:grid-cols-2">
                      <div className="relative order-2 col-span-1 border-r-0 border-t sm:order-1 sm:border-r sm:border-t-0">
                        <Plan plan={plans.free} />
                      </div>
                      <div className="relative order-1 col-span-1 sm:order-2">
                        <Plan plan={plans.plus} active />
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              <div className="mt-5 sm:mt-4"></div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Upgrade;

type PlanType = {
  title: string;
  features: string[];
  price?: string;
  note?: { title: string; url: string };
};

const Plan = ({ plan, active }: { plan: PlanType; active?: boolean }) => {
  return (
    <div className="p-4 flex flex-col gap-3 bg-white z-20 relative">
      <div className="text-xl font-semibold justify-between items-center flex">
        <span>{plan.title}</span>
        {plan.price && <span className="font-semibold text-gray-500">{plan.price}</span>}
      </div>
      <button className={active ? "rounded-md bg-green-700 text-white  btn relative btn-primary border-none py-3 font-semibold" : "rounded-md opacity-50 cursor-not-allowed btn relative btn-primary border-none bg-gray-300 py-3 font-semibold text-gray-800"} disabled>
        <div className="flex w-full gap-2 items-center justify-center">
          <span className="inline-block">{active ? "Upgrade to Plus" : "Your current plan"}</span>
        </div>
      </button>
      {plan.features.map((feature, i) => (
        <Feature key={i} title={feature} active={active} />
      ))}
      {plan.note && (
        <a target="_blank" href={plan.note.url}>
          <div className="gap-2 flex flex-row justify-start text-sm items-start sm:pb-1">
            <div className="flex flex-row items-center space-x-1 underline">
              <span>{plan.note.title}</span>
            </div>
          </div>
        </a>
      )}
    </div>
  );
};

const Feature = ({ title, active }: { title: string; active?: boolean }) => {
  return (
    <div className="gap-2 flex flex-row justify-start text-sm items-start">
      <span className={active ? "text-green-600" : "text-gray-400"}>
        <Icon name="check" size={26} />
      </span>
      <span className="max-w-[250px]">{title}</span>
    </div>
  );
};

const plans = {
  free: {
    title: "Free plan",
    features: ["Access to our GPT-3.5 model", "Standard response speed", "Regular model updates"],
  },
  plus: {
    title: "ChatGPT Plus",
    price: "USD $20/mo",
    features: ["Access to GPT-4, our most capable model", "Faster response speed", "Exclusive access to beta features like Browsing, Plugins, and Code Interpreter"],
    note: {
      title: "I need help with a billing issue",
      url: "https://help.openai.com/en/collections/3943089-billing",
    },
  },
};
