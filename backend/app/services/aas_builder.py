import os
import requests
import logging

from backend.app.schemas import instrument

logger = logging.getLogger("passporttwin.aas")
BASYX_AAS_URL = os.getenv("BASYX_AAS_URL", "http://basyx-aas:4001/aasServer")

class AASBuilder:
    @staticmethod
    def sync_instrument_shell(instrument, instrument_type) -> bool:
        """Proyecta un activo canónico a una Asset Administration Shell en BaSyx."""
        aas_id = f"urn:passporttwin:aas:{instrument.serial_number}"
        asset_id = f"urn:passporttwin:asset:{instrument.serial_number}"
        sm_id = f"urn:passporttwin:submodel:nameplate:{instrument.serial_number}"
        
        payload = {
            "idShort": f"AAS_{instrument.serial_number}",
            "identification": {
                "id": aas_id,
                "idType": "IRI"
            },
            "asset": {
                "idShort": f"Asset_{instrument.serial_number}",
                "identification": {
                    "id": asset_id,
                    "idType": "IRI"
                },
                "kind": "Instance"
            },
            "submodels": [
                {
                    "keys": [
                        {
                            "type": "Submodel",
                            "local": False,
                            "value": sm_id,
                            "idType": "IRI"
                        }
                    ]
                }
            ]
        }

        nameplate_payload = {
            "idShort": "Nameplate",
            "identification": {
                "id": sm_id,
                "idType": "IRI"
            },
            "semanticId": {
                "keys": [
                    {
                        "type": "GlobalReference",
                        "local": False,
                        "value": "https://admin-shell.io/zvei/nameplate/1/0/Nameplate",
                        "idType": "IRI"
                    }
                ]
            },
            "submodelElements": [
                {
                    "idShort": "ManufacturerName",
                    "modelType": {"name": "Property"},
                    "valueType": "string",
                    "value": str(instrument.manufacturer)
                },
                {
                    "idShort": "ManufacturerProductDesignation",
                    "modelType": {"name": "Property"},
                    "valueType": "string",
                    "value": str(instrument.model)
                },
                {
                    "idShort": "SerialNumber",
                    "modelType": {"name": "Property"},
                    "valueType": "string",
                    "value": str(instrument.serial_number)
                },
                {
                    "idShort": "PhysicalQuantity",
                    "modelType": {"name": "Property"},
                    "valueType": "string",
                    "value": str(instrument_type.magnitude)
                }
            ]
        }

        try:
            # Enviar AAS Shell
            url_shells = f"{BASYX_AAS_URL}/shells"
            resp_shell = requests.post(url_shells, json=shell_payload, timeout=4)
            if resp_shell.status_code not in [200, 201]:
                # Intentar PUT si ya existe
                requests.put(f"{url_shells}/{shell_payload['idShort']}", json=shell_payload, timeout=4)

            # Enviar Submodel Nameplate
            url_sm = f"{BASYX_AAS_URL}/submodels"
            resp_sm = requests.post(url_sm, json=nameplate_payload, timeout=4)
            if resp_sm.status_code not in [200, 201]:
                requests.put(f"{url_sm}/{nameplate_payload['idShort']}", json=nameplate_payload, timeout=4)

            return True
        except Exception as e:
            logger.error(f"Fallo al sincronizar con BaSyx AAS Server: {str(e)}")
            return False