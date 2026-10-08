from sqlalchemy.orm import Session

from models.labels_models import Label
from schemas.labels import LabelCreate, LabelUpdate

def get_all_labels(db: Session, skip: int = 0, limit: int = 100) -> list[Label]:
    return db.query(Label).order_by(Label.id).offset(skip).limit(limit).all()

def create_label(db: Session, label_data: LabelCreate) -> Label:
    existing_label = db.query(Label).filter(Label.name == label_data.name).first()

    if existing_label:
        raise ValueError(f"A label with name '{label_data.name}' already exists")

    new_label = Label(
        name=label_data.name,
        country=label_data.country,
        website=label_data.website
    )
    
    db.add(new_label)
    db.commit()
    db.refresh(new_label)
    
    return new_label

def get_label_by_id(db: Session, label_id: int) -> Label | None:
    return db.query(Label).filter(Label.id == label_id).first()

def update_label(db: Session, label_id: int, label_data: LabelUpdate) -> Label | None:
    db_label = get_label_by_id(db, label_id)

    if db_label is None:
        return None
    
    if label_data.name is not None:
        existing_label = (db.query(Label).filter(Label.name == label_data.name, Label.id != label_id).first())
        if existing_label:
            raise ValueError(f"A label with name '{label_data.name}' already exists")
        db_label.name = label_data.name

    if label_data.country is not None:
        db_label.country = label_data.country

    if label_data.website is not None:
        db_label.website = label_data.website

    db.commit()
    db.refresh(db_label)

    return db_label

def delete_label(db: Session, label_id: int) -> bool:
    db_label = get_label_by_id(db, label_id)

    if db_label is None:
        return False

    db.delete(db_label)
    db.commit()

    return True
