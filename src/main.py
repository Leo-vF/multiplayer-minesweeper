from fastapi import FastAPI, Request
from tortoise.contrib.fastapi import register_tortoise

from .routers import field, general
from .models.db_minesweeper import db_minesweeper

app = FastAPI()
app.include_router(general.router)
app.include_router(field.router)


@app.get("/")
def main_page(request: Request):
    return {"inital working"}


register_tortoise(app,
                  db_url="sqlite://database/minesweeper.sql",
                  # "src.models.db_minesweeper", "src.models.db_spot"
                  modules={"models": ["src.ms_models"]},
                  generate_schemas=True,
                  add_exception_handlers=True)
