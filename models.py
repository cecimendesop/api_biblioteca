from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, declarative_base



Base = declarative_base()

class Livro(Base):
    __tablename__ = "livros"
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, index=True)
    autor = Column(String)
    isbn = Column(String, index=True)
    resumo = Column(String)

class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    cpf = Column(String, unique=True, index=True)
    endereco = Column(String)

class Emprestimo(Base):
    __tablename__ = "emprestimos"
    id = Column(Integer, primary_key=True, index=True)
    data_emprestimo = Column(String)
    data_devolucao_prevista = Column(String)
    livro_id = Column(Integer, ForeignKey("livros.id"))
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    livro = relationship("Livro")
    usuario = relationship("Usuario")

