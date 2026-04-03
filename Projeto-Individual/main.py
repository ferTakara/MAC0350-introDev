from fastapi import FastAPI, Request, Response, Depends, Cookie, HTTPException, Form, Query
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select, SQLModel, create_engine
from models import Usuario, Jogo, Avaliacao, Desenvolvedora, Distribuidora
from typing import Annotated

arquivo_sqlite = "database.db"
url_sqlite = f"sqlite:///{arquivo_sqlite}"

engine = create_engine(url_sqlite)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI()

# Utilizamos jinja para retornar a partir dos métodos arquivos htmls completos, para melhorar a visibilidade do código e a manutenção dele
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.on_event("startup")
def on_startup() -> None:
    create_db_and_tables()

def get_current_user(
    session: SessionDep,
    session_user: Annotated[str | None, Cookie()] = None
):
    if not session_user:
        return None

    user = session.get(Usuario, int(session_user))
    return user

@app.get("/")
def home(request: Request, user: Usuario | None = Depends(get_current_user)):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "user": user
        }
    )

@app.get("/games")
def home(request: Request, user: Usuario | None = Depends(get_current_user)):
    return templates.TemplateResponse(
        request=request,
        name="games.html",
        context={
            "user": user
        }
    )

@app.post("/user")
def create_hero(user: Usuario, session: SessionDep) -> Usuario:
    try:
        session.add(user)
        session.commit()
        session.refresh(user)
        return user
    except IntegrityError:
        session.rollback()
        raise HTTPException(400, "Username or Email already in use")

@app.get("/user")
def read_heroes(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[Usuario]:
    users = session.exec(select(Usuario).offset(offset).limit(limit)).all()
    return users


@app.get("/user/{user_id}")
def read_hero(user_id: int, session: SessionDep) -> Usuario:
    user = session.get(Usuario, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Hero not found")
    return user


@app.delete("/user/{user_id}")
def delete_hero(user_id: int, session: SessionDep):
    user = session.get(Usuario, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Hero not found")
    session.delete(user)
    session.commit()
    return {"ok": True}


@app.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={}
    )

@app.get("/sign_in")
def sign_in_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="create_user.html",
        context={}
    )


@app.post("/login")
def login(
    username: str = Form(...),
    password: str = Form(...),
    response: Response = None,
    session: SessionDep = None
):
    statement = select(Usuario).where(Usuario.username == username)
    user = session.exec(statement).first()

    if not user:
        raise HTTPException(status_code=401, detail="Usuário não encontrado")

    if user.senha_hash != password:
        raise HTTPException(status_code=401, detail="Senha inválida")

    response.set_cookie(key="session_user", value=str(user.id))

    return {"message": "Login realizado"}

@app.get("/home")
def profile(request: Request, user: Usuario = Depends(get_current_user)):

    return templates.TemplateResponse(
        request=request,
        name="profile.html",
        context={
            "username": user.username,
        }
    )

@app.get("/profile_data")
def profile_data(session: SessionDep):
    user = session.exec(select(Usuario)).first()  # simplificado

    return {
        "avatar": user.avatar or "/static/avatars/default.png",
        "total_games": user.total_games or 0,
        "played_2026": user.played_2026 or 0,
        "reviews": user.reviews or 0
    }

@app.get("/logout")
def logout(response: Response):
    response.delete_cookie("session_user")
    return {"message": "Logout realizado"}

from fastapi.responses import HTMLResponse

@app.get("/add_game_form", response_class=HTMLResponse)
def get_add_game_form():
    return """
    <div id="modal-overlay" style="
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0,0,0,0.7);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 1000;
    ">

        <div style="
            background: #181a21;
            padding: 25px;
            border-radius: 12px;
            width: 300px;
            box-shadow: 0 0 20px rgba(0,0,0,0.5);
        ">

            <h2 style="margin-top: 0;">Add Game</h2>

            <form 
                hx-post="/post_add_game"
                hx-target="body"
                hx-swap="none"
                enctype="multipart/form-data"
            >

                <input type="text" name="nome" placeholder="Game name" required
                    style="width:100%; margin-bottom:10px; padding:8px; border-radius:6px; border:none;">

                <input type="text" name="plataforma" placeholder="Platform"
                    style="width:100%; margin-bottom:10px; padding:8px; border-radius:6px; border:none;">

                <input type="number" name="nota" placeholder="Rating (0-10)" min="0" max="10"
                    style="width:100%; margin-bottom:15px; padding:8px; border-radius:6px; border:none;">

                <input type="text" name="desenvolvedora" placeholder="Developer"
                    style="width:100%; margin-bottom:10px; padding:8px; border-radius:6px; border:none;">

                <input type="text" name="distribuidora" placeholder="Distributor"
                    style="width:100%; margin-bottom:10px; padding:8px; border-radius:6px; border:none;">

                <input type="file" name="imagem" accept="image/*"
                    style="width:100%; margin-bottom:10px;">

                <div style="display:flex; justify-content: space-between;">

                    <button type="submit" style="
                        background:#4CAF50;
                        border:none;
                        padding:8px 12px;
                        border-radius:6px;
                        color:white;
                        cursor:pointer;
                    ">
                        Save
                    </button>

                    <button type="button" onclick="fecharModal()" style="
                        background:#444;
                        border:none;
                        padding:8px 12px;
                        border-radius:6px;
                        color:white;
                        cursor:pointer;
                    ">
                        Cancel
                    </button>

                </div>
            </form>
        </div>
    </div>

    <script>
        function fecharModal() {
            document.getElementById('modal-overlay').remove();
        }
    </script>
    """

from fastapi import Form, UploadFile, File

@app.post("/post_add_game")
def post_add_game(
    session: SessionDep,
    nome: str = Form(...),
    plataforma: str = Form(None),
    nota: int = Form(None),
    desenvolvedora: str = Form(None),
    distribuidora: str = Form(None),
    imagem: UploadFile = File(None)
):
    caminho_imagem = None

    # 📸 salva imagem
    if imagem:
        caminho_imagem = f"{UPLOAD_DIR}/{imagem.filename}"
        with open(caminho_imagem, "wb") as buffer:
            shutil.copyfileobj(imagem.file, buffer)

    # 🎮 cria objeto do jogo
    novo_jogo = Jogo(
        nome=nome,
        plataforma=plataforma,
        nota=nota,
        desenvolvedora=desenvolvedora,
        distribuidora=distribuidora,
        imagem=caminho_imagem
    )

    # 💾 salva no banco
    session.add(novo_jogo)
    session.commit()
    session.refresh(novo_jogo)

    print("SALVO:", novo_jogo)

    # fecha modal no frontend
    return "<script>fecharModal()</script>"