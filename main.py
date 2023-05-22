from fastapi import FastAPI
from part_1.routes import auth, contact, users
from fastapi_limiter import FastAPILimiter
from part_1.conf.config import settings
import redis.asyncio as redis
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Welcome to API!"}


app.include_router(auth.router, prefix='/api')
app.include_router(contact.router, prefix='/api')
app.include_router(users.router, prefix='/api')

@app.on_event("startup")
async def startup():
    r = await redis.Redis(host=settings.redis_host, port=settings.redis_port, db=0, encoding="utf-8",
                          decode_responses=True)
    await FastAPILimiter.init(r)



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)