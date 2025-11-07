import type { PokemonType } from "@/types";
import styles from "./TypeChip.module.css";

interface TypeChipProps {
  type: PokemonType;
  variant?: "filled" | "outlined";
  selected?: boolean;
  onClick?: () => void;
}

export default function TypeChip({
  type,
  variant = "filled",
  selected = false,
  onClick,
}: TypeChipProps) {
  const className = [
    styles.chip,
    styles[`chip--${type}`],
    styles[`chip--${variant}`],
    selected ? styles["chip--selected"] : "",
    onClick ? styles["chip--clickable"] : "",
  ]
    .filter(Boolean)
    .join(" ");

  return (
    <span className={className} onClick={onClick}>
      {type}
    </span>
  );
}
