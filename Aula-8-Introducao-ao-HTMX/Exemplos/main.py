# Arquivo main.py

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, PlainTextResponse
from fastapi.templating import Jinja2Templates

likes = 0
app = FastAPI()

templates = Jinja2Templates(directory=["Templates", "Templates/Partials"])

@app.get("/home",response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse(request, "index.html", {"pagina": "/home  /pagina1"})

@app.post("/curtir", response_class=PlainTextResponse)
async def curtir():
    global likes
    likes += 1
    return str(likes)

@app.get("/likes", response_class=PlainTextResponse)
async def get_likes():
    return str(likes)

@app.delete("/likes", response_class=PlainTextResponse)
async def delete_likes():
    global likes
    likes = 0
    return str(likes)

@app.get("/home/pagina1", response_class=HTMLResponse)
async def pag1(request: Request):
    if (not "HX-Request" in request.headers):
        return templates.TemplateResponse(request, "index.html", {"pagina": "/home/pagina1"})
    return templates.TemplateResponse(request, "Pagina1.html")

@app.get("/home/pagina2", response_class=HTMLResponse)
async def pag2(request: Request):
    if (not "HX-Request" in request.headers):
        return templates.TemplateResponse(request, "index.html", {"pagina": "/home/pagina2"})
    return templates.TemplateResponse(request, "Pagina2.html")

@app.get("/home/pagina3", response_class=HTMLResponse)
async def pag2(request: Request):
    if (not "HX-Request" in request.headers):
        return templates.TemplateResponse(request, "index.html", {"pagina": "/home/pagina3"})
    return templates.TemplateResponse(request, "Pagina3.html")