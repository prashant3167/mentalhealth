import secrets
from datetime import datetime
from typing import Dict, Any


class TokenService:
    def __init__(self, db):
        self.db = db

    async def create_token(self, employee_id: str, company: str, **kwargs) -> Dict[str, Any]:
        token_value = secrets.token_hex(8) # Replace with your token generation logic
        created_at = datetime.now()
        token_entry = {
            "employee_id": employee_id,
            "token": token_value,
            "created_at": created_at,
            "company": company
        }
        result = await self.db.get_collection("Token").insert_one(token_entry)
        return {**token_entry, "id": str(result.inserted_id)}

