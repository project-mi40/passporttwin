from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database.session import get_db
from app.models.instrument import InstrumentType, InstrumentUnit
from app.schemas.instrument import (
    InstrumentTypeCreate, 
    InstrumentTypeResponse, 
    InstrumentUnitCreate, 
    InstrumentUnitResponse
)
from app.services.aas_builder import AASBuilder

router = APIRouter(prefix="/instruments", tags=["instruments"])

@router.post("/types", response_model=InstrumentTypeResponse, status_code=status.HTTP_201_CREATED)
def create_instrument_type(payload: InstrumentTypeCreate, db: Session = Depends(get_db)):
    db_type = db.query(InstrumentType).filter(InstrumentType.name == payload.name).first()
    if db_type:
        raise HTTPException(status_code=400, detail="Instrument type already exists")
    new_type = InstrumentType(**payload.model_dump())
    db.add(new_type)
    db.commit()
    db.refresh(new_type)
    return new_type

@router.post("", response_model=InstrumentUnitResponse, status_code=status.HTTP_201_CREATED)
def create_instrument(payload: InstrumentUnitCreate, db: Session = Depends(get_db)):
    db_inst = db.query(InstrumentUnit).filter(InstrumentUnit.serial_number == payload.serial_number).first()
    if db_inst:
        raise HTTPException(status_code=400, detail="Serial number already registered")
    
    inst_type = db.query(InstrumentType).filter(InstrumentType.id == payload.instrument_type_id).first()
    if not inst_type:
        raise HTTPException(status_code=404, detail="Instrument type ID not found")

    new_inst = InstrumentUnit(**payload.model_dump())
    
    # 1. Persistencia Canónica
    db.add(new_inst)
    db.commit()
    db.refresh(new_inst)

    # 2. Proyección Interoperable AAS (BaSyx)
    synced = AASBuilder.sync_instrument_shell(new_inst, inst_type)
    new_inst.aas_sync_status = "SYNCED" if synced else "PENDING"
    db.commit()
    db.refresh(new_inst)

    return new_inst

@router.get("", response_model=List[InstrumentUnitResponse])
def list_instruments(db: Session = Depends(get_db)):
    return db.query(InstrumentUnit).all()

@router.get("/{id}", response_model=InstrumentUnitResponse)
def get_instrument(id: int, db: Session = Depends(get_db)):
    inst = db.query(InstrumentUnit).filter(InstrumentUnit.id == id).first()
    if not inst:
        raise HTTPException(status_code=404, detail="Instrument not found")
    return inst