
from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from Models import Aluno
from contextlib import asynccontextmanager
from sqlmodel import SQLModel, create_engine, Session, select, col

@asynccontextmanager
async def initFunction(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=initFunction)

arquivo_sqlite = "HTMX2.db"
url_sqlite = f"sqlite:///{arquivo_sqlite}"

engine = create_engine(url_sqlite)

templates = Jinja2Templates(directory=["Templates", "Templates/Partials"])

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
 
def buscar_alunos():
    with Session(engine) as session:
        query = select(Aluno)
        return session.exec(query).all()
    
@app.get("/busca", response_class=HTMLResponse)
def busca(request: Request):
    return templates.TemplateResponse(request, "index.html")


@app.get("/editarAlunos")
def novoAluno(request: Request):
    return templates.TemplateResponse(request, "options.html")

@app.post("/novoAluno", response_class=HTMLResponse)
def criar_aluno(nome: str = Form(...)):
    with Session(engine) as session:
        novo_aluno = Aluno(nome=nome)
        session.add(novo_aluno)
        session.commit()
        session.refresh(novo_aluno)
        return HTMLResponse(content=f"<p>O(a) aluno(a) {novo_aluno.nome} foi registrado(a)!</p>")


@app.delete("/deletaAluno", response_class=HTMLResponse)
def deletar_aluno(id: int = Form(...)):
    with Session(engine) as session:
        query = select(Aluno).where(Aluno.id == id)
        aluno = session.exec(query).first()
        if (not aluno):
            raise HTTPException(404, "Aluno não encontrado")
        session.delete(aluno)
        session.commit()
        return HTMLResponse(content=f"<p>O(a) aluno(a) {aluno.nome} foi deletado(a)!</p>")


def buscar_alunos(busca=""):
    with Session(engine) as session:
        query = select(Aluno).where(col(Aluno.nome).contains(busca)).order_by(Aluno.nome)
        alunos = session.exec(query).limit(10)
        return alunos

@app.get("/lista", response_class=HTMLResponse)
def lista(request: Request, busca: str | None='', page: int = 1):
    with Session(engine) as session:
        PAGE_SIZE = 10

        query = select(Aluno)
        total = session.exec(query).all()
        total_count = len(total)

        # paginação
        offset = (page - 1) * PAGE_SIZE

        query = select(Aluno)

        if busca:
            query = query.where(Aluno.nome.ilike(f"%{busca}%"))

        query = query.order_by(Aluno.nome)

        alunos = session.exec(
            query.offset(offset).limit(PAGE_SIZE)
        ).all()

        has_next = offset + PAGE_SIZE < total_count

        return templates.TemplateResponse(
            request,
            "lista.html",
            {
                "alunos": alunos,
                "busca": busca,
                "page": page,
                "has_next": has_next
            }
        )