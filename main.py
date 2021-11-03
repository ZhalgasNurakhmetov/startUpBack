from fastapi import FastAPI

from services.database.database_service import engine, Base
from services.routes.routes_service import initialize_routes

Base.metadata.create_all(engine, checkfirst=True)

app = FastAPI()

initialize_routes(app)
