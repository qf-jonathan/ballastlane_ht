from tortoise import fields
from tortoise.models import Model


class Pokemon(Model):
    """Pokemon model for storing Pokemon data."""

    id = fields.IntField(primary_key=True)
    name = fields.CharField(max_length=100, unique=True, index=True)
    height = fields.IntField()
    weight = fields.IntField()
    description = fields.TextField(null=True)  # Pokemon description from species
    sprite_front_default = fields.CharField(max_length=500, null=True)
    sprite_official_artwork = fields.CharField(max_length=500, null=True)
    # Store types, abilities, and stats as JSON fields
    types = fields.JSONField()  # List of type names
    abilities = fields.JSONField()  # List of ability names
    stats = fields.JSONField()  # List of stat objects with name and base_stat
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "pokemon"

    def __str__(self):
        return f"Pokemon(id={self.id}, name={self.name})"
