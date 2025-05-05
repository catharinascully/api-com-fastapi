from fastapi import FastAPI
from pydantic import BaseModel
from model.database import Database

app = FastAPI()

db = Database()
serie_db = [] # Lista que simula um banco de dados

class Serie(BaseModel):
    id: str
    titulo: str
    descricao: str
    ano_lancamento: int
    id_categoria: int

@app.post('/series/')
def cadastrar(serie: Serie):
    db.conectar()
    sql = "INSERT INTO serie (titulo, descricao, ano_lancamento, id_categoria) VALUES (%s, %s,%s,%s)"
    db.executar(sql,(serie.titulo, serie.descricao,serie.ano_lancamento, serie.id_categoria))
    db.desconectar()
    return {"mensagem": "Série cadastrada com sucesso", "serie": serie}
 
 