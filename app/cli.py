import typer
from app.database import create_db_and_tables, get_cli_session, drop_all
from app.models import *
from fastapi import Depends
from sqlmodel import select
from app.utilities import encrypt_password

# ==================== SIR'S ORIGINAL CODE - DO NOT MODIFY ====================

cli = typer.Typer()

@cli.command()
def initialize():
    with get_cli_session() as db:
        drop_all()
        create_db_and_tables()

        # ==================== STUDENT CODE BELOW ====================

        # --- Sample Albums ---
        albums = [
            Album(
                title="Midnight Echoes",
                artist="The Neon Wolves",
                image="https://weblabs.web.app/api/brainrot/1.webp"
            ),
            Album(
                title="Solar Drift",
                artist="Luna Park",
                image="https://weblabs.web.app/api/brainrot/2.webp"
            ),
            Album(
                title="Static Dreams",
                artist="Voltage Kids",
                image="https://weblabs.web.app/api/brainrot/3.webp"
            ),
            Album(
                title="Oceanic",
                artist="Deep Blue Trio",
                image="https://weblabs.web.app/api/brainrot/4.webp"
            ),
        ]

        for album in albums:
            db.add(album)
        db.commit()
        for album in albums:
            db.refresh(album)

        # --- Sample Tracks ---
        tracks = [
            # Album 1
            Track(title="Wolf Run", duration="3:42", album_id=albums[0].id),
            Track(title="Neon Lights", duration="4:10", album_id=albums[0].id),
            Track(title="Midnight Chase", duration="3:55", album_id=albums[0].id),
            # Album 2
            Track(title="Solar Flare", duration="5:01", album_id=albums[1].id),
            Track(title="Orbit", duration="3:30", album_id=albums[1].id),
            Track(title="Drifting", duration="4:22", album_id=albums[1].id),
            # Album 3
            Track(title="Static", duration="2:58", album_id=albums[2].id),
            Track(title="Dream State", duration="4:45", album_id=albums[2].id),
            # Album 4
            Track(title="Deep Blue", duration="6:00", album_id=albums[3].id),
            Track(title="Undertow", duration="3:15", album_id=albums[3].id),
        ]

        for track in tracks:
            db.add(track)
        db.commit()
        for track in tracks:
            db.refresh(track)

        # --- Sample Comments ---
        comments = [
            Comment(content="Absolute banger!", author="Alice", track_id=tracks[0].id),
            Comment(content="Love this track so much.", author="Bob", track_id=tracks[0].id),
            Comment(content="This hits different at night.", author="Carol", track_id=tracks[1].id),
            Comment(content="Solar Flare is a masterpiece.", author="Dave", track_id=tracks[3].id),
            Comment(content="Can't stop replaying this.", author="Eve", track_id=tracks[6].id),
        ]

        for comment in comments:
            db.add(comment)

        # --- Sample Reactions ---
        reactions = [
            Reaction(reaction_type="like", track_id=tracks[0].id),
            Reaction(reaction_type="like", track_id=tracks[0].id),
            Reaction(reaction_type="dislike", track_id=tracks[0].id),
            Reaction(reaction_type="like", track_id=tracks[1].id),
            Reaction(reaction_type="like", track_id=tracks[3].id),
            Reaction(reaction_type="like", track_id=tracks[3].id),
            Reaction(reaction_type="dislike", track_id=tracks[3].id),
            Reaction(reaction_type="like", track_id=tracks[6].id),
        ]

        for reaction in reactions:
            db.add(reaction)

        db.commit()
        typer.secho("Database initialized with sample albums, tracks, comments and reactions!", fg=typer.colors.GREEN)

# ==================== SIR'S ORIGINAL CODE - DO NOT MODIFY ====================

@cli.command()
def test():
    print("You're already in the test")

if __name__ == "__main__":
    cli()