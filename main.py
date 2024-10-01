#Importações
import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Float, String
from sqlalchemy.orm import sessionmaker

#Criando conexão

def criar_conexão():
    try:
        engine = db.create_engine('mysql+pymysql://root:@localhost:3306/escola')
        print('Egine criada com sucesso')
        return engine
    except Exception as error:
        print(f'Falha conexão! {error}')


#Criar tabela
Base = declarative_base()
class Aluno(Base):
    __tablename__ = 'alunos'

    matricula = Column(Integer, primary_key = True,  autoincrement=True)
    nome = Column(String(180), nullable = False)
    idade = Column(Integer, nullable= True)
    nota = Column(Float, nullable = False, default = 0)

    def __repr__(self):
        return f'({self.matricula}, {self.nome}, {self.idade}, {self.nota})'


#conexao = criar_conexão()
#Base.metadata.create_all(conexao)

#criando sessão
conexao = criar_conexão()
Session = sessionmaker(bind=conexao)
session = Session()

def add_aluno(nome:str,idade:int,nota:float):
    aluno1 = Aluno(nome = nome, idade = idade, nota = nota)
    session.add(aluno1)
    session.commit()
    return aluno1


#Liatando alunos

def listar_alunos():
    alunos = session.query(Aluno).all()
    for aluno in alunos:
        print(aluno)

    return alunos

def buscar_por_matricula(matricula:int):
    aluno = session.query(Aluno).filter(Aluno.matricula==matricula).one_or_none()
    return aluno
    

#Alterando dados da tabela
def editar_aluno(matricula:int, nome:str,idade:int,nota:float):
    aluno = session.query(Aluno).filter(Aluno.matricula==matricula).one_or_none()
    if aluno:
        aluno.nome = nome
        aluno.idade = idade
        aluno.nota = nota
        session.commit()
        print('Aluno alterado com sucessso')
        return aluno
    else:
        print('Aluno não encontrado!!!')


def remover_aluno(matricula:int):
    aluno = session.query(Aluno).filter(Aluno.matricula==matricula).one_or_none()
    if aluno:
        session.delete(aluno)
        session.commit()
        print('Aluno removido com sucesso')
        return []
    else:
        print('Aluno não encontrado')

#add_aluno(nome='Maria',idade=22,nota=8.8)    
#listar_alunos()
#editar_aluno(matricula=2,nome='Jose',idade=25,nota= 7.2)
#buscar_por_matricula(2)
#remover_aluno(4)
#istar_alunos()

#Realizando testes
import unittest
class TestCrudAlunosUnit(unittest.TestCase):
    def test_funcao_add_aluno(self):
        aluno = add_aluno(nome='Vanessa',idade=25, nota=9)
        self.assertEqual(aluno.nome,'Vanessa')
        self.assertEqual(aluno.idade,25)
        self.assertEqual(aluno.nota,9)
        self.assertIsInstance(aluno, Aluno)
