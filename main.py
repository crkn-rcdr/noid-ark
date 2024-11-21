from fastapi import FastAPI
from api.noid import router
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI(
    title="NOID Generator API",
    description="API to generate NOIDs (Nice Opaque Identifiers) based on specified types and a default template.",
    version="1.0.0"
)
origins = [
   '*'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
)

@app.get("/",include_in_schema=False)
async def redirect_to_docs():
    return RedirectResponse(url="/docs")

app.include_router(router)