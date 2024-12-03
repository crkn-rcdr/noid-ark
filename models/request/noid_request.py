from typing import Any
from pydantic import BaseModel,Field,field_validator
from enum import Enum

class CaseInsensitiveEnum(str,Enum):
    @classmethod
    def _missing_(cls, value: object) -> Any:
        if isinstance(value,str):
            value_lower = value.lower()
            for member in cls:
                if member.value.lower() == value_lower:
                    return member
        return super()._missing_(value)
    
class CRKNType(CaseInsensitiveEnum):
    manifest = "manifest"
    manifests = "manifests"
    canvas = "canvas"
    canvases = "canvases"
    collection = "collection"
    collections = "collections"
    generic = "generic"

class SchemaType(CaseInsensitiveEnum):
    ARK = "ARK"
    PURL = "PURL"
    Handle = "Handle"
    URN = "URN"
    DOI = "DOI"
   

class NoidRequest(BaseModel):
    m:int = Field(...,gt=0,description="models/data/models.py")
    type_:CRKNType =  Field(...,description="Type of NOID, e.g.,'canvas','collection'")
    schema_: SchemaType = Field(...,description="Scheme prefix for the NOID")
    naan: str = Field("69429",min_length=4,max_length=6, description="NAAN (Name Assigning Authority Number) for the NOID")

    @field_validator('naan')
    def validate_naan(cls,v):
        if not v.isdigit():
            raise ValueError('NAAN must be numeric')
        
        return v
