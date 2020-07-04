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
        except Exception:
            response = {'status': 'erro', 'mensagem': 'erro desconhecido contate o administrador da API'}
        return response
    def put(self, nome):
        try:
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
        except AttributeError:
            mensagem='O nome <{}> não foi encontrado na base de dados'.format(nome)
            response = {'status':'erro', 'mensagem':mensagem}
        except Exception:
            response = {'status':'erro', 'mensagem':'erro desconhecido contate o administrador da API'}
        return response
    def delete(self, nome):
        try:
            pessoa = Pessoas.query.filter_by(nome=nome).first()
            mensagem = 'Pessoa {} excluida com sucesso'.format(pessoa.nome)
            pessoa.delete()
            response ={'status': 'sucesso', 'mensagem':mensagem}

        except AttributeError:
            mensagem = 'não foi encontrado o registro <{}> para deletar'.format(nome)
            response = {'status':'error','mensagem':mensagem}
        except Exception:
            response = {'status': 'erro', 'mensagem': 'erro desconhecido contate o administrador da API'}
        return response
class ListaPessoas(Resource):
    @auth.login_required
    def get(self):
        try:
            pessoas = Pessoas.query.all()
            response = [{
                'id':i.id,
                'nome':i.nome,
                'idade':i.idade
            } for i in pessoas]
        except Exception:
            response = {'status': 'erro', 'mensagem': 'erro desconhecido contate o administrador da API'}
        return response

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
        try:
            atividades = Atividades.query.all()
            response = [{
                'id': i.id,
                'nome':i.nome,
                'pessoa':i.pessoa.nome,
                'status':status(i.status)
            }for i in atividades]
        except Exception:
            response = {'status': 'erro', 'mensagem': 'erro desconhecido contate o administrador da API'}
        return response

    def post(self):
        try:
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
        except AttributeError:
            mensagem = 'O nome <{}> não foi encontrado na base de dados'.format(dados['pessoa'])
            response = {'status': 'erro', 'mensagem': mensagem}
        except Exception:
            response = {'status': 'erro', 'mensagem': 'erro desconhecido contate o administrador da API'}
        return response
class ListarAtividadesPessoa(Resource):
    def get(self,nome):
        try:
            atividades = Atividades.query.all()
            response=[{
                'id':i.id,
                'nome':i.nome,
                'pessoa':i.pessoa.nome,
                'status':status(i.status)

            }for i in atividades if i.pessoa.nome == nome]
        except AttributeError:
            mensagem = 'O nome <{}> não foi encontrado na base de dados'.format(nome)
            response = {'status': 'erro', 'mensagem': mensagem}
        except Exception:
            response = {'status': 'erro', 'mensagem': 'erro desconhecido contate o administrador da API'}
        return response
class ModificarStatusAtividades(Resource):
    def put(self,id):
        try:
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
        except AttributeError:
            mensagem = 'O id <{}> não foi encontrado na base de dados'.format(id)
            response = {'status': 'erro', 'mensagem': mensagem}
        except Exception:
            response = {'status': 'erro', 'mensagem': 'erro desconhecido contate o administrador da API'}
        return response

api.add_resource(Pessoa, '/pessoa/<string:nome>/')
api.add_resource(ListaPessoas, '/pessoa/')
api.add_resource(ListaAtividade,'/atividades/')
api.add_resource(ListarAtividadesPessoa, '/atividades/<string:nome>/')
api.add_resource(ModificarStatusAtividades, '/atividades/status/<int:id>/')
if __name__ == '__main__':
    app.run(debug=True)
