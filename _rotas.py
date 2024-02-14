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


@app.route('/grupo', methods=['GET'])
def grupo():
    return render_template("_grupo.html")


@app.route('/contato', methods=['GET'])
def contato():
    return render_template("_contato.html")


if __name__ == '__main__':
    app.run(debug=True)

# para comentar o código no vscode é só selecionar o que quer comentar e prescionar ctrl+;
