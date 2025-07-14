from fastapi import FastAPI
from routes import user, login
from routers import product  # ✅ Importing product router

app = FastAPI()

# ✅ Include all route modules
app.include_router(user.router)
app.include_router(login.router)
app.include_router(product.router)

# ✅ Optional root check
@app.get("/")
def read_root():
    return {"message": "Welcome to the API"}

