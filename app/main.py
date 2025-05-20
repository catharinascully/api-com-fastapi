from fastapi import FastAPI, HTTPException
from model.database import Database
from model.models import Serie, Ator, Categoria, Motivo, Avaliacao

app = FastAPI()
db = Database()

 
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from data.database import Database
from model.models import Serie, Ator, Categoria, Motivo, Avaliacao
 
db = Database()
app = FastAPI()
 
series_db = [] #Lista que simula um banco de dados
 
@app.post('/serie/')
def cadastrar(serie: Serie):
    with Database() as db:
        sql = "INSERT INTO serie (titulo, descricao, ano_lancamento, id_categoria) VALUES (%s, %s, %s, %s)"
        db.executar(sql, (serie.titulo, serie.descricao, serie.ano_lancamento, serie.id_categoria))
    return {"mensagem": "Série cadastrada com sucesso", "serie": serie}
 
@app.post("/ator/")
def cadastrar_ator(ator: Ator):
    with Database() as db:
        sql = "INSERT INTO ator (nome) VALUES (%s)"
        db.executar(sql, (ator.nome,))
    return {"message": "Ator cadastrado com sucesso"}
 
@app.post("/categorias/")
def adicionar_categoria(categoria: Categoria):
    with Database() as db:
        sql = "INSERT INTO categoria (nome) VALUES (%s)"
        db.executar(sql, (categoria.nome,))
    return {"message": "Categoria adicionada com sucesso"}
 
@app.post("/atores/{id_ator}/series/{id_serie}")
def associar_ator_serie(id_ator: int, id_serie: int, personagem: str):
    with Database() as db:
        sql = "INSERT INTO ator_serie (id_ator, id_serie, personagem) VALUES (%s, %s, %s)"
        db.executar(sql, (id_ator, id_serie, personagem))
    return {"message": "Ator associado à série com sucesso"}
 
@app.post("/motivos/")
def incluir_motivo(motivo: Motivo):
    with Database() as db:
        sql = "INSERT INTO motivo_assistir (id_serie, motivo) VALUES (%s, %s)"
        db.executar(sql, (motivo.id_serie, motivo.motivo))
    return {"message": "Motivo incluído com sucesso"}
 
@app.post("/avaliacoes/")
def avaliar_serie(avaliacao: Avaliacao):
    with Database() as db:
        sql = "INSERT INTO avaliacao_serie (id_serie, nota, comentario) VALUES (%s, %s, %s)"
        db.executar(sql, (avaliacao.id_serie, avaliacao.nota, avaliacao.comentario))
    return {"message": "Avaliação registrada com sucesso"}
 
@app.get("/series/")
def listar_series():
    with Database() as db:
        sql = "SELECT * FROM serie"
        return db.executar(sql)
 
@app.get("/atores/")
def listar_atores():
    with Database() as db:
        sql = "SELECT * FROM ator"
        return db.executar(sql)
 
@app.get("/categorias/")
def listar_categorias():
    with Database() as db:
        sql = "SELECT * FROM categoria"
        return db.executar(sql)
 
@app.get("/avaliacoes/")
def listar_avaliacoes():
    with Database() as db:
        sql = "SELECT * FROM avaliacao_serie"
        return db.executar(sql)
 
@app.delete('/deletar/{id_serie}/')
def deletar_series(id_serie: int):
    with Database() as db:
        serie_existente = db.executar("SELECT * FROM serie WHERE id_serie = %s", (id_serie,))
        if not serie_existente:
            raise HTTPException(status_code=404, detail="Série não encontrada")
        db.executar("DELETE FROM ator_serie WHERE id_serie = %s", (id_serie,))
        db.executar("DELETE FROM avaliacao_serie WHERE id_serie = %s", (id_serie,))
        db.executar("DELETE FROM motivo_assistir WHERE id_serie = %s", (id_serie,))
        db.executar("DELETE FROM serie WHERE id_serie = %s", (id_serie,))
    return {"mensagem": "Série e dados relacionados deletados com sucesso"}
 
@app.delete("/ator/{id_ator}")
def deletar_ator(id_ator: int):
    with Database() as db:
        ator_existente = db.executar("SELECT * FROM ator WHERE id_ator = %s", (id_ator,))
        if not ator_existente:
            raise HTTPException(status_code=404, detail="Ator não encontrado")
        db.executar("DELETE FROM ator_serie WHERE id_ator = %s", (id_ator,))
        db.executar("DELETE FROM ator WHERE id_ator = %s", (id_ator,))
    return {"mensagem": "Ator e vínculos deletados com sucesso"}
 
@app.delete("/categoria/{id_categoria}")
def deletar_categoria(id_categoria: int):
    with Database() as db:
        categoria_existente = db.executar("SELECT * FROM categoria WHERE id_categoria = %s", (id_categoria,))
        if not categoria_existente:
            raise HTTPException(status_code=404, detail="Categoria não encontrada")
        series = db.executar("SELECT id_serie FROM serie WHERE id_categoria = %s", (id_categoria,))
        for serie in series:
            db.executar("DELETE FROM ator_serie WHERE id_serie = %s", (serie['id_serie'],))
            db.executar("DELETE FROM avaliacao_serie WHERE id_serie = %s", (serie['id_serie'],))
            db.executar("DELETE FROM motivo_assistir WHERE id_serie = %s", (serie['id_serie'],))
            db.executar("DELETE FROM serie WHERE id_serie = %s", (serie['id_serie'],))
        db.executar("DELETE FROM categoria WHERE id_categoria = %s", (id_categoria,))
    return {"mensagem": "Categoria e séries relacionadas deletadas com sucesso"}
 
@app.delete("/motivo/{id_motivo}")
def deletar_motivo(id_motivo: int):
    with Database() as db:
        motivo_existente = db.executar("SELECT * FROM motivo_assistir WHERE id_motivo = %s", (id_motivo,))
        if not motivo_existente:
            raise HTTPException(status_code=404, detail="Motivo não encontrado")
        db.executar("DELETE FROM motivo_assistir WHERE id_motivo = %s", (id_motivo,))
    return {"mensagem": "Motivo deletado com sucesso"}
 
@app.delete("/avaliacao/{id_avaliacao}")
def deletar_avaliacao(id_avaliacao: int):
    with Database() as db:
        avaliacao_existente = db.executar("SELECT * FROM avaliacao_serie WHERE id_avaliacao = %s", (id_avaliacao,))
        if not avaliacao_existente:
            raise HTTPException(status_code=404, detail="Avaliação não encontrada")
        db.executar("DELETE FROM avaliacao_serie WHERE id_avaliacao = %s", (id_avaliacao,))
    return {"mensagem": "Avaliação deletada com sucesso"}
 
@app.put("/ator/{id_ator}")
def atualizar_ator(id_ator: int, ator: Ator):
    with Database() as db:
        ator_existente = db.executar("SELECT * FROM ator WHERE id_ator = %s", (id_ator,))
        if not ator_existente:
            raise HTTPException(status_code=404, detail="Ator não encontrado")
        db.executar("UPDATE ator SET nome = %s WHERE id_ator = %s", (ator.nome, id_ator))
    return {"mensagem": "Ator atualizado com sucesso", "ator_atualizado": ator}
 
@app.put("/categoria/{id_categoria}")
def atualizar_categoria(id_categoria: int, categoria: Categoria):
    with Database() as db:
        categoria_existente = db.executar("SELECT * FROM categoria WHERE id_categoria = %s", (id_categoria,))
        if not categoria_existente:
            raise HTTPException(status_code=404, detail="Categoria não encontrada")
        db.executar("UPDATE categoria SET nome = %s WHERE id_categoria = %s", (categoria.nome, id_categoria))
    return {"mensagem": "Categoria atualizada com sucesso", "categoria_atualizada": categoria}
 
@app.put("/motivo/{id_motivo}")
def atualizar_motivo(id_motivo: int, motivo: Motivo):
    with Database() as db:
        motivo_existente = db.executar("SELECT * FROM motivo_assistir WHERE id_motivo = %s", (id_motivo,))
        if not motivo_existente:
            raise HTTPException(status_code=404, detail="Motivo não encontrado")
        db.executar("UPDATE motivo_assistir SET id_serie = %s, motivo = %s WHERE id_motivo = %s", (motivo.id_serie, motivo.motivo, id_motivo))
    return {"mensagem": "Motivo atualizado com sucesso", "motivo_atualizado": motivo}
 
@app.put("/avaliacao/{id_avaliacao}")
def atualizar_avaliacao(id_avaliacao: int, avaliacao: Avaliacao):
    with Database() as db:
        avaliacao_existente = db.executar("SELECT * FROM avaliacao_serie WHERE id_avaliacao = %s", (id_avaliacao,))
        if not avaliacao_existente:
            raise HTTPException(status_code=404, detail="Avaliação não encontrada")
        db.executar("UPDATE avaliacao_serie SET id_serie = %s, nota = %s, comentario = %s WHERE id_avaliacao = %s", (avaliacao.id_serie, avaliacao.nota, avaliacao.comentario, id_avaliacao))
    return {"mensagem": "Avaliação atualizada com sucesso", "avaliacao_atualizada": avaliacao}
 
@app.put("/series/{id_serie}")
def atualizar_serie(id_serie: int, serie: Serie):
    with Database() as db:
        resultado = db.executar("SELECT * FROM serie WHERE id_serie = %s", (id_serie,))
        if not resultado:
            raise HTTPException(status_code=404, detail="Série não encontrada")
        db.executar("UPDATE serie SET titulo = %s, descricao = %s, ano_lancamento = %s, id_categoria = %s WHERE id_serie = %s", (serie.titulo, serie.descricao, serie.ano_lancamento, serie.id_categoria, id_serie))
    return {"mensagem": "Série atualizada com sucesso", "serie_atualizada": serie}
 
 