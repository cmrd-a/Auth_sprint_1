import logging

import aioredis
import uvicorn as uvicorn
from elasticsearch import AsyncElasticsearch
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from api.v1 import films, genres, persons
from core.config import config
from core.logger import LOGGING
from db import elastic, redis

app = FastAPI(
    title=config.project_name,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
)


@app.on_event("startup")
async def startup():
    redis.redis = await aioredis.from_url(config.redis_url)
    elastic.es = AsyncElasticsearch(hosts=[f"{config.es_host}:{config.es_port}"])


@app.on_event("shutdown")
async def shutdown():
    await redis.redis.close()
    await elastic.es.close()


app.include_router(films.router, prefix="/api/v1/films", tags=["films"])
app.include_router(genres.router, prefix="/api/v1/genres", tags=["genres"])
app.include_router(persons.router, prefix="/api/v1/persons", tags=["persons"])

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        log_config=LOGGING,
        log_level=logging.INFO,
    )
