from flask import Flask, jsonify, request
import json

#Escrever no arquivo json
def EscreverJson(usuarios_dados):
    with open('Usuarios.json','w') as dados:
        dados.write(json.dumps(usuarios_dados, indent=4, sort_keys=True))

#Abrindo arquivo json
with open('Usuarios.json') as dados:    
    try:
        usuarios_dados = json.load(dados)
    except:
        usuarios_dados = []


app = Flask(__name__)

#Rota que retorna todos os usuarios
@app.route("/", methods=['GET'])
def retornaUsuario():
    return jsonify(usuarios_dados)

#Rota que adiciona um usuario
@app.route("/usuarios", methods=['POST'])
def addUsuario():
    try:
        usuario = {'Nome': request.json['Nome'], 'ID':(max(usuarios_dados, key=lambda item:item['ID'])['ID']+1)}
    except:
         usuario = {'Nome': request.json['Nome'], 'ID':1}
    usuarios_dados.append(usuario)
    EscreverJson(usuarios_dados)

    return jsonify(usuarios_dados)

#Rota que modifica um usuario
@app.route("/usuarios/<string:nome>", methods=['PUT'])
def editUsuario(nome):
    try:
        usuario = [usuario for usuario in usuarios_dados if usuario['Nome'] == nome]
        usuario[0]['Nome'] = request.json['Nome']
        EscreverJson(usuarios_dados)
        return jsonify(usuarios_dados)
    except:
        return "Usuário não existe"

#Rota que deleta um usuario
@app.route("/usuarios/<string:nome>", methods=['DELETE'])
def deletUsuario(nome):
    try:
        usuario = [usuario for usuario in usuarios_dados if usuario['Nome'] == nome]
        usuarios_dados.remove(usuario[0])
        EscreverJson(usuarios_dados)
        return jsonify(usuarios_dados)
    except:
        return "Usuário não existe"

if __name__ == "__main__":
    app.run(debug = True,port=8080)