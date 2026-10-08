# Imports
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from core.database import get_db
from schemas.albums import (
    AlbumCreate,
    AlbumResponse,
    AlbumUpdate
)
from controller.albums_controller import (
    create_album,
    delete_album,
    get_album,
    get_albums,
    update_album,
)

# Router Configuration
router = APIRouter(
    prefix="/albums",
    tags=["Albums"]
)

# Endpoints
@router.get(
    "/",
    response_model=list[AlbumResponse],
    status_code=status.HTTP_200_OK
)
def read_albums(
    genre: str | None = Query(
        default=None,
        description="Filter by genre"
    ),
    search: str | None = Query(
        default=None,
        description="Search by title or artist"
    ),
    db: Session = Depends(get_db)
):
    return get_albums(
        db,
        genre=genre,
        search=search
    )


@router.get(
    "/{album_id}",
    response_model=AlbumResponse,
    status_code=status.HTTP_200_OK
)
def read_album(
    album_id: int,
    db: Session = Depends(get_db)
):
    return get_album(db, album_id)


@router.post(
    "/",
    response_model=AlbumResponse,
    status_code=status.HTTP_201_CREATED
)
def create_new_album(
    album_data: AlbumCreate,
    db: Session = Depends(get_db)
):
    return create_album(db, album_data)


@router.put(
    "/{album_id}",
    response_model=AlbumResponse,
    status_code=status.HTTP_200_OK
)
def update_existing_album(
    album_id: int,
    album_data: AlbumUpdate,
    db: Session = Depends(get_db)
):
    return update_album(
        db,
        album_id,
        album_data
    )


@router.delete(
    "/{album_id}",
    status_code=status.HTTP_200_OK
)
def delete_existing_album(
    album_id: int,
    db: Session = Depends(get_db)
):
    delete_album(db, album_id)

    return {
        "message": "Album successfully deleted"
    }


# Backwards compatibility router for /discs
discs_router = APIRouter(
    prefix="/discs",
    tags=["Discs (Legacy)"]
)


discs_router.add_api_route(
    "/",
    read_albums,
    methods=["GET"],
    response_model=list[AlbumResponse]
)

discs_router.add_api_route(
    "/{album_id}",
    read_album,
    methods=["GET"],
    response_model=AlbumResponse
)

discs_router.add_api_route(
    "/",
    create_new_album,
    methods=["POST"],
    response_model=AlbumResponse,
    status_code=status.HTTP_201_CREATED
)

discs_router.add_api_route(
    "/{album_id}",
    update_existing_album,
    methods=["PUT"],
    response_model=AlbumResponse
)

discs_router.add_api_route(
    "/{album_id}",
    delete_existing_album,
    methods=["DELETE"]
)