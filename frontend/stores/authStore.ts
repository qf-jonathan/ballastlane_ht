import { create } from "zustand";
import { apiClient } from "@/lib/api";
import type { User, LoginCredentials } from "@/types";

interface AuthState {
  user: User | null;
  token: string | null;
  isLoading: boolean;
  error: string | null;
  isAuthenticated: boolean;
  login: (credentials: LoginCredentials) => Promise<void>;
  logout: () => void;
  checkAuth: () => Promise<void>;
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  token: null,
  isLoading: false,
  error: null,
  isAuthenticated: false,

  login: async (credentials: LoginCredentials) => {
    set({ isLoading: true, error: null });
    try {
      const tokenResponse = await apiClient.login(credentials);
      localStorage.setItem("auth_token", tokenResponse.access_token);

      const user = await apiClient.getCurrentUser();

      set({
        token: tokenResponse.access_token,
        user,
        isAuthenticated: true,
        isLoading: false,
        error: null,
      });
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : "Login failed";
      set({
        error: errorMessage,
        isLoading: false,
        isAuthenticated: false,
        user: null,
        token: null,
      });
      localStorage.removeItem("auth_token");
      throw error;
    }
  },

  logout: () => {
    localStorage.removeItem("auth_token");
    set({
      user: null,
      token: null,
      isAuthenticated: false,
      error: null,
    });
  },

  checkAuth: async () => {
    const token = localStorage.getItem("auth_token");
    if (!token) {
      set({ isAuthenticated: false, user: null, token: null });
      return;
    }

    set({ isLoading: true });
    try {
      const user = await apiClient.getCurrentUser();
      set({
        user,
        token,
        isAuthenticated: true,
        isLoading: false,
        error: null,
      });
    } catch (error) {
      localStorage.removeItem("auth_token");
      set({
        user: null,
        token: null,
        isAuthenticated: false,
        isLoading: false,
      });
    }
  },
}));
