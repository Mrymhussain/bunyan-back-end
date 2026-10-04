import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

from controllers.auth import router as AuthRouter
from controllers.projects import router as ProjectsRouter
from controllers.users import router as UsersRouter

app = FastAPI()


origins = [
    origin.strip()
    for origin in os.getenv("CORS_ORIGINS", "").split(",")
    if origin.strip()
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(AuthRouter, prefix="/api")
app.include_router(UsersRouter, prefix="/api")
app.include_router(ProjectsRouter, prefix="/api")

@app.get("/health")
def health_check():
    return {"message": "Api is running"}