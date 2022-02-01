from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse 

app = FastAPI()

@app.get("/")
async def read_index():
    return FileResponse('index.html')

app.mount("/", StaticFiles(directory="."), name="static")
