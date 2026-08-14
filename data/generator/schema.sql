-- PassportTwin — Draft schema (Sprint 0)
-- This is a first draft to unblock Docker/Postgres setup.
-- Indexes, constraints, and relations will be refined in Sprint 2 (FastAPI CRUD + live DB).

CREATE TABLE IF NOT EXISTS instrument_type (
    id              SERIAL PRIMARY KEY,
    name            TEXT NOT NULL,          -- e.g. 'temperature', 'pressure', 'pH'
    magnitude       TEXT,
    unit            TEXT,
    created_at      TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE IF NOT EXISTS instrument_unit (
    id              SERIAL PRIMARY KEY,
    instrument_type_id INTEGER REFERENCES instrument_type(id),
    serial_number   TEXT UNIQUE NOT NULL,
    manufacturer    TEXT,
    model           TEXT,
    location        TEXT,
    criticality     TEXT,
    installed_at    DATE,
    lifecycle_state TEXT DEFAULT 'operational', -- operational | pending | out_of_tolerance | blocked | reuse_candidate | retired
    created_at      TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE IF NOT EXISTS document (
    id              SERIAL PRIMARY KEY,
    instrument_unit_id INTEGER REFERENCES instrument_unit(id),
    document_type   TEXT,     -- certificate | datasheet | manual
    file_path       TEXT,
    uploaded_at     TIMESTAMPTZ DEFAULT now(),
    validated_by    TEXT,
    validated_at    TIMESTAMPTZ
);

CREATE TABLE IF NOT EXISTS calibration_event (
    id              SERIAL PRIMARY KEY,
    instrument_unit_id INTEGER REFERENCES instrument_unit(id),
    calibration_date DATE,
    error_value     NUMERIC,
    tolerance       NUMERIC,
    result          TEXT,     -- pass | fail | out_of_tolerance
    next_due_date   DATE,
    created_at      TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE IF NOT EXISTS maintenance_event (
    id              SERIAL PRIMARY KEY,
    instrument_unit_id INTEGER REFERENCES instrument_unit(id),
    event_date      DATE,
    description     TEXT,
    cost_estimate   NUMERIC,
    created_at      TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE IF NOT EXISTS incident (
    id              SERIAL PRIMARY KEY,
    instrument_unit_id INTEGER REFERENCES instrument_unit(id),
    incident_date   DATE,
    description     TEXT,
    severity        TEXT,
    resolved_at     TIMESTAMPTZ,
    created_at      TIMESTAMPTZ DEFAULT now()
);
