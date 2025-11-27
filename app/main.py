from fastapi import FastAPI
from routers.auth import router as auth_router
from core.database import AsyncSessionLocal
from contextlib import asynccontextmanager
from core.admin_configuration import create_admin_user
from middleware.current_user import CurrentUserMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with AsyncSessionLocal() as session:
        await create_admin_user(session)
    pass
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(CurrentUserMiddleware)
app.include_router(auth_router)


