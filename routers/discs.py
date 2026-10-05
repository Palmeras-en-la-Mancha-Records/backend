from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from core.database import get_db
from schemas.discs import DiscCreate, DiscResponse, DiscUpdate
from services.discs_services import (
    create_disc,
    delete_disc,
    get_disc,
    get_discs,
    update_disc,
)

router = APIRouter(
    prefix="/discs",
    tags=["Discs"]
)


@router.get(
    "/",
    response_model=list[DiscResponse],
    status_code=status.HTTP_200_OK
)
def read_discs(
    genre: str | None = Query(default=None, description="Filtrar por género"),
    search: str | None = Query(default=None, description="Buscar por título o artista"),
    db: Session = Depends(get_db)
):
    return get_discs(db, genre=genre, search=search)


@router.get(
    "/{disc_id}",
    response_model=DiscResponse,
    status_code=status.HTTP_200_OK
)
def read_disc(
    disc_id: int,
    db: Session = Depends(get_db)
):
    disc = get_disc(db, disc_id)
    if disc is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Disco no encontrado"
        )
    return disc


@router.post(
    "/",
    response_model=DiscResponse,
    status_code=status.HTTP_201_CREATED
)
def create_new_disc(
    disc_data: DiscCreate,
    db: Session = Depends(get_db)
):
    return create_disc(db, disc_data)


@router.put(
    "/{disc_id}",
    response_model=DiscResponse,
    status_code=status.HTTP_200_OK
)
def update_existing_disc(
    disc_id: int,
    disc_data: DiscUpdate,
    db: Session = Depends(get_db)
):
    disc = update_disc(db, disc_id, disc_data)
    if disc is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Disco no encontrado"
        )
    return disc


@router.delete(
    "/{disc_id}",
    status_code=status.HTTP_200_OK
)
def delete_existing_disc(
    disc_id: int,
    db: Session = Depends(get_db)
):
    deleted = delete_disc(db, disc_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Disco no encontrado"
        )
    return {
        "message": "Disco eliminado correctamente"
    }
