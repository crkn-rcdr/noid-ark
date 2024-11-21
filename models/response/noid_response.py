from pydantic import BaseModel
from typing import List

class NoidResponse(BaseModel):
    noids:List[str]