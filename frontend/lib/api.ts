import type {
  AuthToken,
  LoginCredentials,
  PokemonDetails,
  PokemonListResponse,
  User,
} from "@/types";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

class ApiClient {
  private baseUrl: string;

  constructor(baseUrl: string) {
    this.baseUrl = baseUrl;
  }

  private getAuthHeader(): HeadersInit {
    const token = localStorage.getItem("auth_token");
    if (token) {
      return {
        Authorization: `Bearer ${token}`,
      };
    }
    return {};
  }

  private async handleResponse<T>(response: Response): Promise<T> {
    if (!response.ok) {
      const error = await response.json().catch(() => ({
        detail: "An error occurred",
      }));
      throw new Error(error.detail || `HTTP error ${response.status}`);
    }
    return response.json();
  }

  // Auth endpoints
  async login(credentials: LoginCredentials): Promise<AuthToken> {
    const response = await fetch(`${this.baseUrl}/auth/login/json`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(credentials),
    });
    return this.handleResponse<AuthToken>(response);
  }

  async getCurrentUser(): Promise<User> {
    const response = await fetch(`${this.baseUrl}/auth/me`, {
      headers: {
        ...this.getAuthHeader(),
      },
    });
    return this.handleResponse<User>(response);
  }

  // Pokémon endpoints
  async getPokemonList(
    offset: number = 0,
    limit: number = 20,
    query?: string,
    sortBy?: "id" | "name"
  ): Promise<PokemonListResponse> {
    const params = new URLSearchParams({
      offset: offset.toString(),
      limit: limit.toString(),
    });
    if (query) {
      params.append("query", query);
    }
    if (sortBy) {
      params.append("sort_by", sortBy);
    }

    const response = await fetch(`${this.baseUrl}/pokemon?${params}`, {
      headers: {
        ...this.getAuthHeader(),
      },
    });
    return this.handleResponse<PokemonListResponse>(response);
  }

  async getPokemonDetails(nameOrId: string): Promise<PokemonDetails> {
    const response = await fetch(`${this.baseUrl}/pokemon/${nameOrId}`, {
      headers: {
        ...this.getAuthHeader(),
      },
    });
    return this.handleResponse<PokemonDetails>(response);
  }
}

export const apiClient = new ApiClient(API_BASE_URL);
