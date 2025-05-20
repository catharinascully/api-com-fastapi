from fastapi import FastAPI, HTTPException
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

# MÉTODO PARA ATUALIZAR
@app.put("/ator/{id_ator}")
def atualizar_ator(id_ator: int, ator: Ator):
    db.conectar()
 
    ator_existente = db.executar("SELECT * FROM ator WHERE id_ator = %s", (id_ator,))
    if not ator_existente:
        db.desconectar()
        raise HTTPException(status_code=404, detail="Ator não encontrado")
 
    sql = "UPDATE ator SET nome = %s WHERE id_ator = %s"
    db.executar(sql, (ator.nome, id_ator))
    db.desconectar()
    return {"mensagem": "Ator atualizado com sucesso", "ator_atualizado": ator}
 
@app.put("/categoria/{id_categoria}")
def atualizar_categoria(id_categoria: int, categoria: Categoria):
    db.conectar()
 
    categoria_existente = db.executar("SELECT * FROM categoria WHERE id_categoria = %s", (id_categoria,))
    if not categoria_existente:
        db.desconectar()
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
 
    sql = "UPDATE categoria SET nome = %s WHERE id_categoria = %s"
    db.executar(sql, (categoria.nome, id_categoria))
    db.desconectar()
    return {"mensagem": "Categoria atualizada com sucesso", "categoria_atualizada": categoria}
 
@app.put("/motivo/{id_motivo}")
def atualizar_motivo(id_motivo: int, motivo: Motivo):
    db.conectar()
 
    motivo_existente = db.executar("SELECT * FROM motivo_assistir WHERE id_motivo = %s", (id_motivo,))
    if not motivo_existente:
        db.desconectar()
        raise HTTPException(status_code=404, detail="Motivo não encontrado")
 
    sql = "UPDATE motivo_assistir SET id_serie = %s, motivo = %s WHERE id_motivo = %s"
    db.executar(sql, (motivo.id_serie, motivo.motivo, id_motivo))
    db.desconectar()
    return {"mensagem": "Motivo atualizado com sucesso", "motivo_atualizado": motivo}
 
@app.put("/avaliacao/{id_avaliacao}")
def atualizar_avaliacao(id_avaliacao: int, avaliacao: Avaliacao):
    db.conectar()
 
    avaliacao_existente = db.executar("SELECT * FROM avaliacao_serie WHERE id_avaliacao = %s", (id_avaliacao,))
    if not avaliacao_existente:
        db.desconectar()
        raise HTTPException(status_code=404, detail="Avaliação não encontrada")
 
    sql = "UPDATE avaliacao_serie SET id_serie = %s, nota = %s, comentario = %s WHERE id_avaliacao = %s"
    db.executar(sql, (avaliacao.id_serie, avaliacao.nota, avaliacao.comentario, id_avaliacao))
    db.desconectar()
    return {"mensagem": "Avaliação atualizada com sucesso", "avaliacao_atualizada": avaliacao}
 
@app.put("/series/{id_serie}")
def atualizar_serie(id_serie: int, serie: Serie):
    db.conectar()
 
    # Verificar se a série existe
    sql_verifica = "SELECT * FROM serie WHERE id_serie = %s"
    resultado = db.executar(sql_verifica, (id_serie,))
    if not resultado:
        db.desconectar()
        raise HTTPException(status_code=404, detail="Série não encontrada")
   
    sql = "UPDATE serie SET titulo = %s, descricao = %s, ano_lancamento = %s, id_categoria = %s WHERE id_serie = %s"
    db.executar(sql, (serie.titulo, serie.descricao, serie.ano_lancamento, serie.id_categoria, id_serie))
    db.desconectar()
    return {"mensagem": "Série atualizada com sucesso", "serie_atualizada": serie}

#MÉTODO PARA DELETAR
 
@app.delete('/deletar/{id_serie}/')
def deletar_series(id_serie: int):
    db.conectar()
 
    serie_existente = db.executar("SELECT * FROM serie WHERE id_serie = %s", (id_serie,))
    if not serie_existente:
        db.desconectar()
        raise HTTPException(status_code=404, detail="Série não encontrada")
 
   
    # Deletar dependências primeiro
    db.executar("DELETE FROM ator_serie WHERE id_serie = %s", (id_serie,))
    db.executar("DELETE FROM avaliacao_serie WHERE id_serie = %s", (id_serie,))
    db.executar("DELETE FROM motivo_assistir WHERE id_serie = %s", (id_serie,))
   
    # Agora deletar a série
    db.executar("DELETE FROM serie WHERE id_serie = %s", (id_serie,))
   
    db.desconectar()
    return {"mensagem": "Série e dados relacionados deletados com sucesso"}
 
@app.delete("/ator/{id_ator}")
def deletar_ator(id_ator: int):
    db.conectar()
   
    ator_existente = db.executar("SELECT * FROM ator WHERE id_ator = %s", (id_ator,))
    if not ator_existente:
        db.desconectar()
        raise HTTPException(status_code=404, detail="Ator não encontrado")
   
    # Deletar os vínculos com séries primeiro
    sql_delete_vinculo = "DELETE FROM ator_serie WHERE id_ator = %s"
    db.executar(sql_delete_vinculo, (id_ator,))
   
    # Agora deletar o ator
    sql_delete_ator = "DELETE FROM ator WHERE id_ator = %s"
    db.executar(sql_delete_ator, (id_ator,))
   
    db.desconectar()
    return {"mensagem": "Ator e vínculos deletados com sucesso"}
 
@app.delete("/categoria/{id_categoria}")
def deletar_categoria(id_categoria: int):
    db.conectar()
   
    categoria_existente = db.executar("SELECT * FROM categoria WHERE id_categoria = %s", (id_categoria,))
    if not categoria_existente:
        db.desconectar()
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
 
    # Deletar dados relacionados às séries dessa categoria
    sql_busca_series = "SELECT id_serie FROM serie WHERE id_categoria = %s"
    series = db.executar(sql_busca_series, (id_categoria,))
   
    for serie in series:
        id_serie = serie['id_serie']
        db.executar("DELETE FROM ator_serie WHERE id_serie = %s", (id_serie,))
        db.executar("DELETE FROM avaliacao_serie WHERE id_serie = %s", (id_serie,))
        db.executar("DELETE FROM motivo_assistir WHERE id_serie = %s", (id_serie,))
        db.executar("DELETE FROM serie WHERE id_serie = %s", (id_serie,))
   
    # Agora deletar a categoria
    db.executar("DELETE FROM categoria WHERE id_categoria = %s", (id_categoria,))
   
    db.desconectar()
    return {"mensagem": "Categoria e séries relacionadas deletadas com sucesso"}
 
@app.delete("/motivo/{id_motivo}")
def deletar_motivo(id_motivo: int):
    db.conectar()
 
    motivo_existente = db.executar("SELECT * FROM motivo_assistir WHERE id_motivo = %s", (id_motivo,))
    if not motivo_existente:
        db.desconectar()
        raise HTTPException(status_code=404, detail="Motivo não encontrado")
   
    db.executar("DELETE FROM motivo_assistir WHERE id_motivo = %s", (id_motivo,))
    db.desconectar()
    return {"mensagem": "Motivo deletado com sucesso"}
 
@app.delete("/avaliacao/{id_avaliacao}")
def deletar_avaliacao(id_avaliacao: int):
    db.conectar()
 
    avaliacao_existente = db.executar("SELECT * FROM avaliacao_serie WHERE id_avaliacao = %s", (id_avaliacao,))
    if not avaliacao_existente:
        db.desconectar()
        raise HTTPException(status_code=404, detail="Avaliação não encontrada")
   
    sql = "DELETE FROM avaliacao_serie WHERE id_avaliacao = %s"
    db.executar(sql, (id_avaliacao,))
    db.desconectar()
    return {"mensagem": "Avaliação deletada com sucesso"}