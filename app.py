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
    dados = request.get_json()
    print(dados)

    try:
        campos_obrigatorios = ['titulo', 'autor', 'isbn', 'resumo']
        for campo in campos_obrigatorios:
            if campo not in dados or not str(dados[campo]).strip():
                return jsonify({'erro': f"Campo obrigatório ausente ou vazio: {campo}"}), 400

        form_cadastro_livro = Livro(
            titulo=str(dados['titulo']),
            autor=str(dados['autor']),
            ISBN=int(dados['isbn']),
            resumo=str(dados['resumo']),
            status="disponível"  # status inicial
        )

        form_cadastro_livro.save()

        return jsonify({
            'Mensagem': 'Livro adicionado com sucesso',
            'titulo': form_cadastro_livro.titulo,
            'autor': form_cadastro_livro.autor,
            'isbn': form_cadastro_livro.ISBN,
            'resumo': form_cadastro_livro.resumo,
            'status': form_cadastro_livro.status
        })

    except ValueError:
        return jsonify({'erro': 'Cadastro de livro inválido!'}), 400



@app.route('/novo_usuario', methods=['POST'])
def cadastrar_usuarios():
    dados = request.get_json()
    print(dados)
    try:
        # Verificação correta dos campos
        campos_obrigatorios = ['nome', 'cpf', 'endereco']
        for campo in campos_obrigatorios:
            if campo not in dados or not str(dados[campo]).strip():
                return jsonify({'erro': f"Campo obrigatório ausente ou vazio: {campo}"}), 400

        form_cadastro_usuario = Usuario(
            nome=str(dados['nome']),
            CPF=str(dados['cpf']),
            endereco=str(dados['endereco']),
        )

        form_cadastro_usuario.save()

        return jsonify({

            'Nome': form_cadastro_usuario.nome,
            'CPF': form_cadastro_usuario.CPF,
            'Endereco': form_cadastro_usuario.endereco,
            'Mensagem': 'Usuário criado com sucesso',
        })

    except ValueError:
        return jsonify({'erro': 'Cadastro de usuário inválido!'}), 400


@app.route('/realizar_emprestimo', methods=['POST'])
def cadastrar_emprestimo():
    dados = request.get_json()
    try:
        if not all(k in dados and dados[k] for k in ("data_devolucao", "data_emprestimo", "id_usuario", "id_livro")):
            return jsonify({'erro': "Campos obrigatórios não podem ser vazios"})

        usuario = db_session.query(Usuario).filter_by(id_usuario=int(dados['id_usuario'])).first()
        livro = db_session.query(Livro).filter_by(id_livro=int(dados['id_livro'])).first()

        if not usuario or not livro:
            return jsonify({'erro': "Usuário ou livro não encontrado"})

        # Atualiza status do livro
        livro.status = "emprestado"
        livro.save()

        form_cadastro_emprestimo = Emprestimo(
            id_usuario=int(dados['id_usuario']),
            id_livro=int(dados['id_livro']),
            data_emprestimo=dados['data_emprestimo'],
            data_devolucao=dados['data_devolucao'],
            livro_emprestado=livro.titulo,
            usuario_emprestado=usuario.nome
        )

        form_cadastro_emprestimo.save()

        return jsonify({
            'Mensagem': 'Empréstimo realizado com sucesso',
            'id_usuario': form_cadastro_emprestimo.id_usuario,
            'id_livro': form_cadastro_emprestimo.id_livro,
            'data_emprestimo': form_cadastro_emprestimo.data_emprestimo,
            'data_devolucao': form_cadastro_emprestimo.data_devolucao,
            'status_livro': livro.status
        })

    except ValueError:
        return jsonify({'erro': 'Erro ao processar os dados do empréstimo'})




@app.route('/consulta_historico_emprestimo', methods=['GET'])
def historico_emprestimo():
    sql_historico_emprestimo = select(Emprestimo)
    resultado_historico_emprestimo = db_session.execute(sql_historico_emprestimo).scalars()
    lista_historico_emprestimo = []
    for n in resultado_historico_emprestimo:
        lista_historico_emprestimo.append(n.serialize_emprestimo())
    return jsonify({'historico_de_emprestimo': lista_historico_emprestimo})


@app.route('/atualizar_usuario/<int:id>', methods=['PUT'])
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

                }

               ## Erros possíveis (JSON):
                "O CPF deste usuário já está cadastrado"
                Bad Request***:
                    ```json
               """
    dados = request.get_json()
    print(dados)
    try:
        if not dados.get('nome') or not dados.get('cpf') or not dados.get('endereco'):
            return jsonify({'erro': "Campos obrigatórios não podem ser vazios"})

        usuario_editado = db_session.execute(
            select(Usuario).where(Usuario.id_usuario == int(id))
        ).scalar()

        if not usuario_editado:
            return jsonify({"erro": "Não foi possível encontrar o usuário!"})

        # Verifica se o CPF foi alterado
        cpf = dados['cpf'].strip()
        if usuario_editado.CPF != cpf:
            cpf_existe = db_session.execute(
                select(Usuario).where(Usuario.CPF == cpf)
            ).scalar()

            if cpf_existe:
                return jsonify({"erro": "Este CPF já existe!"})

        usuario_editado.nome = dados['nome']
        usuario_editado.CPF = cpf
        usuario_editado.endereco = dados['endereco']
        usuario_editado.save()

        return jsonify({
            "nome": usuario_editado.nome,
            "CPF": usuario_editado.CPF,
            "endereco": usuario_editado.endereco,
        })

    except sqlalchemy.exc.IntegrityError:
        return jsonify({"erro": "Esse CPF já foi cadastrado!"})


@app.route('/atualizar_livro/<int:id>', methods=['PUT'])
def editar_livro(id):
    dados = request.get_json()
    print(dados)

    try:
        # Verifica se as chaves existem
        if not all(key in dados for key in ("titulo", "autor", "ISBN", "resumo")):
            return jsonify({'erro': "Campos obrigatórios"})

        # Verifica se algum campo está vazio (ou só com espaços)
        if any(dados.get(key, "").strip() == "" for key in ("titulo", "autor", "ISBN", "resumo")):
            return jsonify({'erro': "Campos não podem ser vazios"})

        livro_editado = db_session.execute(select(Livro).where(Livro.id_livro == id)).scalar()

        if not livro_editado:
            return jsonify({"erro": "O livro não foi encontrado!"})

        # Atualiza o livro com os dados recebidos
        livro_editado.titulo = dados['titulo']
        livro_editado.autor = dados['autor']
        livro_editado.ISBN = dados['ISBN']
        livro_editado.resumo = dados['resumo']

        livro_editado.save()

        return jsonify({
            "titulo": livro_editado.titulo,
            "autor": livro_editado.autor,
            "ISBN": livro_editado.ISBN,
            "resumo": livro_editado.resumo
        })

    except sqlalchemy.exc.IntegrityError:
        return jsonify({"erro": "O título já foi cadastrado!"})


@app.route('/livro_status', methods=['GET'])
def livro_status():
    try:
        livros = db_session.execute(select(Livro)).scalars().all()

        lista_emprestados = [livro.serialize_livro() for livro in livros if livro.status == "emprestado"]
        lista_disponiveis = [livro.serialize_livro() for livro in livros if livro.status == "disponível"]

        return jsonify({
            "livros_emprestados": lista_emprestados,
            "livros_disponiveis": lista_disponiveis
        })

    except Exception as e:
        print("Erro ao consultar status dos livros:", e)
        return jsonify({"erro": "Dados indisponíveis"}), 500


@app.route('/editar_status_livro/<int:id>', methods=['PUT'])
def editar_status_livro(id):
    dados = request.get_json()

    if not dados or 'status' not in dados:
        return jsonify({"erro": "Campo 'status' obrigatório"}), 400

    status = dados['status'].strip().lower()
    if status not in ("disponível", "emprestado"):
        return jsonify({"erro": "Status inválido. Use 'disponível' ou 'emprestado'."}), 400

    livro = db_session.execute(select(Livro).where(Livro.id_livro == id)).scalar()

    if not livro:
        return jsonify({"erro": "Livro não encontrado"}), 404

    livro.status = status
    livro.save()

    return jsonify({
        "id_livro": livro.id_livro,
        "nome": livro.titulo,
        "status": livro.status
    }), 200





if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)