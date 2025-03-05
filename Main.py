import sqlite3

# Conecta (ou cria) o banco de dados chamado 'tarefas.db'
conn = sqlite3.connect("db/tarefas.db")

def cria_tabela():
    """Cria a tabela de produtos se ela não existir."""
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tarefas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            objetivo TEXT,
            data_criacao TEXT DEFAULT (datetime('now', 'localtime')),
            prazo TEXT CHECK(prazo GLOB '[0-3][0-9]/[0-1][0-9]/[0-9][0-9][0-9][0-9]'),
            status TEXT NOT NULL CHECK(status IN ('pendente','iniciado', 'concluída'))
        )
    """)
    conn.commit()

def add_tarefa():
    """Adiciona uma nova tarefa a lista."""
    nome = input("Nome da Tarefa: ")
    objetivo = input("Objetivo da Tarefa: ")
    prazo = input("Prazo da Tarefa: ")
    status = input("Status da Tarefa: ")

    conn.execute("INSERT INTO tarefas (nome, objetivo, prazo, status) VALUES (?, ?, ?, ?)",
                 (nome, objetivo, prazo, status))
    conn.commit()
    print("Produto adicionado com sucesso.\n")

def Lista_Tarefas():
    """Lista todos os produtos do estoque."""
    cursor = conn.execute("SELECT * FROM tarefas")
    tarefas = cursor.fetchall()
    
    if not tarefas:
        print("Nenhuma tarefa cadastrado.\n")
        return

    print("\n--- Tarefas ---")
    for tarefa in tarefas:
        print(f"ID: {tarefa[0]}")
        print(f"Nome: {tarefa[1]}")
        print(f"Objetivo: {tarefa[2]}")
        print(f"Prazo: {tarefa[3]}")
        print(f"Status: {tarefa[4]}")
        print("---------------")

def atualiza_tarefa():
    """Atualiza os objetivos, prazos e status de uma tarefa."""
    try:
        id_tarefa = int(input("Informe o ID da tarefa para atualizar: "))

    except ValueError:
        print("Valor inválido para ID.")
        return
    
    novo_objetivo = input("Novo objetivo: ")
    novo_prazo =  input("Novo prazo: ")
    novo_status = input("Novo status: ")

    conn.execute("UPDATE tarefas SET objetivo = ?, prazo = ?, status = ? WHERE id = ?",
                 (novo_objetivo, novo_prazo, novo_status, id_tarefa))
    conn.commit()
    print("Produto atualizado com sucesso.\n")

def deleta_tarefa():
    """Deleta uma tarefa da lista com base no ID informado."""
    try:
        id_tarefa = int(input("Informe o ID da tarefa para deletar: "))
    except ValueError:
        print("ID inválido.")
        return

    conn.execute("DELETE FROM tarefas WHERE id = ?", (id_tarefa,))
    conn.commit()
    print("Tarefa deletada com sucesso.\n")

def menu():
    """Exibe o menu e retorna a opção escolhida pelo usuário."""
    print("==== Lista de Tarefas ====")
    print("1. Adicionar Tarefa")
    print("2. Listar Tarefas")
    print("3. Atualizar Tarefa")
    print("4. Deletar Tarefa")
    print("5. Sair")
    return input("Escolha uma opção: ")

def main():
    # Cria a tabela de produtos
    cria_tabela()
    while True:
        option = menu()
        if option == "1":
            add_tarefa()
        elif option == "2":
            Lista_Tarefas()
        elif option == "3":
            atualiza_tarefa()
        elif option == "4":
            deleta_tarefa()
        elif option == "5":
            print("Encerrando o programa...")
            break
        else:
            print("Opção inválida. Tente novamente.\n")

    # Fecha a conexão com o banco de dados
    conn.close()

if __name__ == "__main__":
    main()
