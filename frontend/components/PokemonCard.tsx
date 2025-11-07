"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import TypeChip from "./TypeChip";
import type { PokemonDetails } from "@/types";
import { apiClient } from "@/lib/api";
import styles from "./PokemonCard.module.css";

interface PokemonCardProps {
  name: string;
  url: string;
}

export default function PokemonCard({ name, url }: PokemonCardProps) {
  const [pokemon, setPokemon] = useState<PokemonDetails | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchPokemon = async () => {
      try {
        const data = await apiClient.getPokemonDetails(name);
        setPokemon(data);
      } catch (error) {
        console.error("Error fetching Pokémon:", error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchPokemon();
  }, [name]);

  if (isLoading) {
    return (
      <div className={styles.card}>
        <div className={styles.loading}>Loading...</div>
      </div>
    );
  }

  if (!pokemon) {
    return null;
  }

  const primaryType = pokemon.types[0]?.type.name;
  const imageUrl =
    pokemon.sprites?.other?.["official-artwork"]?.front_default ||
    pokemon.sprites?.front_default ||
    "/placeholder-pokemon.png";

  return (
    <Link href={`/pokemon/${pokemon.id}`} className={styles.card}>
      <div className={styles.cardInner} data-type={primaryType}>
        <div className={styles.number}>#{String(pokemon.id).padStart(3, "0")}</div>
        <div className={styles.imageContainer}>
          <img
            src={imageUrl}
            alt={pokemon.name}
            className={styles.image}
          />
        </div>
        <h3 className={styles.name}>{pokemon.name}</h3>
        <div className={styles.types}>
          {pokemon.types.map((typeSlot) => (
            <TypeChip key={typeSlot.type.name} type={typeSlot.type.name} />
          ))}
        </div>
      </div>
    </Link>
  );
}
