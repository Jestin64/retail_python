# app/create_tables.py

from db.session import engine, Base
# import your models so they’re registered on Base.metadata
import models.user  

def main():
    Base.metadata.create_all(bind=engine)
    print("✅ Tables created successfully")

if __name__ == "__main__":
    main()
