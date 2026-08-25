from ..schemas.fhir import FHIRLocation

class FHIRService:
    @staticmethod
    def convert_hospital_to_location(hospital_id: int, name: str) -> FHIRLocation:
        return FHIRLocation(id=str(hospital_id), name=name)
