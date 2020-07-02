from models import Pessoas

#Inserir dados na tabela pessoa
def insere_pessoas():
    pessoa = Pessoas(nome ='Israel', idade=40)
    print(pessoa)
    pessoa.save()

#Consulta dados na tabela pessoa
def consulta_pessoas():
    pessoas = Pessoas.query.all()
    print(pessoas)
    for i in pessoas:
        print(i.nome)
    pessoa = Pessoas.query.filter_by(nome='David').first()
    print(pessoa.idade)
    print(pessoa)

#Altera dados na tabela pessoa
def alterar_pessoa():
    pessoa = Pessoas.query.filter_by(nome = 'David').first()
    pessoa.idade = 21
    pessoa.save()

#Excluir dados na tabela pessoa
def excluir_pessoa():
    pessoa = Pessoas.query.filter_by(nome='Marcos').first()
    pessoa.delete()

if __name__ == '__main__':
    #insere_pessoas()
    excluir_pessoa()
    consulta_pessoas()
    #alterar_pessoa()