""""Module main"""

from fastapi import FastAPI
from routes import auth, contact, users
from fastapi_limiter import FastAPILimiter
from configure.config import settings
import redis.asyncio as redis
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

@app.get("/")
def root():
    """
    The root function is a simple endpoint that returns a welcome message.

    :return: A dictionary with a message
    """
    return {"message": "Welcome to API!"}


app.include_router(auth.router, prefix='/api')
app.include_router(contact.router, prefix='/api')
app.include_router(users.router, prefix='/api')

@app.on_event("startup")
async def startup():
    """
    The startup function is called when the application starts up.
    It's a good place to initialize things that are used by the app, such as databases or caches.

    :return: A future, so we need to await it
    """
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