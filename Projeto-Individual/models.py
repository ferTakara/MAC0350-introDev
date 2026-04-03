from typing import List, Optional
from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Field, Relationship, Session, SQLModel, create_engine

# =========================
# 🔗 Tabela de ligação (N:N)
# =========================
class UsuarioJogoLink(SQLModel, table=True):
    usuario_id: int = Field(foreign_key="usuario.id", primary_key=True)
    jogo_id: int = Field(foreign_key="jogo.id", primary_key=True)


# =========================
# 👤 Usuario
# =========================
class Usuario(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    email: Optional[str] = Field(default=None, index=True)
    senha_hash: Optional[str] = None
    avatar: Optional[str] = None
    total_games: Optional[int] = None
    played_2026: Optional[int] = None
    reviews: Optional[int] = None

    jogos_jogados: List["Jogo"] = Relationship(
        back_populates="usuarios",
        link_model=UsuarioJogoLink
    )

    avaliacoes: List["Avaliacao"] = Relationship(back_populates="usuario")


# =========================
# 🏢 Desenvolvedora
# =========================
class Desenvolvedora(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str = Field(index=True, unique=True)


# =========================
# 📦 Distribuidora
# =========================
class Distribuidora(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str = Field(index=True, unique=True)


# =========================
# 🎮 Jogo
# =========================
class Jogo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str = Field(index=True, unique=True)
    capa: Optional[str] = None
    genero: Optional[str] = None
    plataformas: Optional[str] = None
    ano: Optional[int] = None

    desenvolvedora_id: int = Field(foreign_key="desenvolvedora.id")
    distribuidora_id: int = Field(foreign_key="distribuidora.id")

    usuarios: List[Usuario] = Relationship(
        back_populates="jogos_jogados",
        link_model=UsuarioJogoLink
    )

    avaliacoes: List["Avaliacao"] = Relationship(back_populates="jogo")


# =========================
# ⭐ Avaliação
# =========================
class Avaliacao(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    usuario_id: int = Field(foreign_key="usuario.id")
    jogo_id: int = Field(foreign_key="jogo.id")

    tempo_de_jogo: int
    nota: int
    comentario: str

    usuario: Usuario = Relationship(back_populates="avaliacoes")
    jogo: Jogo = Relationship(back_populates="avaliacoes")

