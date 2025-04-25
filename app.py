import sqlalchemy
from flask import Flask, jsonify, request
from sqlalchemy import select
from models import Livro, Usuario, Emprestimo, db_session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'

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
    sql_livros = select(Livro)
    resultado_livros = db_session.execute(sql_livros).scalars()
    lista_livros = []
    for n in resultado_livros:
        lista_livros.append(n.serialize_livro())
    return jsonify({'lista_livros': lista_livros})

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
    sql_usuarios = select(Usuario)
    resultado_usuarios = db_session.execute(sql_usuarios).scalars()
    lista_usuarios = []
    for n in resultado_usuarios:
        lista_usuarios.append(n.serialize_usuario())
    return jsonify({'lista_usuarios': lista_usuarios})

@app.route('/emprestimos', methods=['GET'])
def emprestimos():
    sql_emprestimos = select(Emprestimo)
    resultado_emprestimos = db_session.execute(sql_emprestimos).scalars()
    lista_emprestimos = []
    for n in resultado_emprestimos:
        lista_emprestimos.append(n.serialize_emprestimo())
    return jsonify({'lista_emprestimos' : lista_emprestimos})

@app.route('/novo_livro', methods=['POST'])
def cadastrar_livros():
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
    dados = request.get_json()
    print(dados)

    try:
        if not "titulo" or not "autor" or not "ISBN" in dados:
            return jsonify({'erro':"Campos obrigatorios"})
        if dados['titulo'] or ['autor'] or ['ISBN'] or ['resumo'] == "":
            return jsonify({'erro': "Campos não pode ser vazio"})
        form_cadastro_livro = Livro(
            titulo=str (dados['titulo']),
            autor=str(dados['autor']),
            ISBN=int(dados['ISBN']),
            resumo=str(dados['resumo'])
        )

        form_cadastro_livro.save()

        return jsonify({
            'Mensagem': 'Livro adicionado com sucesso',
            'Titulo': form_cadastro_livro.titulo,
            'Autor': form_cadastro_livro.autor,
            'ISBN': form_cadastro_livro.ISBN,
            'Resumo': form_cadastro_livro.resumo
        })

    except ValueError:
        return jsonify({
            'erro':'cadastro de livro inválida!'
        })

@app.route('/novo_usuario', methods=['POST'])
def cadastrar_usuarios():
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
    dados = request.get_json()
    print(dados)
    try:
        if not "nome" or not "cpf" in dados:
            return jsonify({'erro':"Campos obrigatorios"})
        if dados['nome'] or ['cpf'] or ['endereco'] == "":
            return jsonify({'erro': "Campos não pode ser vazio"})
        form_cadastro_usuario = Usuario(
            nome=str(dados['nome']),
            CPF=str(dados['cpf']),
            endereco=str(dados['endereco']),
        )

        form_cadastro_usuario.save()

        return jsonify({
            'Mensagem': 'Usuário criado com sucesso',
            'Nome': form_cadastro_usuario.nome,
            'CPF': form_cadastro_usuario.CPF,
            'Endereco': form_cadastro_usuario.endereco,
        })

    except ValueError:
        return jsonify({
            'erro':'cadastro de usuário inválida!'
        })

@app.route('/realizar_emprestimo', methods=['POST'])
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
    dados = request.get_json()
    print(dados)
    try:
        if not "data_devolucao" or not "data_emprestimo" in dados:
            return jsonify({'erro':"Campos obrigatorios"})
        if dados['data_devolucao'] or ['data_emprestimo'] == "":
            return jsonify({'erro': "Campos não pode ser vazio"})

        form_cadastro_emprestimo = Emprestimo(
            id_usuario = int(dados['id_usuario']),
            id_livro = int(dados['id_livro']),
            data_emprestimo = (dados['data_emprestimo']),
            data_devolucao = (dados['data_devolucao']),
        )
        return jsonify({
            'Mensagem': 'Empréstimo realizado com sucesso',
            'id_usuario': form_cadastro_emprestimo.id_usuario,
            'id_livro': form_cadastro_emprestimo.id_livro,
            'data_emprestimo': form_cadastro_emprestimo.data_emprestimo,
            'data_devolucao': form_cadastro_emprestimo.data_devolucao,
        })

    except ValueError:
        return jsonify({
            'erro':'cadastro de usuário inválida!'
        })

@app.route('/consulta_historico_emprestimo', methods=['GET'])
def historico_emprestimo():
    sql_historico_emprestimo = select(Emprestimo)
    resultado_historico_emprestimo = db_session.execute(sql_historico_emprestimo).scalars()
    lista_historico_emprestimo = []
    for n in resultado_historico_emprestimo:
        lista_historico_emprestimo.append(n.serialize_emprestimo())
    return jsonify({'historico_de_emprestimo': lista_historico_emprestimo})


@app.route('/atualizar_usuario/<id>', methods=['PUT'])
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
    dados = request.get_json()
    print(dados)
    try:
        if not "nome" or not "cpf" in dados:
            return jsonify({'erro':"Campos obrigatorios"})
        if dados['nome'] or ['cpf'] or ['endereco'] == "":
            return jsonify({'erro': "Campos não pode ser vazio"})

        usuario_editado = db_session.execute(select(Usuario).where(Usuario.id_usuario == id)).scalar()

        if not usuario_editado:
            return jsonify({
                "erro": "Não foi possível encontrar o usuário!"
            })

        if request.method == 'PUT':
            if (not request.form['form_nome'] and not request.form['form_CPF']
                    and not request.form['form_endereco']):
                return jsonify({
                    "erro": "Os campos não devem ficar em branco!"
                })

            else:
                cpf = request.form['form_CPF'].strip()
                if usuario_editado.cpf != cpf:
                    cpf_existe = db_session.execute(select(Usuario).where(Usuario.CPF == cpf)).scalar()

                    if cpf_existe:
                        return jsonify({
                            "erro": "Este CPF já existe!"
                        })

                usuario_editado.nome = (dados['form_nome'])
                usuario_editado.CPF = (dados['form_cpf']).strip()
                usuario_editado.endereco = (dados['form_endereco'])

                usuario_editado.save()

                return jsonify({
                    "nome": usuario_editado.nome,
                    "CPF": usuario_editado.CPF,
                    "endereco": usuario_editado.endereco,
                })

    except sqlalchemy.exc.IntegrityError:
        return jsonify({
            "erro": "Esse CPF já foi cadastrado!"
        })

@app.route('/atualizar_livro/<id>', methods=['PUT'])
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
    dados = request.get_json()
    print(dados)
    try:
        if not "titulo" or not "autor" or not "ISBN" in dados:
            return jsonify({'erro':"Campos obrigatorios"})
        if dados['titulo'] or ['autor'] or ['ISBN'] or ['resumo '] == "":
            return jsonify({'erro': "Campos não pode ser vazio"})

        livro_editado = db_session.execute(select(Livro).where(Livro.id_livro == id)).scalar()

        if not livro_editado:
            return jsonify({
                "erro": "O livro não foi encontrado!"
            })

        if request.method == 'PUT':
            if (not request.form['form_titulo'] and not request.form['form_autor']
                    and not request.form['form_ISBN'] and not request.form['form_resumo']):
                return jsonify({
                    "erro": "Os campos não devem ficar em branco!"
                })

            else:
                livro_editado.titulo = (dados['form_titulo'])
                livro_editado.autor = (dados['form_autor'])
                livro_editado.ISBN = (dados['form_ISBN'])
                livro_editado.resumo = (dados['form_resumo'])

                livro_editado.save()

                return jsonify({
                    "titulo": livro_editado.titulo,
                    "autor": livro_editado.autor,
                    "ISBN": livro_editado.ISBN,
                    "resumo": livro_editado.resumo
                })

    except sqlalchemy.exc.IntegrityError:
        return jsonify({
            "erro": "O titulo já foi cadastrado!"
        })

@app.route('/livro_status', methods=['GET'])
def livro_status():
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
            select(Livro).where(Livro.id_livro == Emprestimo.id_livro).distinct(Livro.ISBN)
        ).scalars()

        id_livro_emprestado = db_session.execute(
            select(Emprestimo.id_livro).distinct(Emprestimo.id_livro)
        ).scalars().all()

        print("livro Emprestados",livro_emprestado)
        print("ids_livro_emprestado",id_livro_emprestado)
        livrostatus = db_session.execute(select(Livro)).scalars()

        print("Todos os livros", livrostatus)

        lista_emprestados = []
        lista_disponiveis = []
        for livro in livro_emprestado:
            lista_emprestados.append(livro.serialize_livro())

        print("Resultados da lista:", lista_emprestados)

        for livro in livrostatus:
            if livro.id_livro not in id_livro_emprestado:
                lista_disponiveis.append(livro.serialize_livro())

        print("Resultados disponiveis", lista_disponiveis)


        return jsonify({
            "Livros emprestados": lista_emprestados,
            "Livros disponiveis": lista_disponiveis

        })

    except ValueError:
        return jsonify({
            "error": "Dados indisponíveis"
        })


if __name__ == '__main__':
    app.run(debug=True)