from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base, relationship

engine = create_engine('sqlite:///biblioteca.sqlite3')
db_session = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

class Livro(Base):
    __tablename__ = 'livros'
    id_livro = Column(Integer, primary_key=True)
    titulo = Column(String(50), nullable=False, index=True)
    autor = Column(String(50), nullable=False, index=True)
    resumo = Column(String(300), nullable=False, index=True)
    ISBN = Column(Integer, nullable=False, index=True)
    data_lancamento = Column(String(11), nullable=False, index=True)

    titulolivro = relationship('Emprestimo', back_populates="livro")

    def __repr__(self):
        return '<Livro:  {} {} {} {} {} {} >'.format(self.id_livro, self.titulo, self.autor, self.resumo, self.ISBN,
                                                         self.data_lancamento)

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()

    def serialize_livro(self):
        dados_livro = {
            "id_livro": self.id_livro,
            "título": self.titulo,
            "autor": self.autor,
            "resumo": self.resumo,
            "ISBN": self.ISBN,
            "data de lançamento": self.data_lancamento,
        }
        return dados_livro

class Usuario(Base):
    __tablename__ = 'usuarios'
    id_usuario = Column(Integer, primary_key=True)
    nome = Column(String(50), nullable=False, index=True)
    CPF = Column(Integer, nullable=False, index=True)
    endereco = Column(String(90), nullable=False, index=True)
    telefone = Column(Integer, nullable=False, index=True)

    movimentacoes = relationship('Emprestimo', back_populates="usuario")

    def __repr__(self):
        return '<usuário: {} {} {} {} {}>'.format(self.id_usuario, self.nome, self.CPF, self.endereco, self.telefone)

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()

    def serialize_usuario(self):
        dados_usuario = {
            "id_usuario": self.id_usuario,
            "nome": self.nome,
            "CPF": self.CPF,
            "endereço": self.endereco,
            "telefone": self.telefone,
        }
        return dados_usuario

class Emprestimo(Base):
    __tablename__ = 'emprestimos'
    id_emprestimo = Column(Integer, primary_key=True)
    data_emprestimo = Column(String(11), nullable=False, index=True)
    data_devolucao = Column(String(11), nullable=False, index=True)
    livro_emprestado = Column(String, ForeignKey('livro.titulo'), nullable=False)
    usuario_do_emprestimo = Column(String, ForeignKey('usuario.nome'), nullable=False)
    status = Column(String, nullable=False)

    titulo = relationship('Livro', back_populates="Emprestimo")
    usuario_emprestimo = relationship('Usuario', back_populates="Emprestimo")

    def __repr__(self):
            return '<Empréstimo: {} {} {} {}>'.format(self.id_emprestimo, self.livro_emprestado, self.usuario_do_emprestimo,
                                                      self.data_emprestimo, self.data_devolucao, self.status)

    def save(self):
        """Salva a movimentação no banco de dados."""
        db_session.add(self)
        db_session.commit()

    def delete(self):
        """Deleta a movimentação do banco de dados."""
        db_session.delete(self)
        db_session.commit()

    def serialize_emprestimo(self):
            dados_emprestimo = {
                "id_emprestimo": self.id_emprestimo,
                "livro emprestado": self.livro_emprestado,
                "usuário do empréstimo": self.usuario_do_emprestimo,
                "data do empréstimo": self.data_emprestimo,
                "data de devolução": self.data_devolucao,
                "status": self.status,
            }
            return dados_emprestimo
    
def init_db():
    Base.metadata.create_all(bind=engine)


if __name__ == '__main__':
    init_db()