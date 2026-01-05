from fastapi import APIRouter, Request
from starlette.templating import Jinja2Templates

registration = APIRouter(prefix="/register")

templates = Jinja2Templates(directory="templates")


@registration.get("/")
def register(request: Request):
    return templates.TemplateResponse("registration.html.j2", {"request": request})
