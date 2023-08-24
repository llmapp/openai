import Icon from "../icon";

type BannerProps = {
  title: string;
  examples: string[];
  capabilities: string[];
  limitations: string[];

  onClickExample: (example: string) => void;
};

const Banner = ({ title, examples, capabilities, limitations, onClickExample }: BannerProps) => {
  return (
    <>
      <div className="w-full h-24">{/* <Selection /> */}</div>

      <div className="text-gray-800 w-full mx-auto md:max-w-2xl lg:max-w-3xl md:h-full md:flex md:flex-col px-6">
        <h1 className="text-4xl font-semibold text-center mt-6 sm:mt-[6vh] ml-auto mr-auto mb-4 sm:mb-16 flex gap-2 items-center justify-center">{title}</h1>
        <div className="md:flex items-start text-center gap-3.5">
          <ItemList title="Examples" icon="sun" items={examples} onClick={onClickExample} />
          <ItemList title="Capabilities" icon="thunder-o" items={capabilities} />
          <ItemList title="Limitations" icon="warn" items={limitations} />
        </div>
      </div>
    </>
  );
};

export default Banner;

type ListProps = { title: string; icon: string; items: string[]; onClick?: (item: string) => void };

const ItemList = ({ title, icon, items, onClick }: ListProps) => {
  return (
    <div className="flex flex-col mb-8 md:mb-auto gap-3.5 flex-1">
      <h2 className="flex gap-3 items-center m-auto text-lg font-normal md:flex-col md:gap-2">
        <div className="w-6 h-6 flex items-center justify-center">
          <Icon name={icon} />
        </div>
        {title}
      </h2>
      <ul className="flex flex-col gap-3.5 w-full sm:max-w-md m-auto">
        {items.map((item, index) =>
          !onClick ? (
            <div key={index} className="w-full bg-gray-50 p-3 rounded-md hover:bg-gray-200 text-sm cursor-default">
              {item}
            </div>
          ) : (
            <button key={index} className="w-full bg-gray-50 p-3 rounded-md hover:bg-gray-200 text-sm" onClick={() => onClick(item)}>
              &quot;{item}&quot; →
            </button>
          )
        )}
      </ul>
    </div>
  );
};
