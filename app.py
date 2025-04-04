from flask import Flask, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Livro, Usuario, Emprestimo

DATABASE_URL = "sqlite:///./biblioteca.sqlite3"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

app = Flask(__name__)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.route("/livros/", methods=["POST"])
def criar_livro():
    data = request.form
    if not all(k in data for k in ("titulo", "autor", "isbn", "formato", "resumo")):
        return jsonify({"error": "Todos os campos são obrigatórios."}), 400
    db = SessionLocal()
    novo_livro = Livro(**data)
    db.add(novo_livro)
    db.commit()
    db.refresh(novo_livro)
    db.close()
    return jsonify({"message": "Livro criado com sucesso", "data": data})

@app.route("/usuarios/", methods=["POST"])
def criar_usuario():
    data = request.form
    if not all(k in data for k in ("nome", "cpf", "endereco")):
        return jsonify({"error": "Todos os campos são obrigatórios."}), 400
    db = SessionLocal()
    if db.query(Usuario).filter(Usuario.cpf == data["cpf"]).first():
        db.close()
        return jsonify({"error": "CPF já cadastrado."}), 400
    novo_usuario = Usuario(**data)
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    db.close()
    return jsonify({"message": "Usuário criado com sucesso", "data": data})

@app.route("/usuarios/<int:usuario_id>", methods=["PUT"])
def editar_usuario(usuario_id):
    data = request.form
    db = SessionLocal()
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        db.close()
        return jsonify({"error": "Usuário não encontrado"}), 404
    for key, value in data.items():
        setattr(usuario, key, value)
    db.commit()
    db.close()
    return jsonify({"message": "Usuário atualizado com sucesso"})

@app.route("/livros/disponiveis", methods=["GET"])
def listar_livros_disponiveis():
    db = SessionLocal()
    livros_emprestados = db.query(Emprestimo.livro_id).all()
    ids_emprestados = {emprestimo.livro_id for emprestimo in livros_emprestados}
    livros_disponiveis = db.query(Livro).filter(~Livro.id.in_(ids_emprestados)).all()
    db.close()
    return jsonify({"message": "Lista de livros disponíveis", "data": [livro.titulo for livro in livros_disponiveis]})

@app.route("/livros/<int:livro_id>", methods=["PUT"])
def editar_livro(livro_id):
    data = request.form
    db = SessionLocal()
    livro = db.query(Livro).filter(Livro.id == livro_id).first()
    if not livro:
        db.close()
        return jsonify({"error": "Livro não encontrado"}), 404
    for key, value in data.items():
        setattr(livro, key, value)
    db.commit()
    db.close()
    return jsonify({"message": "Livro atualizado com sucesso"})

if __name__ == "__main__":
    app.run(debug=True)

