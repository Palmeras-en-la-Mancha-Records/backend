# Imports
from sqlalchemy.orm import Session
from sqlalchemy import or_

from models.albums import Album
from schemas.albums import AlbumCreate, AlbumUpdate

# Read Services
def get_albums(
    db: Session,
    genre: str | None = None,
    search: str | None = None
) -> list[Album]:
    query = db.query(Album)

    if genre:
        query = query.filter(Album.genre.ilike(f"%{genre}%"))

    if search:
        search_pattern = f"%{search}%"
        query = query.filter(
            or_(
                Album.title.ilike(search_pattern),
                Album.artist.ilike(search_pattern)
            )
        )

    return query.order_by(Album.id.desc()).all()


def get_album(db: Session, album_id: int) -> Album | None:
    return db.query(Album).filter(Album.id == album_id).first()

# Write Services
def create_album(db: Session, album_data: AlbumCreate) -> Album:
    new_album = Album(**album_data.model_dump())
    db.add(new_album)
    db.commit()
    db.refresh(new_album)
    return new_album


def update_album(db: Session, album_id: int, album_data: AlbumUpdate) -> Album | None:
    album_db = get_album(db, album_id)
    if album_db is None:
        return None

    update_dict = album_data.model_dump(exclude_unset=True)
    for key, value in update_dict.items():
        setattr(album_db, key, value)

    db.commit()
    db.refresh(album_db)
    return album_db


def delete_album(db: Session, album_id: int) -> bool:
    album_db = get_album(db, album_id)
    if album_db is None:
        return False

    db.delete(album_db)
    db.commit()
    return True

# Aliases for backwards compatibility
get_discs = get_albums
get_disc = get_album
create_disc = create_album
update_disc = update_album
delete_disc = delete_album
