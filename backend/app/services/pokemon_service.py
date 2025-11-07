from typing import List, Optional

from fastapi import HTTPException, status

from app.models.pokemon import Pokemon
from app.schemas.pokemon import PokemonDetails, PokemonListItem, PokemonListResponse


class PokemonService:
    """Service for managing Pokemon data from database."""

    @staticmethod
    async def get_pokemon_details(name_or_id: str) -> PokemonDetails:
        """
        Get detailed information about a specific Pokemon from database.

        Args:
            name_or_id: Pokemon name or ID

        Returns:
            PokemonDetails with full Pokemon information
        """
        try:
            # Try to find by ID if it's numeric, otherwise by name
            if name_or_id.isdigit():
                pokemon = await Pokemon.filter(id=int(name_or_id)).first()
            else:
                pokemon = await Pokemon.filter(name=name_or_id.lower()).first()

            if not pokemon:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Pokemon '{name_or_id}' not found",
                )

            # Transform database data to match the schema
            pokemon_data = {
                "id": pokemon.id,
                "name": pokemon.name,
                "description": pokemon.description,
                "sprite": pokemon.sprite_official_artwork or pokemon.sprite_front_default,
                "sprites": {
                    "front_default": pokemon.sprite_front_default,
                    "other": {
                        "official_artwork": {
                            "front_default": pokemon.sprite_official_artwork
                        }
                    },
                },
                "types": [
                    {"type": {"name": type_name}} for type_name in pokemon.types
                ],
                "height": pokemon.height,
                "weight": pokemon.weight,
                "abilities": [
                    {"ability": {"name": ability_name}} for ability_name in pokemon.abilities
                ],
                "stats": [
                    {"base_stat": stat["base_stat"], "stat": {"name": stat["name"]}}
                    for stat in pokemon.stats
                ],
            }

            return PokemonDetails(**pokemon_data)
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error: {str(e)}",
            )

    @staticmethod
    async def search_pokemon(
        query: str | None = None, offset: int = 0, limit: int = 20, sort_by: str = "id"
    ) -> PokemonListResponse:
        """
        Search for Pokemon by name or ID with pagination using database.
        If query is None or empty, returns all Pokemon.

        Args:
            query: Optional search query (name or ID). If None/empty, returns all Pokemon
            offset: Number of results to skip
            limit: Number of results to return
            sort_by: Field to sort by ('id' or 'name')

        Returns:
            PokemonListResponse with filtered and paginated results
        """
        try:
            # If no query provided, return all Pokemon (same as get_pokemon_list)
            if not query:
                total_count = await Pokemon.all().count()
                pokemon_list = await Pokemon.all().offset(offset).limit(limit).order_by(sort_by)

                results = [
                    PokemonListItem(
                        id=p.id,
                        name=p.name,
                        url=f"/pokemon/{p.id}",
                        sprite=p.sprite_front_default,
                        types=p.types,
                    )
                    for p in pokemon_list
                ]

                next_url = None
                previous_url = None

                if offset + limit < total_count:
                    next_url = f"offset={offset + limit}&limit={limit}"

                if offset > 0:
                    prev_offset = max(0, offset - limit)
                    previous_url = f"offset={prev_offset}&limit={limit}"

                return PokemonListResponse(
                    count=total_count,
                    next=next_url,
                    previous=previous_url,
                    results=results,
                )

            # If query is numeric, try direct ID lookup first
            if query.isdigit():
                try:
                    pokemon = await PokemonService.get_pokemon_details(query)
                    return PokemonListResponse(
                        count=1,
                        next=None,
                        previous=None,
                        results=[
                            PokemonListItem(
                                id=pokemon.id,
                                name=pokemon.name,
                                url=f"/pokemon/{pokemon.id}",
                                sprite=pokemon.sprites.other.official_artwork.front_default
                                or pokemon.sprites.front_default,
                                types=[t.type.name for t in pokemon.types],
                            )
                        ],
                    )
                except HTTPException:
                    # If not found, continue with name search
                    pass

            # Search database for Pokemon matching the query
            query_lower = query.lower()

            # Get total count of matching Pokemon
            total_count = await Pokemon.filter(name__icontains=query_lower).count()

            # Get paginated results with sorting
            matching_pokemon = (
                await Pokemon.filter(name__icontains=query_lower)
                .offset(offset)
                .limit(limit)
                .order_by(sort_by)
            )

            # Build results
            results = [
                PokemonListItem(
                    id=p.id,
                    name=p.name,
                    url=f"/pokemon/{p.id}",
                    sprite=p.sprite_front_default,
                    types=p.types,
                )
                for p in matching_pokemon
            ]

            # Build next/previous URLs
            next_url = None
            previous_url = None

            if offset + limit < total_count:
                next_url = f"offset={offset + limit}&limit={limit}"

            if offset > 0:
                prev_offset = max(0, offset - limit)
                previous_url = f"offset={prev_offset}&limit={limit}"

            return PokemonListResponse(
                count=total_count,
                next=next_url,
                previous=previous_url,
                results=results,
            )

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error: {str(e)}",
            )
