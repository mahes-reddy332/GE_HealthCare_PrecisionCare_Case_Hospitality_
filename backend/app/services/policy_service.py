from ..schemas.policy import PolicyExtracted

class PolicyService:
    @staticmethod
    async def extract_from_pdf(file_path: str) -> PolicyExtracted:
        # Mock implementation for OCR / LLM fallback
        return PolicyExtracted(
            sum_insured=500000.0,
            room_rent_cap_type="1% of SI",
            room_rent_limit=5000.0,
            icu_limit=10000.0,
            copay_percentage=10.0,
            deductible=0.0
        )
