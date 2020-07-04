from flask import Flask, request
from flask_restful import Resource, Api
from models import Pessoas, Atividades, Usuario
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()
app = Flask(__name__)
api = Api(app)


def status(i):
    if i == 0:
        return 'pendente'
    else:
        return 'concluido'
# USUARIO ={
#     'david':'1231',
#     'israel':'321'
# }
# @auth.verify_password
# def verificacao(login, senha):
#     print('validando usuario')
#     print((USUARIO.get(login))==senha)
#     if not (login, senha):
#         return  False
#     return  USUARIO.get(login)==senha

@auth.verify_password
def verificacao(login, senha):
    if not(login, senha):
        return False
    return Usuario.query.filter_by(login = login, senha = senha).first()

class Pessoa(Resource):
    @auth.login_required
    def get(self, nome):
        pessoa = Pessoas.query.filter_by(nome=nome).first()
        #pessoa = Pessoas.query.all()
        try:
            response = {
                'nome':pessoa.nome,
                'idade':pessoa.idade,
                'id':pessoa.id
            }
        except AttributeError:
            response = {
                'status':'error',
                'mensagem':'Pessoa não encontrada'
            }
        return response
    def put(self, nome):
        pessoa = Pessoas.query.filter_by(nome=nome).first()
        dados = request.json
        if 'nome' in dados:
            pessoa.nome = dados['nome']
        if 'idade' in dados:
            pessoa.idade = dados['idade']
        pessoa.save()
        response = {
            'id':pessoa.id,
            'nome':pessoa.nome,
            'idade':pessoa.idade
        }
        return response
    def delete(self, nome):
        pessoa = Pessoas.query.filter_by(nome=nome).first()
        mensagem = 'Pessoa {} excluida com sucesso'.format(pessoa.nome)
        pessoa.delete()
        return{'status': 'sucesso', 'mensagem':mensagem}
class ListaPessoas(Resource):
    @auth.login_required
    def get(self):
        pessoas = Pessoas.query.all()
        response = [{
            'id':i.id,
            'nome':i.nome,
            'idade':i.idade
        } for i in pessoas]
        print(response)
        return response
        #for i in pessoas:
         #   lista.apend('nome':i.nome)
    def post(self):
        dados = request.json
        pessoa = Pessoas(nome=dados['nome'], idade = dados['idade'])
        pessoa.save()
        response = {
            'id':pessoa.id,
            'nome':pessoa.nome,
            'idade':pessoa.id
            }
        return response

class ListaAtividade(Resource):
    def get(self):
        atividades = Atividades.query.all()
        response = [{
            'id': i.id,
            'nome':i.nome,
            'pessoa':i.pessoa.nome,
            'status':status(i.status)
        }for i in atividades]
        return response

    def post(self):
        dados = request.json
        pessoa =  Pessoas.query.filter_by(nome=dados['pessoa']).first()
        atividade = Atividades(nome=dados['nome'], pessoa = pessoa, status = dados['status'])#Será lançado 0 no status, pois é uma atividade nova que esta pendente
        atividade.save()
        response = {
            'pessoa':atividade.pessoa.nome,
            'nome':atividade.nome,
            'id':atividade.id,
            'status':status(atividade.status)
        }
        return response
class ListarAtividadesPessoa(Resource):
    def get(self,nome):
        atividades = Atividades.query.all()
        response=[{
            'id':i.id,
            'nome':i.nome,
            'pessoa':i.pessoa.nome,
            'status':status(i.status)

        }for i in atividades if i.pessoa.nome == nome]
        return response
class ModificarStatusAtividades(Resource):
    def put(self,id):
        atividades = Atividades.query.filter_by(id=id).first()
        dados = request.json
        print(dados)
        atividades.status = dados['status']
        atividades.save()
        response = {
            'id':atividades.id,
            'nome':atividades.nome,
            'pessoa':atividades.pessoa.nome,
            'status':status(atividades.status)
            }
        return response

api.add_resource(Pessoa, '/pessoa/<string:nome>/')
api.add_resource(ListaPessoas, '/pessoa/')
api.add_resource(ListaAtividade,'/atividades/')
api.add_resource(ListarAtividadesPessoa, '/atividades/<string:nome>/')
api.add_resource(ModificarStatusAtividades, '/atividades/status/<int:id>/')
if __name__ == '__main__':
    app.run(debug=True)
