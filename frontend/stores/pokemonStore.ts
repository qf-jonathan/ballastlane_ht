import { create } from "zustand";
import { apiClient } from "@/lib/api";
import type { PokemonDetails, PokemonListItem } from "@/types";

interface PokemonState {
  pokemonList: PokemonListItem[];
  currentPokemon: PokemonDetails | null;
  isLoading: boolean;
  error: string | null;
  hasMore: boolean;
  offset: number;
  searchQuery: string;
  sortBy: "id" | "name";
  fetchPokemonList: (reset?: boolean) => Promise<void>;
  fetchPokemonDetails: (nameOrId: string) => Promise<void>;
  setSearchQuery: (query: string) => void;
  setSortBy: (sortBy: "id" | "name") => void;
  reset: () => void;
}

export const usePokemonStore = create<PokemonState>((set, get) => ({
  pokemonList: [],
  currentPokemon: null,
  isLoading: false,
  error: null,
  hasMore: true,
  offset: 0,
  searchQuery: "",
  sortBy: "id",

  fetchPokemonList: async (reset = false) => {
    const { offset, searchQuery, sortBy, pokemonList, isLoading } = get();

    if (isLoading) return;

    const currentOffset = reset ? 0 : offset;

    set({ isLoading: true, error: null });

    try {
      const response = await apiClient.getPokemonList(
        currentOffset,
        20,
        searchQuery || undefined,
        sortBy
      );

      const newList = reset ? response.results : [...pokemonList, ...response.results];

      set({
        pokemonList: newList,
        offset: currentOffset + response.results.length,
        hasMore: response.next !== null,
        isLoading: false,
      });
    } catch (error) {
      const errorMessage =
        error instanceof Error ? error.message : "Failed to fetch Pokémon";
      set({ error: errorMessage, isLoading: false });
    }
  },

  fetchPokemonDetails: async (nameOrId: string) => {
    set({ isLoading: true, error: null, currentPokemon: null });
    try {
      const pokemon = await apiClient.getPokemonDetails(nameOrId);
      set({ currentPokemon: pokemon, isLoading: false });
    } catch (error) {
      const errorMessage =
        error instanceof Error ? error.message : "Failed to fetch Pokémon details";
      set({ error: errorMessage, isLoading: false });
    }
  },

  setSearchQuery: (query: string) => {
    set({ searchQuery: query, offset: 0, pokemonList: [] });
  },

  setSortBy: (sortBy: "id" | "name") => {
    set({ sortBy, offset: 0, pokemonList: [] });
  },

  reset: () => {
    set({
      pokemonList: [],
      currentPokemon: null,
      offset: 0,
      searchQuery: "",
      error: null,
      hasMore: true,
    });
  },
}));
