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
    dados = Usuario.query.filter_by(login = login).first()
    #print('Status do usuario {} = {}'.format(login, dados.ativo))
    if dados.ativo ==0:
        print('Usuario {} desstivado'.format(login))
        response = False

    else:
        #print('Usuario {} Ativado'.format(login))
        if not(login, senha):
            response = False
        else:
            response =Usuario.query.filter_by(login = login, senha = senha).first()
    return response
class Pessoa(Resource):

    def get(self, nome):
        pessoa = Pessoas.query.filter_by(nome=nome).first()

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

    @auth.login_required
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

    @auth.login_required
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

    @auth.login_required
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

    @auth.login_required
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

class ModificarAtividades(Resource):
    def get(self,id):
        try:
            atividades = Atividades.query.filter_by(id=id).first()
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
    @auth.login_required
    def put(self,id):
        try:
            atividades = Atividades.query.filter_by(id=id).first()
            dados = request.json
            #print(dados)
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

    @auth.login_required
    def delete(self,id):
        try:
            atividade = Atividades.query.filter_by(id=id).first()
            mensagem = 'Atividade {} excluida com sucesso'.format(atividade.id)
            atividade.delete()
            response ={'status': 'sucesso', 'mensagem':mensagem}

        except AttributeError:
            mensagem = 'não foi encontrado o registro <{}> para deletar'.format(id)
            response = {'status':'error','mensagem':mensagem}
        except Exception:
            response = {'status': 'erro', 'mensagem': 'erro desconhecido contate o administrador da API'}
        return response


api.add_resource(Pessoa, '/pessoa/<string:nome>/')#listar, modificar, deletar uma pessoa
api.add_resource(ListaPessoas, '/pessoa/')#listar todas as pessoas e incluir pessoas
api.add_resource(ListaAtividade,'/atividades/')#listar todas as atividades e incluir atividades
api.add_resource(ListarAtividadesPessoa, '/atividades/<string:nome>/')#listar todas as atividades pelo nome da pessoa
api.add_resource(ModificarAtividades, '/atividades/<int:id>/')#listar, modificar o status e deletar através do id
if __name__ == '__main__':
    app.run(debug=True)
