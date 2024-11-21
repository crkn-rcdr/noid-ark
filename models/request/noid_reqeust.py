from pydantic import BaseModel,Field
from typing import Optional
from enum import Enum

class CRKNType(str, Enum):
    generic = "generic"
    canvas = "canvas"
    canvases = "canvases"
    collection = "collection"
    collections = "collections"
    manifest = "manifest"
    manifests = "manifests"

class SchemaType(str,Enum):
    PURL = "PURL"
    Handle = "Handle"
    URN = "URN"
    DOI = "DOI"
    ARK = "ARK"

class NoidRequest(BaseModel):
    m:int = Field(...,gt=0,description="models/data/models.py")
    type_:CRKNType =  Field(...,description="Type of NOID, e.g.,'canvas','collection'")
    schema_: Optional[SchemaType] = Field(None,description="Scheme prefix for the NOID")
    naan: Optional[str] = Field(None, description="NAAN (Name Assigning Authority Number) for the NOID")