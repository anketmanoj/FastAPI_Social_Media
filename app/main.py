from fastapi import FastAPI
from . import models
from .database import engine
from . import models
from . routers import post, user, auth, vote

# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
async def root():
    return {"message" : "Home screen"}

# # ! ======================================================
# # * Database connection for testing
# import psycopg2
# from psycopg2.extras import RealDictCursor

# while True:
#     try:
#         # conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='test', cursor_factory=RealDictCursor)
#         # cursor = conn.cursor()
#         print("Database connection succesful")
#         break
#     except Exception as error:
#         print("Connection to database failed")
#         print(f"Error was {error}")
#         time.sleep(2)
    
# # ! ======================================================











