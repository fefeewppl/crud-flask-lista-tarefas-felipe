from flask import Flask, render_template, request, redirect
import psycopg2

app = Flask(__name__)

def ligar_banco():
    banco = psycopg2.connect(
        host="localhost",
        dbname="ListaTarefas",
        user="postgres",
        password="senai",
        port="5432"
    )
    return banco

@app.route("/exibir_tarefas")
def tarefas():
    banco = ligar_banco()
    cursor = banco.cursor()
    cursor.execute("SELECT id, titulo, descricao FROM  tarefa ORDER BY id")
    lista = cursor.fetchall()
    banco.close()
    return render_template("tarefas.html", tarefas=lista)

@app.route("/tarefas/enviar", methods=["POST"])
def enviar_tarefa():
    titulo = request.form.get("titulo")
    descricao = request.form.get("descricao")

    banco = ligar_banco()
    cursor = banco.cursor()
    cursor.execute("""INSERT INTO tarefa (titulo, descricao)
            VALUES (%s, %s)""", (titulo, descricao))
    banco.commit()
    banco.close()
    return redirect("/")

@app.route("/tarefas/editar/<int:id>")
def editar_tarefa(id):
    banco = ligar_banco()
    cursor = banco.cursor()
    cursor.execute("SELECT id, titulo, descricao FROM tarefa WHERE id = %s", (id,))
    tarefa = cursor.fetchone()
    banco.close()

    if tarefa is None:
        return redirect("/")
    return render_template("editar_tarefa.html", tarefa=tarefa)

@app.route("/tarefas/atualizar/<int:id>", methods=["POST"])
def atualizar_tarefa(id):
    titulo = request.form.get("titulo")
    descricao = request.form.get("descricao")

    banco = ligar_banco()
    cursor = banco.cursor()
    cursor.execute("""UPDATE tarefa SET titulo = %s, descricao = %s
            WHERE id = %s""", (titulo, descricao, id))
    banco.commit()
    banco.close()
    return redirect("/")

@app.route("/tarefas/excluir/<int:id>", methods=["POST"])
def excluir_tarefa(id):
    banco = ligar_banco()
    cursor = banco.cursor()
    cursor.execute("DELETE FROM tarefa WHERE id = %s", (id,))
    banco.commit()
    banco.close()
    return redirect("/")


if __name__ == "__main__":
    app.run()
