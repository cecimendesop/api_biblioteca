import sqlalchemy
from flask import Flask, jsonify, request
from flask_jwt_extended import create_access_token, get_jwt_identity, JWTManager, jwt_required
from functools import wraps
from sqlalchemy import select
from models import Livro, Usuario, Emprestimo, local_session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
jwt = JWTManager(app)

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        current_user = get_jwt_identity()
        db_session = local_session()
        try:  # user atual
            print(current_user)
            sql = select(Usuario).where(Usuario.CPF == current_user)
            user = db_session.execute(sql).scalar()
            print(user)
            if user and user.papel == "admin":
                return fn(*args, **kwargs)
            else:
                return jsonify({"msg": "Acesso negado: Requer privilégios de administrador"}), 403
        finally:
            db_session.close()

    return wrapper

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
    db_session = local_session()
    sql_livros = select(Livro)
    resultado_livros = db_session.execute(sql_livros).scalars()
    lista_livros = []
    for n in resultado_livros:
        lista_livros.append(n.serialize_livro())
    return jsonify({'livros': lista_livros})


@app.route('/usuarios', methods=['GET'])
def usuarios():
    # protegido
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
    db_session = local_session()
    sql_usuarios = select(Usuario)
    resultado_usuarios = db_session.execute(sql_usuarios).scalars()
    lista_usuarios = []
    for n in resultado_usuarios:
        lista_usuarios.append(n.serialize_usuario())
    return jsonify({'usuarios': lista_usuarios})


@app.route('/emprestimos', methods=['GET'])
def emprestimos():
    db_session = local_session()
    sql_emprestimos = select(Emprestimo)
    resultado_emprestimos = db_session.execute(sql_emprestimos).scalars()
    lista_emprestimos = []
    for n in resultado_emprestimos:
        lista_emprestimos.append(n.serialize_emprestimo())
    return jsonify({'emprestimos': lista_emprestimos})

@app.route('/novo_livro', methods=['POST'])
@jwt_required()
@admin_required
def cadastrar_livros():
    # proteger - apenas adm
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
    db_session = local_session()
    dados = request.get_json()
    print(dados)

    try:
        if dados['titulo'] == "" or dados['autor'] == "" or dados['isbn'] == "" or dados['resumo'] == "":
            return jsonify({'erro': "Campos não podem ser vazios"})
        else:
            form_cadastro_livro = Livro(
                titulo=str(dados['titulo']),
                autor=str(dados['autor']),
                ISBN=int(dados['isbn']),
                resumo=str(dados['resumo'])
            )

            form_cadastro_livro.save(db_session)

            return jsonify({
                'Mensagem': 'Livro adicionado com sucesso',
                'titulo': form_cadastro_livro.titulo,
                'autor': form_cadastro_livro.autor,
                'isbn': form_cadastro_livro.ISBN,
                'resumo': form_cadastro_livro.resumo
            }), 201
    except ValueError:
        return jsonify({
            'erro': 'cadastro de livro inválida!'
        })

@app.route('/login', methods=['POST'])
def login():
    dados = request.get_json()
    cpf = dados['cpf']
    senha = dados['senha']

    db_session = local_session()

    try:
        sql = select(Usuario).where(Usuario.CPF == cpf)
        user = db_session.execute(sql).scalar()
        print(user)

        if user and user.check_password(senha):
            access_token = create_access_token(identity=user.CPF)
            return jsonify(access_token=access_token)
        return jsonify({"msg": "Credenciais inválidas"}), 401
    finally:
        db_session.close()

@app.route('/novo_usuario', methods=['POST'])
@jwt_required()
@admin_required
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
    db_session = local_session()
    dados = request.get_json()
    print(dados)
    try:
        if dados['nome'] == "" or dados['cpf'] == "" or dados['endereco'] == "":
            return jsonify({'erro': "Campos não podem ser vazios"})
        form_cadastro_usuario = Usuario(
            nome=str(dados['nome']),
            CPF=str(dados['cpf']),
            endereco=str(dados['endereco']),
            papel=str(dados.get('papel', 'usuario'))
        )
        form_cadastro_usuario.set_senha_hash(dados['senha_hash'])

        form_cadastro_usuario.save(db_session)

        return jsonify({
            'Mensagem': 'Usuário criado com sucesso',
            'nome': form_cadastro_usuario.nome,
            'cpf': form_cadastro_usuario.CPF,
            'endereco': form_cadastro_usuario.endereco,
            'papel': form_cadastro_usuario.papel
        }), 201

    except ValueError:
        return jsonify({
            'erro': 'cadastro de usuário inválida!'
        })


@app.route('/realizar_emprestimo', methods=['POST'])
@jwt_required()
@admin_required
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
    db_session = local_session()
    dados = request.get_json()
    print(dados)
    try:
        if dados['data_devolucao'] == "" or dados['data_emprestimo'] == "":
            return jsonify({'erro': "Campos não pode ser vazio"})

        form_cadastro_emprestimo = Emprestimo(
            id_usuario=int(dados['id_usuario']),
            id_livro=int(dados['id_livro']),
            data_emprestimo=(dados['data_emprestimo']),
            data_devolucao=(dados['data_devolucao']),
        )
        form_cadastro_emprestimo.save(db_session)
        return jsonify({
            'Mensagem': 'Empréstimo realizado com sucesso',
            'id_usuario': form_cadastro_emprestimo.id_usuario,
            'id_livro': form_cadastro_emprestimo.id_livro,
            'data_emprestimo': form_cadastro_emprestimo.data_emprestimo,
            'data_devolucao': form_cadastro_emprestimo.data_devolucao,
        }), 201

    except ValueError:
        return jsonify({
            'erro': 'cadastro de usuário inválida!'
        })


@app.route('/atualizar_usuario/<id>', methods=['PUT'])
@jwt_required()
@admin_required
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
    db_session = local_session()
    dados = request.get_json()
    print(dados)
    try:
        if not "nome" in dados or not "cpf" in dados:
            return jsonify({'erro': "Campos obrigatorios"}),400
        if dados['nome'] == "" or dados['cpf'] == "" or dados['endereco'] == "":
            return jsonify({'erro': "Campos não pode ser vazio"}),400

        usuario_editado = db_session.execute(select(Usuario).where(Usuario.id_usuario == id)).scalar()

        if not usuario_editado:
            return jsonify({
                "erro": "Não foi possível encontrar o usuário!"
            }),400

        if request.method == 'PUT':
            if (not dados['nome'] and not dados['cpf']
                    and not dados['endereco']):
                return jsonify({
                    "erro": "Os campos não devem ficar em branco!"
                }),400

            else:
                cpf = dados['cpf'].strip()
                if usuario_editado.CPF != cpf:
                    cpf_existe = db_session.execute(select(Usuario).where(Usuario.CPF == cpf)).scalar()

                    if cpf_existe:
                        return jsonify({
                            "erro": "Este CPF já existe!"
                        })

                usuario_editado.nome = (dados['nome'])
                usuario_editado.CPF = (dados['cpf']).strip()
                usuario_editado.endereco = (dados['endereco'])

                usuario_editado.save(db_session)

                return jsonify({
                    "nome": usuario_editado.nome,
                    "cpf": usuario_editado.CPF,
                    "endereco": usuario_editado.endereco,
                }),200

    except sqlalchemy.exc.IntegrityError:
        return jsonify({
            "erro": "Esse CPF já foi cadastrado!"
        })


@app.route('/atualizar_livro/<id>', methods=['PUT'])
@jwt_required()
@admin_required
def editar_livro(id):
    # protegido
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
    db_session = local_session()
    dados = request.get_json()
    print("gggg: ",dados)
    try:
        if not "titulo" or not "autor" or not "isbn" in dados:
            return jsonify({'erro': "Campos obrigatorios"}),400
        if dados['titulo'] == "" or dados['autor'] == "" or dados['isbn'] == "" or dados['resumo'] == "":
            return jsonify({'erro': "Campos não pode ser vazio"}),400

        livro_editado = db_session.execute(select(Livro).where(Livro.id_livro == id)).scalar()
        print(livro_editado)

        if not livro_editado:
            return jsonify({
                "erro": "O livro não foi encontrado!"
            }),400

        if (not dados['titulo'] and not dados['autor']
                and not dados['isbn'] and not dados['resumo']):
            return jsonify({
                "erro": "Os campos não devem ficar em branco!"
            }),400

        else:
            livro_editado.titulo = (dados['titulo'])
            livro_editado.autor = (dados['autor'])
            livro_editado.ISBN = (dados['isbn'])
            livro_editado.resumo = (dados['resumo'])

            livro_editado.save(db_session)

            return jsonify({
                "titulo": livro_editado.titulo,
                "autor": livro_editado.autor,
                "isbn": livro_editado.ISBN,
                "resumo": livro_editado.resumo
            }),200

    except sqlalchemy.exc.IntegrityError:
        return jsonify({
            "erro": "O titulo já foi cadastrado!"
        }),400
    except Exception as e:
        return jsonify({
            "erro": str(e)
        })



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
