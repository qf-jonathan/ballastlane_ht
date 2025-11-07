from typing import Literal, Optional

from fastapi import APIRouter, Query

from app.schemas.pokemon import PokemonDetails, PokemonListResponse
from app.services.pokemon_service import PokemonService

router = APIRouter(prefix="/pokemon", tags=["pokemon"])


@router.get("/", response_model=PokemonListResponse)
async def get_pokemon_list(
    query: Optional[str] = Query(
        None, description="Search query to filter Pokemon by name or ID"
    ),
    offset: int = Query(0, ge=0, description="Number of Pokemon to skip"),
    limit: int = Query(20, ge=1, le=100, description="Number of Pokemon to return"),
    sort_by: Literal["id", "name"] = Query(
        "id", description="Sort Pokemon by ID or name"
    ),
):
    """
    Get a paginated list of Pokemon from PokeAPI, with optional search/filter.

    Args:
        query: Optional search query to filter by name or ID
        offset: Number of Pokemon to skip (default: 0)
        limit: Number of Pokemon to return (default: 20, max: 100)
        sort_by: Sort by 'id' or 'name' (default: 'id')

    Returns:
        Paginated list of Pokemon with name and URL
    """
    return await PokemonService.search_pokemon(
        query=query, offset=offset, limit=limit, sort_by=sort_by
    )


@router.get("/{name_or_id}", response_model=PokemonDetails)
async def get_pokemon_details(name_or_id: str):
    """
    Get detailed information about a specific Pokemon.

    Args:
        name_or_id: Pokemon name (e.g., "pikachu") or ID (e.g., "25")

    Returns:
        Detailed Pokemon information including sprites, types, abilities, and stats
    """
    return await PokemonService.get_pokemon_details(name_or_id=name_or_id)
