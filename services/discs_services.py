# Imports
from sqlalchemy.orm import Session
from sqlalchemy import or_

from models.discs import Disc
from schemas.discs import DiscCreate, DiscUpdate

# Read Services
def get_discs(
    db: Session,
    genre: str | None = None,
    search: str | None = None
) -> list[Disc]:
    query = db.query(Disc)

    if genre:
        query = query.filter(Disc.genre.ilike(f"%{genre}%"))

    if search:
        search_pattern = f"%{search}%"
        query = query.filter(
            or_(
                Disc.title.ilike(search_pattern),
                Disc.artist.ilike(search_pattern)
            )
        )

    return query.order_by(Disc.id.desc()).all()


def get_disc(db: Session, disc_id: int) -> Disc | None:
    return db.query(Disc).filter(Disc.id == disc_id).first()

# Write Services
def create_disc(db: Session, disc_data: DiscCreate) -> Disc:
    new_disc = Disc(**disc_data.model_dump())
    db.add(new_disc)
    db.commit()
    db.refresh(new_disc)
    return new_disc


def update_disc(db: Session, disc_id: int, disc_data: DiscUpdate) -> Disc | None:
    disc_db = get_disc(db, disc_id)
    if disc_db is None:
        return None

    update_dict = disc_data.model_dump(exclude_unset=True)
    for key, value in update_dict.items():
        setattr(disc_db, key, value)

    db.commit()
    db.refresh(disc_db)
    return disc_db


def delete_disc(db: Session, disc_id: int) -> bool:
    disc_db = get_disc(db, disc_id)
    if disc_db is None:
        return False

    db.delete(disc_db)
    db.commit()
    return True
