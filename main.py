from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from services.database.database_service import engine, Base
from services.routes.routes_service import initialize_routes

Base.metadata.create_all(engine, checkfirst=True)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

initialize_routes(app)
