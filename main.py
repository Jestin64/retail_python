from fastapi import FastAPI
from routes.user     import router as user_router
from routes.login    import router as login_router
from routes.product  import router as product_router
from routes.category import router as category_router
from routes.order    import router as order_router
from db.session import Base, engine

# 📥 Make sure SQLAlchemy sees all your models
import models.user
import models.product
import models.category
import models.order
import models.order_item


# 🛠️ Create tables if they don't exist
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Include all route modules
app.include_router(user_router)
app.include_router(login_router)
app.include_router(product_router)
app.include_router(category_router)
app.include_router(order_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the API"}


