from fastapi import FastAPI
from routes import user, login

app = FastAPI()

# Wire up both routers
app.include_router(user.router)
app.include_router(login.router)

# Optional root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the API"}
