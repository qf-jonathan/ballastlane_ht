from typing import List

from pydantic import BaseModel


class PokemonListItem(BaseModel):
    """Schema for Pokemon in list view."""

    id: int
    name: str
    url: str
    sprite: str | None
    types: List[str]


class PokemonListResponse(BaseModel):
    """Schema for paginated Pokemon list response."""

    count: int
    next: str | None
    previous: str | None
    results: List[PokemonListItem]


class PokemonSprite(BaseModel):
    """Schema for Pokemon sprite."""

    front_default: str | None


class OfficialArtwork(BaseModel):
    """Schema for official artwork."""

    front_default: str | None


class OtherSprites(BaseModel):
    """Schema for other sprites."""

    official_artwork: OfficialArtwork = {"front_default": None}


class PokemonSprites(BaseModel):
    """Schema for Pokemon sprites."""

    front_default: str | None
    other: OtherSprites = {"official_artwork": {"front_default": None}}


class PokemonType(BaseModel):
    """Schema for Pokemon type."""

    name: str


class PokemonTypeSlot(BaseModel):
    """Schema for Pokemon type slot."""

    type: PokemonType


class PokemonAbility(BaseModel):
    """Schema for Pokemon ability."""

    name: str


class PokemonAbilitySlot(BaseModel):
    """Schema for Pokemon ability slot."""

    ability: PokemonAbility


class PokemonStat(BaseModel):
    """Schema for Pokemon stat."""

    name: str


class PokemonStatValue(BaseModel):
    """Schema for Pokemon stat value."""

    base_stat: int
    stat: PokemonStat


class PokemonDetails(BaseModel):
    """Schema for detailed Pokemon information."""

    id: int
    name: str
    description: str | None  # Pokemon description from species
    sprite: str | None  # Primary sprite (same as list view)
    sprites: PokemonSprites
    types: List[PokemonTypeSlot]
    height: int
    weight: int
    abilities: List[PokemonAbilitySlot]
    stats: List[PokemonStatValue]
