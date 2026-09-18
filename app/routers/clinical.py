from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app import models, schemas
from app.database import get_db


router = APIRouter(tags=["clinical views"])


@router.get("/clients/by-uid/{client_uid}", response_model=schemas.ClientRead)
def get_client_by_uid(client_uid: str, db: Session = Depends(get_db)):
    stmt = select(models.Clients.marital_status,models.Clients.marital_status).where(models.Clients.client_uid == client_uid)
    client = db.scalar(stmt)
    if client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    return client


@router.get("/fp-methods/{method_id}/details", response_model=schemas.FPMethodDetail)
def fp_method_details(method_id: int, db: Session = Depends(get_db)):
    stmt = (
        select(models.FPMethods)
        .options(
            selectinload(models.FPMethods.advantages),
            selectinload(models.FPMethods.cautions),
            selectinload(models.FPMethods.side_effects),
            selectinload(models.FPMethods.use_instructions),
        )
        .where(models.FPMethods.method_id == method_id)
    )
    method = db.scalar(stmt)
    if method is None:
        raise HTTPException(status_code=404, detail="FP method not found")
    return method


@router.get("/clients/{client_id}/timeline", response_model=schemas.ClientTimeline)
def client_timeline(client_id: int, db: Session = Depends(get_db)):
    client = db.get(models.Clients, client_id)
    if client is None:
        raise HTTPException(status_code=404, detail="Client not found")

    reproductive_history = db.scalar(
        select(models.ReproductiveHistory).where(models.ReproductiveHistory.client_id == client_id)
    )
    encounters = list(db.scalars(
        select(models.Encounters)
        .where(models.Encounters.client_id == client_id)
        .order_by(models.Encounters.encounter_date, models.Encounters.encounter_id)
    ).all())
    episodes = list(db.scalars(
        select(models.FPUsageEpisodes)
        .where(models.FPUsageEpisodes.client_id == client_id)
        .order_by(models.FPUsageEpisodes.start_date, models.FPUsageEpisodes.episode_id)
    ).all())
    episode_ids = [e.episode_id for e in episodes]

    if episode_ids:
        dispensing = list(db.scalars(
            select(models.FPDispensing)
            .where(models.FPDispensing.episode_id.in_(episode_ids))
            .order_by(models.FPDispensing.dispense_date)
        ).all())
        followups = list(db.scalars(
            select(models.Followups)
            .where(models.Followups.episode_id.in_(episode_ids))
            .order_by(models.Followups.due_date)
        ).all())
        reports = list(db.scalars(
            select(models.SideEffectReports)
            .where(models.SideEffectReports.client_id == client_id)
            .order_by(models.SideEffectReports.report_date)
        ).all())
    else:
        dispensing, followups, reports = [], [], []

    return {
        "client": client,
        "reproductive_history": reproductive_history,
        "encounters": encounters,
        "usage_episodes": episodes,
        "dispensing": dispensing,
        "followups": followups,
        "side_effect_reports": reports,
    }
