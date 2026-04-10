from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, List

# ==================== SIR'S ORIGINAL CODE - DO NOT MODIFY ====================

class NotFound(Exception):
    pass

# ==================== STUDENT CODE BELOW ====================

class Album(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    artist: str
    image: str

    # Relationship: one album has many tracks
    tracks: List["Track"] = Relationship(back_populates="album")


class Track(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    duration: str  # e.g. "3:45"
    album_id: int = Field(foreign_key="album.id")

    # Relationships
    album: Optional[Album] = Relationship(back_populates="tracks")
    comments: List["Comment"] = Relationship(back_populates="track")
    reactions: List["Reaction"] = Relationship(back_populates="track")

    @property
    def likes(self) -> int:
        return sum(1 for r in self.reactions if r.reaction_type == "like")

    @property
    def dislikes(self) -> int:
        return sum(1 for r in self.reactions if r.reaction_type == "dislike")


class Comment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    content: str
    author: str
    track_id: int = Field(foreign_key="track.id")

    # Relationship
    track: Optional[Track] = Relationship(back_populates="comments")


class Reaction(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    reaction_type: str  # "like" or "dislike"
    track_id: int = Field(foreign_key="track.id")

    # Relationship
    track: Optional[Track] = Relationship(back_populates="reactions")