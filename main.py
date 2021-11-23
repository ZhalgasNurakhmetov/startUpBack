from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from services.database.database_service import engine, Base
from services.routes.routes_service import initialize_routes

Base.metadata.create_all(engine, checkfirst=True)

app = FastAPI(title="Bookberry server", version="0.1.0")
# app.mount("/static", StaticFiles(directory="static"), name="static")

app = FastAPI()

origins = [
    "http://localhost:8100",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

initialize_routes(app)
