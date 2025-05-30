from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import scoped_session, sessionmaker, relationship, declarative_base
engine = create_engine('sqlite:///base_biblioteca.sqlite3')

db_session = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

class Livro(Base):
    __tablename__ = 'LIVROS'
    id_livro = Column(Integer, primary_key=True)
    titulo = Column(String(40), nullable=False, index=True, unique=True)
    autor = Column(String(30), nullable=False, index=True)
    ISBN = Column(Integer, nullable=False, index=True)
    resumo = Column(String(200), nullable=False, index=True)

    def __repr__(self):
        return '<Livro: {} {} {} {} {}'.format(self.id_livro, self.titulo, self.autor, self.ISBN, self.resumo)

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()

    def serialize_livro(self):
        dados_livro = {
            "titulo": self.titulo,
            "autor": self.autor,
            "isbn": self.ISBN,
            "resumo": self.resumo
        }
        return dados_livro



class Usuario(Base):
    __tablename__ = 'USUARIOS'
    id_usuario = Column(Integer, primary_key=True)
    nome = Column(String(40), nullable=False, index=True)
    CPF = Column(String(11), nullable=False, index=True, unique=True)
    endereco = Column(String(50), nullable=False, index=True)

    def __repr__(self):
        return '<Produto: {} {} {} {}'.format(self.id_usuario, self.nome, self.CPF, self.endereco)

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()

    def serialize_usuario(self):
        dados_usuario = {
            "nome": self.nome,
            "cpf": self.CPF,
            "endereco": self.endereco
        }
        return dados_usuario


class Emprestimo(Base):
    __tablename__ = 'EMPRÉSTIMOS'
    id_emprestimo = Column(Integer, primary_key=True)
    data_emprestimo = Column(String(8), nullable=False, index=True)
    data_devolucao = Column(String(8), nullable=False, index=True)


    id_usuario = Column(Integer, ForeignKey('USUARIOS.id_usuario'))
    usuario = relationship('Usuario')
    id_livro = Column(Integer, ForeignKey('LIVROS.id_livro'))
    livro = relationship('Livro')


    def __repr__(self):
        return '<Venda: {} {} {}  '.format(self.id_emprestimo, self.data_emprestimo, self.data_devolucao)

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()

    def serialize_emprestimo(self):
        dados_emprestimo = {
            "data de emprestimo": self.data_emprestimo,
            "data de devolucao": self.data_devolucao,
            'usuario': self.id_usuario,
            'livro': self.id_livro,
        }
        return dados_emprestimo

def init_db():
    Base.metadata.create_all(bind=engine)


if __name__ == '__main__':
    init_db()
