from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
from typing import List, Optional
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_FILE = "backend/momo_sms.db"

class Transaction(BaseModel):
    id: int
    category: str
    amount: int
    sender: Optional[str]
    receiver: Optional[str]
    date: Optional[str]
    description: Optional[str]

@app.get("/api/transactions", response_model=List[Transaction])
def get_transactions(category: Optional[str] = None, min_amount: Optional[int] = None, date: Optional[str] = None):
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    query = "SELECT id, category, amount, sender, receiver, date, description FROM sms_transactions WHERE 1=1"
    params = []
    if category:
        query += " AND category = ?"
        params.append(category)
    if min_amount:
        query += " AND amount >= ?"
        params.append(min_amount)
    if date:
        query += " AND date LIKE ?"
        params.append(f"{date}%")
    cursor = conn.execute(query, params)
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows
