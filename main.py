import secrets

import uvicorn
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException, Request, APIRouter
from fastapi.responses import RedirectResponse
from sqlalchemy import select
from starlette.responses import HTMLResponse
from starlette.status import HTTP_307_TEMPORARY_REDIRECT

from engine import async_session

import validators

import schemas
from models.models import URL

app = FastAPI(
    title='Short link',
    swagger_ui_parameters={"docExpansion": "none"},
)

app.add_middleware(CORSMiddleware,
                   allow_origins=["*"],
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"],
                   max_age=3600
                   )


def raise_not_found(request):
    message = f"URL '{request.url}' doesn't exist"
    raise HTTPException(status_code=404, detail=message)


def raise_bad_request(message):
    raise HTTPException(status_code=400, detail=message)


@app.get('/url/{url_key}', response_class=RedirectResponse, status_code=302)
async def get_link(url_key: str, request: Request):
    async with async_session() as session:
        query = select(URL).where(URL.key == url_key)
        result = await session.scalar(query)
        url = result.target_url
    return RedirectResponse(url=url, status_code=HTTP_307_TEMPORARY_REDIRECT)
    # if result:
    #     return RedirectResponse(result.target_url)
    # else:
    #     raise_not_found(request)


@app.post("/url/")
async def create_url(url: schemas.URLBase):
    if not validators.url(url.target_url):
        raise_bad_request(message="Your provided URL is not valid")

    chars = "ABCDEFGHJKLMNOPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz234567890"
    key = "".join(secrets.choice(chars) for _ in range(12))

    async with async_session() as session:
        db_url = URL(
            target_url=url.target_url, key=key
        )
        session.add(db_url)
        await session.commit()
        session.refresh(db_url)
        db_url.key = key

    return f"TODO: Create database entry for: {url.target_url}"
