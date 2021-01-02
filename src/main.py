from fastapi import FastAPI, Request
from tortoise.contrib.fastapi import register_tortoise

from .routers import field, general

app = FastAPI()
app.include_router(general.router)
app.include_router(field.router)


@app.get("/")
def main_page(request: Request):
    return {"inital working"}


register_tortoise(app,
                  db_url="sqlite://database/minesweeper.sql",
                  modules={"models": ["src.ms_models"]},
                  generate_schemas=True,
                  add_exception_handlers=True)
