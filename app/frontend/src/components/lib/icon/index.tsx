import icons from "./path";

declare type IconProps = {
  name: string;
  size?: number;
  color?: string;
  onClick?: () => void;
};

const Icon = ({ name, size = 20, color, onClick }: IconProps) => {
  const svg = icons[name] || {};
  const scale = svg.scale ?? 1.0;

  return (
    <div style={color ? { color } : {}} onClick={onClick}>
      <svg width={size * scale} height={size * scale} strokeWidth={svg.stroke && svg.stroke !== 0 ? `${svg.stroke}` : "1.5"} stroke={svg.stroke === false || svg.stroke === 0 ? "transparent" : "currentColor"} strokeLinecap="round" strokeLinejoin="round" fill={svg.fill ? "currentColor" : "transparent"} viewBox={svg.viewBox || "0 0 32 32"}>
        {svg.path}
      </svg>
    </div>
  );
};

export default Icon;
