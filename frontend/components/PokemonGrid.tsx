"use client";

import { useEffect, useRef, useCallback } from "react";
import { usePokemonStore } from "@/stores/pokemonStore";
import PokemonCard from "./PokemonCard";
import SearchBar from "./SearchBar";
import SortDropdown from "./SortDropdown";
import styles from "./PokemonGrid.module.css";

export default function PokemonGrid() {
  const {
    pokemonList,
    isLoading,
    error,
    hasMore,
    fetchPokemonList,
    setSearchQuery,
    setSortBy,
    searchQuery,
    sortBy,
  } = usePokemonStore();

  const observerRef = useRef<IntersectionObserver | null>(null);
  const loadMoreRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    fetchPokemonList(true);
  }, [searchQuery, sortBy]);

  const handleSearch = useCallback(
    (query: string) => {
      setSearchQuery(query);
    },
    [setSearchQuery]
  );

  const handleSortChange = useCallback(
    (newSortBy: "id" | "name") => {
      setSortBy(newSortBy);
    },
    [setSortBy]
  );

  useEffect(() => {
    if (isLoading || !hasMore) return;

    observerRef.current = new IntersectionObserver(
      (entries) => {
        if (entries[0].isIntersecting && hasMore && !isLoading) {
          fetchPokemonList(false);
        }
      },
      { threshold: 0.1 }
    );

    if (loadMoreRef.current) {
      observerRef.current.observe(loadMoreRef.current);
    }

    return () => {
      if (observerRef.current) {
        observerRef.current.disconnect();
      }
    };
  }, [isLoading, hasMore, fetchPokemonList]);

  return (
    <div className={styles.container}>
      <div className={styles.controls}>
        <div className={styles.controlsWrapper}>
          <SearchBar onSearch={handleSearch} />
          <SortDropdown value={sortBy} onChange={handleSortChange} />
        </div>
      </div>

      {error && <div className={styles.error}>{error}</div>}

      <div className={styles.grid}>
        {pokemonList.map((pokemon) => (
          <PokemonCard key={pokemon.id} pokemon={pokemon} />
        ))}
      </div>

      {isLoading && (
        <div className={styles.loading}>
          <div className={styles.spinner}></div>
          <p>Loading Pokémon...</p>
        </div>
      )}

      {!isLoading && pokemonList.length === 0 && !error && (
        <div className={styles.empty}>No Pokémon found</div>
      )}

      {hasMore && !isLoading && <div ref={loadMoreRef} className={styles.loadMore} />}
    </div>
  );
}
