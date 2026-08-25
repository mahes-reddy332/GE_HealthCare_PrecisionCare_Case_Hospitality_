class CostService:
    @staticmethod
    def calculate_deductions(total_bill: float, copay_pct: float) -> float:
        return total_bill * (copay_pct / 100.0)
