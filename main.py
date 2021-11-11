from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from services.database.database_service import engine, Base
from services.routes.routes_service import initialize_routes

Base.metadata.create_all(engine, checkfirst=True)

app = FastAPI(title="Bookberry server", version="0.1.0")
app.mount("/static", StaticFiles(directory="static"), name="static")

initialize_routes(app)
