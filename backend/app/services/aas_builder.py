import os
import requests
import logging

logger = logging.getLogger("passporttwin.aas")
BASYX_AAS_URL = os.getenv("BASYX_AAS_URL", "http://basyx-aas:4001/aasServer")

class AASBuilder:
    @staticmethod
    def sync_instrument_shell(instrument, instrument_type) -> bool:
        """Proyecta un activo canónico a una Asset Administration Shell en BaSyx."""
        aas_id = f"urn:passporttwin:aas:{instrument.serial_number}"
        asset_id = f"urn:passporttwin:asset:{instrument.serial_number}"
        
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
            "submodels": []
        }

        try:
            url = f"{BASYX_AAS_URL}/shells/{payload['idShort']}"
            resp = requests.put(url, json=payload, timeout=4)
            if resp.status_code in [200, 201]:
                return True
            # Si PUT no existe, probar POST canónico
            resp_post = requests.post(f"{BASYX_AAS_URL}/shells", json=payload, timeout=4)
            return resp_post.status_code in [200, 201]
        except Exception as e:
            logger.error(f"Error sincronizando con Eclipse BaSyx: {str(e)}")
            return False