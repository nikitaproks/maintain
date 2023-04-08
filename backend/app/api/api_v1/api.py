from app.api.api_v1.routers import accounts, auth, roles, users, tickets, cities, tasks
from fastapi import APIRouter

api_router = APIRouter()

api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(roles.router)
api_router.include_router(accounts.router)
api_router.include_router(tickets.router)
api_router.include_router(cities.router)
api_router.include_router(tasks.router)
