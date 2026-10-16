import os
from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
views = Jinja2Templates(directory=os.path.join(Path(__file__).resolve().parent.parent, "Views"))


@router.get("/", response_class=HTMLResponse)
def index(request: Request):    
    return views.TemplateResponse(request=request, name="index.html")








