from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlmodel import Session, select
from app.database import create_db_and_tables, get_session
from app.models import Album, Track, Comment, Reaction
from contextlib import asynccontextmanager
from fastapi import status
from typing import Annotated

# ==================== SIR'S ORIGINAL CODE - DO NOT MODIFY ====================

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

templates = Jinja2Templates(directory="app/templates")

app.mount("/static", StaticFiles(directory="app/static"), name="static")

# ==================== STUDENT CODE BELOW ====================

SessionDep = Annotated[Session, Depends(get_session)]

@app.get("/", response_class=HTMLResponse)
async def index(request: Request, db: SessionDep):
    """Home page - display all albums"""
    albums = db.exec(select(Album)).all()
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "albums": albums,
            "selected_album": None,
            "selected_track": None,
            "tracks": [],
            "comments": [],
            "likes": 0,
            "dislikes": 0,
        }
    )


@app.get("/albums/{album_id}", response_class=HTMLResponse)
async def view_album(request: Request, album_id: int, db: SessionDep):
    """View a specific album and its tracks"""
    albums = db.exec(select(Album)).all()
    album = db.get(Album, album_id)

    if not album:
        return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)

    tracks = db.exec(select(Track).where(Track.album_id == album_id)).all()

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "albums": albums,
            "selected_album": album,
            "selected_track": None,
            "tracks": tracks,
            "comments": [],
            "likes": 0,
            "dislikes": 0,
        }
    )


@app.get("/albums/{album_id}/tracks/{track_id}", response_class=HTMLResponse)
async def view_track(request: Request, album_id: int, track_id: int, db: SessionDep):
    """View a specific track with its comments and reactions"""
    albums = db.exec(select(Album)).all()
    album = db.get(Album, album_id)
    track = db.get(Track, track_id)

    if not album or not track:
        return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)

    tracks = db.exec(select(Track).where(Track.album_id == album_id)).all()
    comments = db.exec(select(Comment).where(Comment.track_id == track_id)).all()

    likes = db.exec(
        select(Reaction).where(Reaction.track_id == track_id, Reaction.reaction_type == "like")
    ).all()
    dislikes = db.exec(
        select(Reaction).where(Reaction.track_id == track_id, Reaction.reaction_type == "dislike")
    ).all()

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "albums": albums,
            "selected_album": album,
            "selected_track": track,
            "tracks": tracks,
            "comments": comments,
            "likes": len(likes),
            "dislikes": len(dislikes),
        }
    )


@app.post("/albums/{album_id}/tracks/{track_id}/comment")
async def add_comment(
    album_id: int,
    track_id: int,
    db: SessionDep,
    content: str = Form(...),
    author: str = Form(...)
):
    """Add a comment to a track"""
    comment = Comment(content=content, author=author, track_id=track_id)
    db.add(comment)
    db.commit()
    return RedirectResponse(
        url=f"/albums/{album_id}/tracks/{track_id}",
        status_code=status.HTTP_303_SEE_OTHER
    )


@app.post("/albums/{album_id}/tracks/{track_id}/react")
async def react_to_track(
    album_id: int,
    track_id: int,
    db: SessionDep,
    reaction_type: str = Form(...)  # "like" or "dislike"
):
    """Like or dislike a track"""
    reaction = Reaction(reaction_type=reaction_type, track_id=track_id)
    db.add(reaction)
    db.commit()
    return RedirectResponse(
        url=f"/albums/{album_id}/tracks/{track_id}",
        status_code=status.HTTP_303_SEE_OTHER
    )


@app.post("/comments/{comment_id}/delete")
async def delete_comment(
    comment_id: int,
    db: SessionDep,
    album_id: int = Form(...),
    track_id: int = Form(...)
):
    """Delete a comment"""
    comment = db.get(Comment, comment_id)
    if comment:
        db.delete(comment)
        db.commit()
    return RedirectResponse(
        url=f"/albums/{album_id}/tracks/{track_id}",
        status_code=status.HTTP_303_SEE_OTHER
    )