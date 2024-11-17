from fastapi import FastAPI, HTTPException, Depends
from typing import Optional, List, Dict
from pydantic import BaseModel
from uuid import UUID, uuid4

app = FastAPI()
