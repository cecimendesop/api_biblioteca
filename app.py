from flask import Flask, request, jsonify
from models import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'

@app.route('/cadastro-livro/', methods=['POST'])
def cadastro_livro(e):
    try:
        sql_usuarios = select(Usuario)
        resultado_usuarios = db_session.execute(sql_usuarios).scalars()
        lista_usuarios = []
        for usuario in resultado_usuarios:
            lista_usuarios.append(usuario.serialize_user())
        return jsonify({
            "usuarios": lista_usuarios
        })
    except ValueError:
        return jsonify({
            "error": "Lista indisponível"
        })

@app.route('/livros', methods=['GET'])
def livros():
    """
        Lista de Livros
           ## Endpoint:
            /livros

           ## Respostas (JSON):
           ```json

        {
            "livros": lista_livros"
        }
        ## Erros possíveis (JSON):
        "Lista indisponível"
        Bad Request***:
            ```json
           """

    try:
        sql_livros = select(Livro)
        resultado_livros = db_session.execute(sql_livros).scalars()
        lista_livros = []
        for livro in resultado_livros:
            lista_livros.append(livro.serialize_user())
        return jsonify({
            "livros": lista_livros
        })
    except ValueError:
        return jsonify({
            "error": "Lista indisponível"
        })

@app.route('/get_livro/<int:id>', methods=['GET'])
def get_livro(id):
    """
            Verifica livro
           ## Endpoint:
            /get_livro/<int:id>

            ##Parâmetros:
            "id" Id do livro

           ## Respostas (JSON):
           ```json
        {
            "id":,
            "titulo":
            "autor",
            "ISBN":,
            "resumo",
        }

        ## Erros possíveis (JSON):
            "Dados indisponíveis"
            Bad Request***:
                ```json
           """
    try:
        livro = db_session.execute(select(Livro).where(Livro.id_livro == id)).scalar()

        if not livro:
            return jsonify({
                "error": "Livro não encontrado!"
            })

        else:
            return jsonify({
                "id": livro.id,
                "titulo": livro.titulo,
                "autor": livro.autor,
                "ISBN": livro.isbn,
                "resumo": livro.resumo
            })

    except ValueError:
        return jsonify({
            "error": "Dados indisponíveis"
        })
@app.route('/emprestimos_usuario/<id>', methods=['GET'])
def emprestimos_usuario(id):
    """
           listar emprestimo por usuário.

           ## Endpoint:
            /emprestimos_usuario/<int:id>

            ##Parâmetros:
            "id" **Id do usuário**

           ## Respostas (JSON):
           ```json
            {
                "usuario":
                "emprestimo",

            }

            ## Erros possíveis (JSON):
            "Não foi possível listar os dados deste emprestimo ***400
            Bad Request***:
                ```json
           """
    try:
        id_usuario = int(id)
        emprestimos_user = db_session.execute(select(Emprestimo).where(Emprestimo.usuario_do_emprestimo== id_usuario)).scalars().all()

        if not emprestimos_user:
            return jsonify({
                "error": "Este usuário não fez emprestimo!"
            })

        else:
            emprestimos_livros = []
            for emprestimo in emprestimos_user:
                emprestimos_livros.append(emprestimo.serialize_user())
            #     livro = db_session.execute(select(Livro).where(Livro.id == emprestimo.livro_id)).scalars().all()
            #     emprestimos_livros.append(livro)
            return jsonify({
                'usuario': int(id_usuario),
                'emprestimos': emprestimos_livros,
            })
    except ValueError:
        return jsonify({
            "error": "Não foi possível listar os dados do emprestimo"
        })
@app.route('/status_livro', methods=['GET'])
def status_livro():
    """
          status de livro.

           ## Endpoint:
            /status_livro
           ## Respostas (JSON):
           ```json
           {
                "livros emprestados":
                "livros disponiveis",
            }

            ## Erros possíveis (JSON):
            "Dados de status indisponíveis"
            Bad Request***:
                ```json
            """
    try:
        livro_emprestado = db_session.execute(
            select(Livro).where(Livro.id_livro == Emprestimo.id_emprestimo).distinct(Livro.ISBN)).scalars()
        id_livro_emprestado = db_session.execute(
            select(Livro.id_livro).where(Livro.id_livro == Emprestimo.id_emprestimo).distinct(Livro.ISBN)).scalars()
        print("livro Emprestado",livro_emprestado)
        livrostatus = db_session.execute(select(Livro)).scalars()

        print("Livros todos", livrostatus)

        lista_emprestados = []
        lista_disponiveis = []
        for livro in livro_emprestado:
            lista_emprestados.append(livro.serialize_user())

        for book in livrostatus:
            if book.id not in id_livro_emprestado:
                lista_disponiveis.append(book.serialize_user())

        print("resultados lista", lista_emprestados)
        print("resultados disponibiliza", lista_disponiveis)


        return jsonify({
            "livros emprestados": lista_emprestados,
            "livros disponiveis": lista_disponiveis

        })

    except ValueError:
        return jsonify({
            "error": "dados de status indisponíveis"
        })


spec.register(app)

if __name__ == '__main__':
    app.run(debug=True)
