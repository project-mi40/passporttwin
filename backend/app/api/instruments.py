from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database.session import get_db
from app.models.instrument import InstrumentType, InstrumentUnit
from app.schemas.instrument import (
    InstrumentTypeCreate, 
    InstrumentTypeResponse, 
    InstrumentUnitCreate, 
    InstrumentUnitResponse)
from app.services.aas_builder import AASBuilder

router = APIRouter(prefix="/instruments", tags=["instruments"])

@router.post("/types", response_model=InstrumentTypeResponse, status_code=status.HTTP_201_CREATED)
def create_instrument_type(payload: InstrumentTypeCreate, db: Session = Depends(get_db)):
    existing = db.query(InstrumentType).filter(InstrumentType.name == payload.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="El tipo de instrumento ya existe.")
    new_type = InstrumentType(**payload.model_dump())
    db.add(new_type)
    db.commit()
    db.refresh(new_type)
    return new_type

@router.get("/types", response_model=List[InstrumentTypeResponse])
def list_instrument_types(db: Session = Depends(get_db)):
    return db.query(InstrumentType).all()

@router.post("", response_model=InstrumentUnitResponse, status_code=status.HTTP_201_CREATED)
def register_instrument(payload: InstrumentUnitCreate, db: Session = Depends(get_db)):
    # 1. Comprobar unicidad de serial
    if db.query(InstrumentUnit).filter(InstrumentUnit.serial_number == payload.serial_number).first():
        raise HTTPException(status_code=400, detail="El número de serie ya está registrado.")

    # 2. Comprobar existencia de tipo
    inst_type = db.query(InstrumentType).filter(InstrumentType.id == payload.instrument_type_id).first()
    if not inst_type:
        raise HTTPException(status_code=404, detail="Tipo de instrumento no encontrado.")

    # 3. Persistencia Canónica Operacional
    new_instrument = InstrumentUnit(**payload.model_dump())
    db.add(new_instrument)
    db.commit()
    db.refresh(new_instrument)

    # 4. Proyección Interoperable AAS (Southbound sync)
    synced = AASBuilder.sync_shell_and_nameplate(new_instrument, inst_type)
    new_instrument.aas_sync_status = "SYNCED" if synced else "PENDING"
    db.commit()
    db.refresh(new_instrument)

    return new_instrument

@router.get("", response_model=List[InstrumentUnitResponse])
def list_instruments(db: Session = Depends(get_db)):
    return db.query(InstrumentUnit).all()

@router.get("/{id}", response_model=InstrumentUnitResponse)
def get_instrument_by_id(id: int, db: Session = Depends(get_db)):
    instrument = db.query(InstrumentUnit).filter(InstrumentUnit.id == id).first()
    if not instrument:
        raise HTTPException(status_code=404, detail="Instrumento no encontrado.")
    return instrument

@router.post("/{id}/sync", response_model=InstrumentUnitResponse)
def force_sync_aas(id: int, db: Session = Depends(get_db)):
    instrument = db.query(InstrumentUnit).filter(InstrumentUnit.id == id).first()
    if not instrument:
        raise HTTPException(status_code=404, detail="Instrumento no encontrado.")
    
    inst_type = db.query(InstrumentType).filter(InstrumentType.id == instrument.instrument_type_id).first()
    synced = AASBuilder.sync_shell_and_nameplate(instrument, inst_type)
    instrument.aas_sync_status = "SYNCED" if synced else "ERROR"
    db.commit()
    db.refresh(instrument)
    return instrument