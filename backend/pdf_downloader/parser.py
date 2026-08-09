class CaseParser:
    @staticmethod
    def parse(case_number: str) -> dict:
        """
        Converts:
        2026-058549-SP-25

        Into:
        {
            "year": "2026",
            "sequence": "058549",
            "code": "SP",
            "location": "25"
        }
        """

        parts = case_number.strip().split("-")

        if len(parts) != 4:
            raise ValueError("Invalid Case Number Format")

        return {
            "year": parts[0],
            "sequence": parts[1],
            "code": parts[2],
            "location": parts[3]
        }