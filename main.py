import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from controllers.auth import router as AuthRouter
from controllers.consultations import router as ConsultationsRouter
from controllers.materials import router as MaterialsRouter
from controllers.order_items import router as OrderItemsRouter
from controllers.orders import router as OrdersRouter
from controllers.project_members import router as ProjectMembersRouter
from controllers.project_updates import router as ProjectUpdatesRouter
from controllers.projects import router as ProjectsRouter
from controllers.reviews import router as ReviewsRouter
from controllers.service_categories import router as ServiceCategoriesRouter
from controllers.service_requests import router as ServiceRequestsRouter
from controllers.users import router as UsersRouter

load_dotenv()

app = FastAPI()

origins = [
    origin.strip()
    for origin in os.getenv("CORS_ORIGINS", "").split(",")
    if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(AuthRouter, prefix="/api")
app.include_router(UsersRouter, prefix="/api")
app.include_router(ProjectsRouter, prefix="/api")
app.include_router(ProjectMembersRouter, prefix="/api")
app.include_router(ProjectUpdatesRouter, prefix="/api")
app.include_router(ConsultationsRouter, prefix="/api")
app.include_router(ServiceCategoriesRouter, prefix="/api")
app.include_router(ServiceRequestsRouter, prefix="/api")
app.include_router(MaterialsRouter, prefix="/api")
app.include_router(OrdersRouter, prefix="/api")
app.include_router(OrderItemsRouter, prefix="/api")
app.include_router(ReviewsRouter, prefix="/api")


@app.get("/health")
def health_check():
    return {"message": "Api is running"}