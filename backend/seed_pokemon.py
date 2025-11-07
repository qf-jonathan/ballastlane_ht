"""
Script to fetch all Pokemon from PokeAPI and populate the database.
Based on the search_pokemon logic that fetches all Pokemon.
"""

import asyncio
import httpx
from tortoise import Tortoise

from app.core.config import settings
from app.models.pokemon import Pokemon


async def fetch_pokemon_details(client: httpx.AsyncClient, pokemon_id: int) -> dict | None:
    """Fetch detailed information for a single Pokemon."""
    try:
        response = await client.get(
            f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}",
            timeout=10.0,
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching Pokemon {pokemon_id}: {e}")
        return None


async def fetch_pokemon_species(client: httpx.AsyncClient, pokemon_id: int) -> dict | None:
    """Fetch species information for a single Pokemon to get description."""
    try:
        response = await client.get(
            f"https://pokeapi.co/api/v2/pokemon-species/{pokemon_id}",
            timeout=10.0,
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching Pokemon species {pokemon_id}: {e}")
        return None


def extract_english_description(species_data: dict) -> str | None:
    """Extract the first English flavor text entry from species data."""
    if not species_data or "flavor_text_entries" not in species_data:
        return None

    for entry in species_data["flavor_text_entries"]:
        if entry.get("language", {}).get("name") == "en":
            # Clean up the text (remove newlines and form feeds)
            text = entry.get("flavor_text", "")
            text = text.replace("\n", " ").replace("\f", " ")
            # Replace multiple spaces with single space
            text = " ".join(text.split())
            return text

    return None


async def seed_pokemon():
    """Fetch all Pokemon from PokeAPI and store in database."""
    # Initialize database
    await Tortoise.init(
        db_url=settings.DATABASE_URL,
        modules={"models": ["app.models.user", "app.models.pokemon"]},
    )
    await Tortoise.generate_schemas()

    print("Starting Pokemon backup from PokeAPI...")

    try:
        async with httpx.AsyncClient() as client:
            # First, get the list of all Pokemon
            print("Fetching Pokemon list...")
            response = await client.get(
                "https://pokeapi.co/api/v2/pokemon",
                params={"limit": 2000},  # Fetch all Pokemon
                timeout=15.0,
            )
            response.raise_for_status()
            data = response.json()

            total_pokemon = len(data["results"])
            print(f"Found {total_pokemon} Pokemon to backup")

            # Fetch details for each Pokemon
            for idx, pokemon_item in enumerate(data["results"], 1):
                # Extract ID from URL
                pokemon_id = int(pokemon_item["url"].split("/")[-2])

                print(f"[{idx}/{total_pokemon}] Fetching details for {pokemon_item['name']}...")

                # Fetch both pokemon details and species data
                details = await fetch_pokemon_details(client, pokemon_id)
                if not details:
                    continue

                species_data = await fetch_pokemon_species(client, pokemon_id)
                description = extract_english_description(species_data) if species_data else None

                # Extract and transform data
                types = [t["type"]["name"] for t in details["types"]]
                abilities = [a["ability"]["name"] for a in details["abilities"]]
                stats = [
                    {
                        "name": s["stat"]["name"],
                        "base_stat": s["base_stat"]
                    }
                    for s in details["stats"]
                ]

                sprite_front = details["sprites"].get("front_default")
                sprite_artwork = (
                    details["sprites"]
                    .get("other", {})
                    .get("official-artwork", {})
                    .get("front_default")
                )

                # Check if Pokemon exists
                exists = await Pokemon.filter(id=details["id"]).exists()

                if exists:
                    # Update existing Pokemon using queryset update
                    await Pokemon.filter(id=details["id"]).update(
                        name=details["name"],
                        height=details["height"],
                        weight=details["weight"],
                        description=description,
                        sprite_front_default=sprite_front,
                        sprite_official_artwork=sprite_artwork,
                        types=types,
                        abilities=abilities,
                        stats=stats,
                    )
                    print(f"[{idx}/{total_pokemon}] ✓ Updated {pokemon_item['name']}")
                else:
                    # Create new Pokemon
                    await Pokemon.create(
                        id=details["id"],
                        name=details["name"],
                        height=details["height"],
                        weight=details["weight"],
                        description=description,
                        sprite_front_default=sprite_front,
                        sprite_official_artwork=sprite_artwork,
                        types=types,
                        abilities=abilities,
                        stats=stats,
                    )
                    print(f"[{idx}/{total_pokemon}] ✓ Created {pokemon_item['name']}")

                # Add a small delay to avoid overwhelming the API
                if idx % 10 == 0:
                    await asyncio.sleep(0.5)

        print(f"\n✓ Successfully backed up {total_pokemon} Pokemon to database!")

    except Exception as e:
        print(f"\n✗ Error during backup: {e}")
        raise
    finally:
        await Tortoise.close_connections()


if __name__ == "__main__":
    asyncio.run(seed_pokemon())
