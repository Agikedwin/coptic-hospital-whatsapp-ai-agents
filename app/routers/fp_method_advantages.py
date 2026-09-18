from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.orm import Session

from app import schemas
from app.crud import fp_method_advantages as crud
from app.database import get_db
from app.exceptions import CRUDConflictError

router = APIRouter(prefix="/fp-method-advantages", tags=["fp-method-advantages"])


@router.get("", response_model=schemas.Page[schemas.FPMethodAdvantageRead])
def list_items(
    offset: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
):
    return {
        "total": crud.count(db),
        "offset": offset,
        "limit": limit,
        "items": crud.get_multi(db, offset=offset, limit=limit),
    }


@router.get("/{item_id}", response_model=schemas.FPMethodAdvantageRead)
def get_item(item_id: int, db: Session = Depends(get_db)):
    obj = crud.get(db, item_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="FPMethodAdvantage not found")
    return obj


@router.post("", response_model=schemas.FPMethodAdvantageRead, status_code=status.HTTP_201_CREATED)
def create_item(payload: schemas.FPMethodAdvantageCreate, db: Session = Depends(get_db)):
    try:
        return crud.create(db, payload)
    except CRUDConflictError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc


@router.patch("/{item_id}", response_model=schemas.FPMethodAdvantageRead)
def update_item(item_id: int, payload: schemas.FPMethodAdvantageUpdate, db: Session = Depends(get_db)):
    obj = crud.get(db, item_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="FPMethodAdvantage not found")
    try:
        return crud.update(db, obj, payload)
    except CRUDConflictError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    try:
        deleted = crud.remove(db, item_id)
    except CRUDConflictError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    if not deleted:
        raise HTTPException(status_code=404, detail="FPMethodAdvantage not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
