from fastapi import FastAPI

from services.routes.routes_service import initialize_routes

app = FastAPI()

initialize_routes(app)
