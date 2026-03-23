from fastapi import FastAPI, Request, Response, Depends, Cookie, HTTPException, Form
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Annotated

app = FastAPI()

templates = Jinja2Templates(directory="templates")

class User(BaseModel):
    username: str
    password: str
    bio: str

# "Banco de dados"
users_db = []

@app.get("/")
def create_user_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="create_user.html",
        context={}
    )

@app.get("/users")
def create_user_page(request: Request):
    return users_db

@app.post("/users")
def create_user(user: User):
    users_db.append(user)
    return {
        "username": user.username,
        "bio": user.bio
    }

@app.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={}
    )

@app.post("/login")
def login(
    username: str = Form(...),
    password: str = Form(...),
    response: Response = None
):

    user = None

    for u in users_db:
        if u.username == username and u.password == password:
            user = u
            break

    if not user:
        raise HTTPException(status_code=401, detail="sexo inválidas")
    
    response.set_cookie(key="session_user", value=username)

    return {"message": "Login realizado"}

    
def get_current_user(session_user: Annotated[str | None, Cookie()] = None):

    if not session_user:
        raise HTTPException(status_code=401, detail="Não logado")

    user = next((u for u in users_db if u.username == session_user), None)

    return user

@app.get("/home")
def profile(request: Request, user: User = Depends(get_current_user)):

    return templates.TemplateResponse(
        request=request,
        name="profile.html",
        context={
            "username": user.username,
            "bio": user.bio
        }
    )