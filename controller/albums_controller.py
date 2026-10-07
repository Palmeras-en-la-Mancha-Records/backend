# Imports
from sqlalchemy import or_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from models.albums_models import Album
from schemas.albums import AlbumCreate, AlbumUpdate


# Read Operations
def get_albums(
    db: Session,
    genre: str | None = None,
    search: str | None = None
) -> list[Album]:

    try:
        query = db.query(Album)

        if genre:
            query = query.filter(
                Album.genre.ilike(f"%{genre}%")
            )

        if search:
            search_pattern = f"%{search}%"

            query = query.filter(
                or_(
                    Album.title.ilike(search_pattern),
                    Album.artist.ilike(search_pattern)
                )
            )

        return (
            query
            .order_by(Album.id.desc())
            .all()
        )

    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving albums"
        )


def get_album(
    db: Session,
    album_id: int
) -> Album:

    try:
        album_db = (
            db.query(Album)
            .filter(Album.id == album_id)
            .first()
        )

        if album_db is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Album not found"
            )

        return album_db

    except HTTPException:
        raise

    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving album"
        )


# Write Operations
def create_album(
    db: Session,
    album_data: AlbumCreate
) -> Album:

    try:
        new_album = Album(
            **album_data.model_dump()
        )

        db.add(new_album)
        db.commit()
        db.refresh(new_album)

        return new_album

    except SQLAlchemyError:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating album"
        )


def update_album(
    db: Session,
    album_id: int,
    album_data: AlbumUpdate
) -> Album:

    try:
        album_db = (
            db.query(Album)
            .filter(Album.id == album_id)
            .first()
        )

        if album_db is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Album not found"
            )

        update_dict = album_data.model_dump(
            exclude_unset=True
        )

        for key, value in update_dict.items():
            setattr(album_db, key, value)

        db.commit()
        db.refresh(album_db)

        return album_db

    except HTTPException:
        raise

    except SQLAlchemyError:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating album"
        )


def delete_album(
    db: Session,
    album_id: int
) -> None:

    try:
        album_db = (
            db.query(Album)
            .filter(Album.id == album_id)
            .first()
        )

        if album_db is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Album not found"
            )

        db.delete(album_db)
        db.commit()

    except HTTPException:
        raise

    except SQLAlchemyError:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error deleting album"
        )


# Aliases for backwards compatibility
get_discs = get_albums
get_disc = get_album
create_disc = create_album
update_disc = update_album
delete_disc = delete_album
