from sqlalchemy.orm import Session

from models.formats import Format
from schemas.formats import FormatCreate, FormatUpdate


def get_formats(db: Session) -> list[Format]:
    return db.query(Format).order_by(Format.id).all()

def get_format(db: Session, format_id: int) -> Format | None:
    return (
        db.query(Format)
        .filter(Format.id == format_id)
        .first()
    )

def get_format_by_name(
    db: Session,
    name: str
) -> Format | None:
    return (
        db.query(Format)
        .filter(Format.name == name)
        .first()
    )

def create_format(
    db: Session,
    format_data: FormatCreate
) -> Format:

    existing_format = get_format_by_name(
        db,
        format_data.name
    )

    if existing_format:
        raise ValueError(
            "A format with this name already exists"
        )

    new_format = Format(
        name=format_data.name,
        description=format_data.description
    )

    db.add(new_format)
    db.commit()
    db.refresh(new_format)

    return new_format


def update_format(
    db: Session,
    format_id: int,
    format_data: FormatUpdate
) -> Format | None:

    format_db = get_format(db, format_id)

    if format_db is None:
        return None

    if format_data.name is not None:
        existing_format = (
            db.query(Format)
            .filter(
                Format.name == format_data.name,
                Format.id != format_id
            )
            .first()
        )

        if existing_format:
            raise ValueError(
                "A format with this name already exists"
            )

        format_db.name = format_data.name

    if format_data.description is not None:
        format_db.description = format_data.description

    db.commit()
    db.refresh(format_db)

    return format_db


def delete_format(
    db: Session,
    format_id: int
) -> bool:

    format_db = get_format(db, format_id)

    if format_db is None:
        return False

    db.delete(format_db)
    db.commit()

    return True