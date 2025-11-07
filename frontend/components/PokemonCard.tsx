"use client";

import Link from "next/link";
import TypeChip from "./TypeChip";
import type { PokemonListItem, PokemonType } from "@/types";
import styles from "./PokemonCard.module.css";

interface PokemonCardProps {
  pokemon: PokemonListItem;
}

export default function PokemonCard({ pokemon }: PokemonCardProps) {
  const primaryType = pokemon.types[0];
  const imageUrl = pokemon.sprite || "/placeholder-pokemon.png";

  return (
    <Link href={`/pokemon/${pokemon.id}`} className={styles.card}>
      <div className={styles.cardInner} data-type={primaryType}>
        <div className={styles.number}>#{String(pokemon.id).padStart(3, "0")}</div>
        <div className={styles.imageContainer}>
          <div className={styles.ground}>
            <h3 className={styles.name}>{pokemon.name}</h3>
          </div>
          <img
            src={imageUrl}
            alt={pokemon.name}
            className={styles.image}
          />
        </div>
        
        {/* <div className={styles.types}>
          {pokemon.types.map((type) => (
            <TypeChip key={type} type={type as PokemonType} />
          ))}
        </div> */}
      </div>
    </Link>
  );
}
