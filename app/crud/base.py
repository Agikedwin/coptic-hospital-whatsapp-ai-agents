from __future__ import annotations

from typing import Any, Generic, TypeVar

from pydantic import BaseModel
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.exceptions import CRUDConflictError


ModelType = TypeVar("ModelType")


class CRUDBase(Generic[ModelType]):
    def __init__(self, model: type[ModelType]):
        self.model = model
        self.pk_column = list(model.__table__.primary_key.columns)[0]

    def get(self, db: Session, item_id: Any) -> ModelType | None:
        return db.get(self.model, item_id)

    def get_multi(self, db: Session, *, offset: int = 0, limit: int = 100) -> list[ModelType]:
        stmt = select(self.model).order_by(self.pk_column).offset(offset).limit(limit)
        return list(db.scalars(stmt).all())

    def count(self, db: Session) -> int:
        stmt = select(func.count()).select_from(self.model)
        return int(db.scalar(stmt) or 0)

    def create(self, db: Session, obj_in: BaseModel) -> ModelType:
        data = obj_in.model_dump(exclude_unset=True)
        obj = self.model(**data)
        db.add(obj)
        try:
            db.commit()
            db.refresh(obj)
            return obj
        except IntegrityError as exc:
            db.rollback()
            raise CRUDConflictError(str(exc.orig)) from exc

    def update(self, db: Session, db_obj: ModelType, obj_in: BaseModel) -> ModelType:
        data = obj_in.model_dump(exclude_unset=True)
        for field, value in data.items():
            setattr(db_obj, field, value)
        db.add(db_obj)
        try:
            db.commit()
            db.refresh(db_obj)
            return db_obj
        except IntegrityError as exc:
            db.rollback()
            raise CRUDConflictError(str(exc.orig)) from exc

    def remove(self, db: Session, item_id: Any) -> bool:
        obj = self.get(db, item_id)
        if obj is None:
            return False
        db.delete(obj)
        try:
            db.commit()
            return True
        except IntegrityError as exc:
            db.rollback()
            raise CRUDConflictError(str(exc.orig)) from exc
