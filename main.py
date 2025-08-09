from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.user     import router as user_router
from routes.login    import router as login_router
from routes.product  import router as product_router
from routes.category import router as category_router
from routes.order    import router as order_router
from db.session import Base, engine

# Ensure SQLAlchemy detects all models
import models.user
import models.product
import models.category
import models.order
import models.order_item

# Dev only: Auto-create tables (use Alembic in prod)
# Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Supermarket Backend API",
    description="API for managing products, categories, orders, and users with role-based access",
    version="1.0.0",
)

# CORS for frontend communication
origins = ["http://localhost:3000", "http://127.0.0.1:3000"]  # Add your frontend URL for prod
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(user_router)
app.include_router(login_router)
app.include_router(product_router)
app.include_router(category_router)
app.include_router(order_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the API"}

@app.get("/health")
def health_check():
    return {"status": "ok"}



