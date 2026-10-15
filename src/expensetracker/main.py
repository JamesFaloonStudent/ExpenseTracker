from fastapi import FastAPI, APIRouter, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates








app = FastAPI()
router = APIRouter()
views = Jinja2Templates(directory="Views")



@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return views.TemplateResponse(request=request, name="index.html") 


app.include_router(router)