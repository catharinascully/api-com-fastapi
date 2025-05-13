from fastapi import FastAPI
from model.database import Database
from model.models import Serie, Ator, Categoria, Motivo, Avaliacao

app = FastAPI()
db = Database()

@app.post('/serie/')
def cadastrar_serie(serie: Serie):
    db.conectar()
    sql = "INSERT INTO serie (titulo, descricao, ano_lancamento, id_categoria) VALUES (%s, %s,%s,%s)"
    db.executar(sql,(serie.titulo, serie.descricao,serie.ano_lancamento, serie.id_categoria))
    db.desconectar()
    return {"mensagem": "Série cadastrada com sucesso"}

@app.post('/ator/')
def cadastrar_ator(ator: Ator):
    db.conectar()
    sql = "INSERT INTO ator (nome) VALUES (%s)"
    db.executar(sql,(ator.nome,))
    db.desconectar()
    return {"mensagem": "Ator cadastrada com sucesso"}

@app.post('/categoria/')
def cadastrar_categoria(categoria: Categoria):
    db.conectar()
    sql = "INSERT INTO categoria (nome) VALUES (%s)"
    db.executar(sql,(categoria.nome,))
    db.desconectar()
    return {"mensagem": "Categoria cadastrada com sucesso"}

@app.post('/motivos/')
def cadastrar_motivo(motivo: Motivo):
    db.conectar()
    sql = "INSERT INTO motivo_assistir (id_serie, motivo) VALUES (%s, %s)"
    db.executar(sql,(motivo.id_serie, motivo.motivo,))
    db.desconectar()
    return {"mensagem": "Motivo cadastrado com sucesso"}

@app.post('/avaliacoes/')
def avaliar_serie(avaliacao: Avaliacao):
    db.conectar()
    sql = "INSERT INTO avaliacao_serie (id_serie, nota, comentario) VALUES (%s, %s, %s)"
    db.executar(sql,(avaliacao.id_serie, avaliacao.nota, avaliacao.comentario,))
    db.desconectar()
    return {"mensagem": "Avaliação registrada com sucesso"}

@app.post('/atores/{id_ator}/series/{id_serie}/')
def associar_ator_serie(id_ator: int, id_serie: int, personagem: str):
    db.conectar()
    sql = "INSERT INTO ator_serie (id_ator, id_serie, personagem) VALUES (%s, %s, %s)"
    db.executar(sql, (id_ator, id_serie, personagem,))
    db.desconectar()
    return {"mensagem": "Ator associado à série com sucesso"}

@app.get('/series/')
def listar_series():
    db.conectar()
    sql = "SELECT * FROM serie"
    lista = db.executar(sql)
    db.desconectar()
    return lista

@app.get('/atores/')
def listar_atores():
    db.conectar()
    sql = "SELECT * FROM ator"
    lista = db.executar(sql)
    db.desconectar()
    return lista

@app.get('/categorias/')
def listar_categorias():
    db.conectar()
    sql = "SELECT * FROM categoria"
    lista = db.executar(sql)
    db.desconectar()
    return lista

@app.get('/avaliacoes/')
def listar_avaliacoes():
    db.conectar()
    sql = "SELECT * FROM avaliacao_serie"
    lista = db.executar(sql)
    db.desconectar()
    return lista

@app.put('/series/{id_serie}')
def atualizar_serie(id_serie: int, serie: Serie):
    db.conectar()
    sql = "UPDATE serie SET titulo = %s, descricao = %s, ano_lancamento = %s, id_categoria = %s WHERE id_serie = %s"
    db.executar(sql, (serie.titulo, serie.descricao, serie.ano_lancamento, serie.id_categoria, id_serie))
    db.desconectar
    return {"mensagem": "Série atualizada com sucesso"}

@app.put('/atores/{id_ator}')
def atualizar_ator(id_ator: int, ator: Ator):
    db.conectar()
    sql = "UPDATE ator SET nome = %s WHERE id_ator = %s"
    db.executar(sql, (ator.nome, id_ator))
    db.desconectar
    return {"mensagem": "Ator atualizado com sucesso"}

@app.put('/categorias/{id_categoria}')
def atualizar_categoria(id_categoria: int, categoria: Categoria):
    db.conectar()
    sql = "UPDATE categoria SET nome = %s WHERE id_categoria = %s"
    db.executar(sql, (categoria.nome, id_categoria))
    db.desconectar
    return {"mensagem": "Categoria atualizada com sucesso"}

@app.put('/motivos/{id_motivo}')
def atualizar_motivo(id_motivo_assistir: int, motivo: Motivo):
    db.conectar()
    sql = "UPDATE motivo_assistir SET nome = %s WHERE id_motivo_assistir = %s"
    db.executar(sql, (motivo.motivo, id_motivo_assistir))
    db.desconectar
    return {"mensagem": "Motivo atualizado com sucesso"}

@app.put('/avaliacoes/{id_avaliacao}')
def atualizar_avaliacao(id_avaliacao: int, avaliacao: Avaliacao):
    db.conectar()
    sql = "UPDATE avaliacao_serie SET id_serie = %s, nota = %s, comentario = %s WHERE id_motivo_assistir = %s"
    db.executar(sql, (avaliacao.id_serie, avaliacao.nota, avaliacao.comentario, id_avaliacao))
    db.desconectar
    return {"mensagem": "Avaliação atualizada com sucesso"}

@app.delete('/deletar/{id_ator}/')
def deletar_atores(id_ator: int):
    db.conectar()
    sql = "DELETE FROM ator WHERE id_ator = %s"
    db.executar(sql,(id_ator,))
    db.desconectar()
    return {"mensagem": "Ator deletado"}

@app.delete('/deletar/{id_serie}/')
def deletar_series(id_serie: int):
    db.conectar()
    sql = "DELETE FROM serie WHERE id_serie = %s"
    db.executar(sql,(id_serie,))
    db.desconectar()
    return {"mensagem": "Série deletada"}