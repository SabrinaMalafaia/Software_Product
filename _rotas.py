from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    return render_template("_index.html")


@app.route('/objetivo', methods=['GET'])
def objetivo():
    return render_template("_objetivo.html")


@app.route('/parceiro', methods=['GET'])
def parceiro():
    return render_template("_parceiro.html")


@app.route('/buscar_parceiro', methods=['GET'])
def buscar_parceiro():
    return render_template("_buscarParceiro.html")


@app.route('/listar_parceiro', methods=['GET'])
def listar_parceiro():
    return render_template("_listarParceiros.html")


@app.route('/cadastrar_parceiro', methods=['GET'])
def cadastrar_parceiro():
    return render_template("_cadastrarParceiro.html")


@app.route('/grupo', methods=['GET'])
def grupo():
    return render_template("_grupo.html")


@app.route('/buscar_grupo', methods=['GET'])
def buscar_grupo():
    return render_template("_buscarGrupo.html")


@app.route('/listar_grupo', methods=['GET'])
def listar_grupo():
    return render_template("_listarGrupos.html")


@app.route('/cadastrar_grupo', methods=['GET'])
def cadastrar_grupo():
    return render_template("_cadastrarGrupo.html")


@app.route('/contato', methods=['GET'])
def contato():
    return render_template("_contato.html")


if __name__ == '__main__':
    app.run(debug=True)

# para comentar o código no vscode é só selecionar o que quer comentar e prescionar ctrl+;
