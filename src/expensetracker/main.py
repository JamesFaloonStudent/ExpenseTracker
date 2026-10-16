from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routers.viewRouter import router as ViewRouter

app = FastAPI()

# Serve everything in ./static at the URL /static
app.mount("/static", StaticFiles(directory="static"), name="static")


app.include_router(ViewRouter)  