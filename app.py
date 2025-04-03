from flask import Flask, request, jsonify
from models import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'

@app.route('/cadastro-livro/', methods=['POST'])
def cadastro_livro(e):
    try:
        form_cadastro = Livro(
            id_livro=int(request.form['id_livro']),
            titulo=request.form['titulo'],
            autor=request.form['autor'],
            resumo=request.form['resumo'],
            ISBN=int(request.form['ISBN']),
            data_lancamento=request.form['data_lancamento'],
        )
        form_cadastro.save()
        return jsonify('Livro cadastrado com sucesso!')
    except ValueError:
        return jsonify('Erro na requisição!')

if __name__ == '__main__':
    app.run(debug=True)
