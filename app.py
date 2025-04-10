
import sqlalchemy
from sqlalchemy import *
from flask import Flask, jsonify, request
from flask_pydantic_spec import FlaskPydanticSpec
from models import *

app = Flask(__name__)
spec = FlaskPydanticSpec()


@app.route('/cadastrar_livro', methods=['GET', 'POST'])
def cadastrar_livro():
    """
       Cadastro de livro.

       ## Endpoint:
        /cadastrar_livro

       ## Respostas (JSON):
       ```json

       {
            "titulo":
            "autor",
            "ISBN":,
            "resumo",
        }

       ## Erros possíveis (JSON):
        "livro já cadastrado"
        Bad Request***:
            ```json
       """

    try:
        if request.method == 'POST':
            if (not request.form['form_titulo'] or not request.form['form_autor']
                    or not request.form['form_isbn'] or not request.form['form_resumo']):
                return jsonify({
                    "erro": "Preencher os campos em branco!!"
                })
            else:
                titulo = request.form['form_titulo'].strip()
                autor = request.form['form_autor']
                isbn = request.form['form_isbn'].strip()
                resumo = request.form['form_resumo']

                titulo_existe = db_session.execute(select(Livro).where(Livro.titulo == titulo)).scalar()
                isbn_existe = db_session.execute(select(Livro).where(Livro.ISBN == isbn)).scalar()

                if titulo_existe:
                    return jsonify({
                        "erro": "Já existe um livro com esse titulo!"
                    })

                if isbn_existe:
                    return jsonify({
                        "erro": "Já existe um livro com esse ISBN!"
                    })

                form_criar = Livro(
                    titulo=titulo,
                    autor=autor,
                    ISBN=int(isbn),
                    resumo=resumo
                )

                form_criar.save()
                # db_session.close()

                return jsonify({
                    "titulo": form_criar.titulo,
                    "autor": form_criar.autor,
                    "isbn": form_criar.ISBN,
                    "resumo": form_criar.resumo
                })

    except sqlalchemy.exc.IntegrityError:
        return jsonify({
            "erro": "livro já cadastrado!"
        })


@app.route('/cadastrar_usuario', methods=['POST', 'GET'])
def cadastrar_usuario():
    """
           Cadastro de usuário

           ## Endpoint:
            /cadastrar_usuario

           ## Respostas (JSON):
           ```json

           {
                "id":
                "nome",
                "cpf":,
                "endereco",
            }

           ## Erros possíveis (JSON):
            "usuário já cadastrado"
            Bad Request***:
                ```json
           """

    try:
        if request.method == 'POST':
            if (not request.form['form_nome'] or not request.form['form_cpf']
                    or not request.form['form_endereco']):
                return jsonify({
                    "erro": "Preencher os campos em branco!!"
                })

            else:
                nome = request.form['form_nome']
                cpf = request.form['form_cpf'].strip()
                endereco = request.form['form_endereco']

                cpf_existe = db_session.execute(select(Usuario).where(Usuario.CPF == cpf)).scalar()

                if cpf_existe:
                    return jsonify({
                        "erro": "Este CPF já existe!"
                    })

                form_criar = Usuario(
                    nome=nome,
                    CPF=int(cpf),
                    endereco=endereco,
                )

                form_criar.save()
                # db_session.close()

                return jsonify({
                    "id": form_criar.id_usuario,
                    "nome": form_criar.nome,
                    "cpf": form_criar.CPF,
                    "endereco": form_criar.endereco
                }), 201

    except sqlalchemy.exc.IntegrityError:
        return jsonify({
            "erro": "usuário já cadastrado!"
        }), 404


@app.route('/cadastrar_emprestimo', methods=['POST', 'GET'])
def cadastrar_emprestimo():
    """
           Realiza emprestimo.

           ## Endpoint:
            /cadastrar_emprestimo

           ## Respostas (JSON):
           ```json

           {
                "data_devolucao":
                "data_emprestimo",
                "livro":,
                "usuario":,
            }

           ## Erros possíveis (JSON):
            "Emprestimo já cadastrado"
            Bad Request***:
                ```json
           """
    try:
        if request.method == 'POST':
            if (not request.form['form_data_emprestimo'] or not request.form['form_data_devolucao']
                    or not request.form['form_livro'] or not request.form['form_usuario']):
                return jsonify({
                    "erro": "Preencher os campos em branco!!"
                })

            else:
                data_devolucao = request.form['form_data_devolucao']
                data_emprestimo = request.form['form_data_emprestimo']
                livro = request.form['form_livro']
                usuario = request.form['form_usuario']

                form_criar = Emprestimo(
                    data_emprestimo=data_emprestimo,
                    data_devolucao=data_devolucao,
                    livro_emprestado=livro,
                    usuario_do_emprestimo=usuario,
                )

                form_criar.save()
                # db_session.close()

                return jsonify({
                    "data_devolucao": form_criar.data_devolucao,
                    "data_emprestimo": form_criar.data_emprestimo,
                    "livro": form_criar.livro_emprestado,
                    "usuario": form_criar.usuario_do_emprestimo,
                })

    except sqlalchemy.exc.IntegrityError:
        return jsonify({
            "erro": "Empréstimo já cadastrado!"
        })

@app.route('/editar_livro/<int:id>', methods=['POST'])
def editar_livro(id):
    """
           Editar livro.
           ## Endpoint:
            /editar_livro/<int:id>

            ## Parâmetro:
            "id" **Id do livro**

           ## Respostas (JSON):
           ```json

           {
                "titulo":
                "autor",
                "ISBN":,
                "resumo",
            }

           ## Erros possíveis (JSON):
            "O titulo já está cadastrado"
            Bad Request***:
                ```json
           """
    try:
        livro_atualizado = db_session.execute(select(Livro).where(Livro.id_livro == id)).scalar()

        if not livro_atualizado:
            return jsonify({
                "erro": "Livro não encontrado!"
            })

        if request.method == 'POST':
            if (not request.form['form_titulo'] and not request.form['form_autor']
                    and not request.form['form_isbn'] and not request.form['form_resumo']):
                return jsonify({
                    "erro": "Preencher os campos em branco!!"
                })

            else:
                livro_atualizado.titulo = request.form['form_titulo']
                livro_atualizado.autor = request.form['form_autor']
                livro_atualizado.isbn = request.form['form_isbn']
                livro_atualizado.resumo = request.form['form_resumo']

                livro_atualizado.save()
                # db_session.commit()

                return jsonify({
                    "titulo": livro_atualizado.titulo,
                    "autor": livro_atualizado.autor,
                    "ISBN": livro_atualizado.isbn,
                    "resumo": livro_atualizado.resumo
                })

    except sqlalchemy.exc.IntegrityError:
        return jsonify({
            "erro": "titulo já está cadastrado!"
        })


@app.route('/editar_usuario/<int:id>', methods=['GET', 'POST'])
def editar_usuario(id):
    """
           API para editar dados do usuario.

           ## Endpoint:
            /editar_usuario/<int:id>

            ##Parâmetros:
            "id" **Id do usuario**

           ## Respostas (JSON):
           ```json

           {
                "nome":
                "cpf",
                "endereco":,
                "telefone":,
            }

           ## Erros possíveis (JSON):
            "O CPF deste usuário já está cadastrado"
            Bad Request***:
                ```json
           """

    try:
        usuario_atualizado = db_session.execute(select(Usuario).where(Usuario.id_usuario == id)).scalar()

        if not usuario_atualizado:
            return jsonify({
                "erro": "Usuário não encontrado!"
            })

        if request.method == 'POST':
            if (not request.form['form_nome'] and not request.form['form_cpf']
                    and not request.form['form_endereco']):
                return jsonify({
                    "erro": "Preencher os campos em branco!!"
                })

            else:
                cpf = request.form['form_cpf'].strip()
                if usuario_atualizado.cpf != cpf:
                    cpf_existe = db_session.execute(select(Usuario).where(Usuario.CPF == cpf)).scalar()

                    if cpf_existe:
                        return jsonify({
                            "erro": "Este CPF já existe!"
                        })

                usuario_atualizado.nome = request.form['form_nome']
                usuario_atualizado.cpf = request.form['form_cpf'].strip()
                usuario_atualizado.endereco = request.form['form_endereco']
                usuario_atualizado.telefone = request.form['form_telefone']

                usuario_atualizado.save()
                # db_session.commit()

                return jsonify({
                    "nome": usuario_atualizado.nome,
                    "cpf": usuario_atualizado.cpf,
                    "endereco": usuario_atualizado.endereco,
                    "telefone": usuario_atualizado.telefone,
                })

    except sqlalchemy.exc.IntegrityError:
        return jsonify({
            "erro": "O CPF deste usuário já está cadastrado!"
        })

@app.route('/get_usuario/<int:id>', methods=['GET'])
def get_usuario(id):
    """
           API para buscar um usuário.

           ## Endpoint:
            /get_usuario/<int:id>

            ##Parâmetros:
            "id" **Id do usuario**

           ## Respostas (JSON):
           ```json

           {
                "id_usuario":
                "nome",
                "CPF":,
                "endereco",
                "telefone":,
            }

           ## Erros possíveis (JSON):
            "Usuário não encontrado"
            Bad Request***:
                ```json
           """
    try:
        usuario = db_session.execute(select(Usuario).where(Usuario.id_usuario == id)).scalar()

        if not usuario:
            return jsonify({
                "erro": "Usuário não encontrado"
            })

        else:
            return jsonify({
                "id": usuario.id,
                "nome": usuario.nome,
                "cpf": usuario.cpf,
                "endereco": usuario.endereco,
                "telefone": usuario.telefone
            })
    except ValueError:
        return jsonify({
            "error": "Lista indisponível"
        })

@app.route('/usuarios', methods=['GET'])
def usuarios():
    """
           Lista de usuários.
           ## Endpoint:
            /usuarios

           ## Respostas (JSON):
           ```json

           {
                "usuarios": lista_usuarios
            }

    """
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
