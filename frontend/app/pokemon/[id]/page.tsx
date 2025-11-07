"use client";

import { useEffect } from "react";
import { useParams, useRouter } from "next/navigation";
import { usePokemonStore } from "@/stores/pokemonStore";
import { useAuthStore } from "@/stores/authStore";
import TypeChip from "@/components/TypeChip";
import styles from "./page.module.css";

export default function PokemonDetailsPage() {
  const params = useParams();
  const router = useRouter();
  const { currentPokemon, isLoading, error, fetchPokemonDetails } = usePokemonStore();
  const { isAuthenticated, checkAuth } = useAuthStore();

  useEffect(() => {
    checkAuth();
  }, [checkAuth]);

  useEffect(() => {
    if (params.id && isAuthenticated) {
      fetchPokemonDetails(params.id as string);
    }
  }, [params.id, fetchPokemonDetails, isAuthenticated]);

  if (!isAuthenticated) {
    router.push("/");
    return null;
  }

  if (isLoading) {
    return (
      <div className={styles.loading}>
        <div className={styles.spinner}></div>
        <p>Loading Pokémon details...</p>
      </div>
    );
  }

  if (error || !currentPokemon) {
    return (
      <div className={styles.error}>
        <p>{error || "Pokémon not found"}</p>
        <button onClick={() => router.push("/")} className={styles.backButton}>
          Back to Pokédex
        </button>
      </div>
    );
  }

  const primaryType = currentPokemon.types[0]?.type.name;
  const typeColorVar = `--color-${primaryType}`;
  const imageUrl =
    currentPokemon.sprites?.other?.["official-artwork"]?.front_default ||
    currentPokemon.sprites?.front_default ||
    "/placeholder-pokemon.png";

  return (
    <div className={styles.page}>
      <div
        className={styles.header}
        style={{ backgroundColor: `var(${typeColorVar})` }}
      >
        <div className={styles.headerContent}>
          <button onClick={() => router.back()} className={styles.backButton}>
            <svg
              width="24"
              height="24"
              viewBox="0 0 24 24"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                d="M19 12H5M5 12L12 19M5 12L12 5"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
            </svg>
          </button>
          <h1 className={styles.name}>{currentPokemon.name}</h1>
          <div className={styles.number}>
            #{String(currentPokemon.id).padStart(3, "0")}
          </div>
        </div>
        <div className={styles.imageContainer}>
          <img
            src={imageUrl}
            alt={currentPokemon.name}
            className={styles.image}
          />
        </div>
      </div>

      <div className={styles.content}>
        <div className={styles.types}>
          {currentPokemon.types.map((typeSlot) => (
            <TypeChip key={typeSlot.type.name} type={typeSlot.type.name} />
          ))}
        </div>

        <section className={styles.section}>
          <h2
            className={styles.sectionTitle}
            style={{ color: `var(${typeColorVar})` }}
          >
            About
          </h2>
          <div className={styles.infoGrid}>
            <div className={styles.infoItem}>
              <span className={styles.infoLabel}>Height</span>
              <span className={styles.infoValue}>
                {(currentPokemon.height / 10).toFixed(1)} m
              </span>
            </div>
            <div className={styles.infoItem}>
              <span className={styles.infoLabel}>Weight</span>
              <span className={styles.infoValue}>
                {(currentPokemon.weight / 10).toFixed(1)} kg
              </span>
            </div>
            <div className={styles.infoItem}>
              <span className={styles.infoLabel}>Abilities</span>
              <span className={styles.infoValue}>
                {currentPokemon.abilities
                  .filter((a) => !a.is_hidden)
                  .map((a) => a.ability.name)
                  .join(", ")}
              </span>
            </div>
          </div>
        </section>

        <section className={styles.section}>
          <h2
            className={styles.sectionTitle}
            style={{ color: `var(${typeColorVar})` }}
          >
            Base Stats
          </h2>
          <div className={styles.stats}>
            {currentPokemon.stats.map((stat) => {
              const statName = stat.stat.name
                .replace("special-", "Sp. ")
                .replace("-", " ")
                .replace(/\b\w/g, (l) => l.toUpperCase());
              const percentage = (stat.base_stat / 255) * 100;

              return (
                <div key={stat.stat.name} className={styles.statRow}>
                  <span className={styles.statName}>{statName}</span>
                  <span className={styles.statValue}>{stat.base_stat}</span>
                  <div className={styles.statBarContainer}>
                    <div
                      className={styles.statBar}
                      style={{
                        width: `${percentage}%`,
                        backgroundColor: `var(${typeColorVar})`,
                      }}
                    />
                  </div>
                </div>
              );
            })}
          </div>
        </section>
      </div>
    </div>
  );
}
