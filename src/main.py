from fastapi import FastAPI, Request

from routers import field

app = FastAPI()
app.include_router(field)


@app.get("/")
def main_page(request: Request):
    return {"inital working"}
