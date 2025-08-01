import json  # Módulo para salvar e carregar dados em formato JSON

# Lista global para armazenar os alunos
alunos = []

def input_float(prompt, min_val=None, max_val=None):
    """
    Função para entrada de número float com validação de intervalo.
    Se o valor for inválido, retorna None.
    """
    try:
        valor = float(input(prompt))
        if min_val is not None and valor < min_val:
            raise ValueError
        if max_val is not None and valor > max_val:
            raise ValueError
        return valor
    except ValueError:
        print(f"Valor inválido! Deve ser um número entre {min_val} e {max_val}.")
        return None

def cadastrar_aluno():
    """Função para cadastrar um novo aluno."""
    nome = input("Nome do aluno: ").strip()
    disciplina = input("Disciplina: ").strip()
    nota = input_float("Nota (0 a 10): ", 0, 10)  # Garante que a nota seja válida
    if nota is None:
        return  # Sai da função se a nota for inválida

    # Adiciona o aluno ao final da lista
    alunos.append({"nome": nome, "disciplina": disciplina, "nota": nota})
    print(f"Aluno {nome} cadastrado com sucesso.")

def listar_alunos():
    """Função para listar os alunos, permitindo escolher o critério e a ordem."""
    if not alunos:
        print("Nenhum aluno cadastrado.")
        return

    # Escolha do critério de ordenação
    criterio = input("Ordenar por (nome/nota/disciplina)? ").strip().lower()
    # Escolha se a ordem será decrescente
    reverse = input("Ordem decrescente? (s/n): ").strip().lower() == "s"

    if criterio not in {"nome", "nota", "disciplina"}:
        print("Critério inválido.")
        return

    # Ordena a lista de alunos conforme o critério e ordem escolhidos
    ordenado = sorted(alunos, key=lambda x: x[criterio], reverse=reverse)

    print("\nLista de alunos:")
    for a in ordenado:
        print(f"{a['nome']} | {a['disciplina']} | Nota: {a['nota']}")

def busca_linear_nome():
    """Busca linear por nome — não precisa ser igual, basta conter o termo."""
    termo = input("Nome para busca linear: ").strip().lower()
    encontrados = [a for a in alunos if termo in a["nome"].lower()]

    if encontrados:
        print("Alunos encontrados:")
        for a in encontrados:
            print(f"{a['nome']} | {a['disciplina']} | Nota: {a['nota']}")
    else:
        print("Nenhum aluno encontrado.")

def busca_binaria_nome():
    """Busca binária por nome exato — exige lista ordenada previamente."""
    if not alunos:
        print("Nenhum aluno cadastrado.")
        return

    termo = input("Nome para busca binária: ").strip().lower()
    # Ordena a lista por nome para garantir que a busca binária funcione
    ordenado = sorted(alunos, key=lambda x: x["nome"].lower())

    low, high = 0, len(ordenado) - 1
    resultados = []

    # Algoritmo clássico de busca binária
    while low <= high:
        mid = (low + high) // 2
        nome_mid = ordenado[mid]["nome"].lower()

        if termo == nome_mid:
            # Encontrou — agora verifica se há mais ocorrências próximas
            resultados.append(ordenado[mid])
            # Busca para a esquerda
            i = mid - 1
            while i >= 0 and ordenado[i]["nome"].lower() == termo:
                resultados.append(ordenado[i])
                i -= 1
            # Busca para a direita
            i = mid + 1
            while i < len(ordenado) and ordenado[i]["nome"].lower() == termo:
                resultados.append(ordenado[i])
                i += 1
            break  # Sai do loop principal após encontrar
        elif termo < nome_mid:
            high = mid - 1
        else:
            low = mid + 1

    if resultados:
        print("Alunos encontrados:")
        for a in resultados:
            print(f"{a['nome']} | {a['disciplina']} | Nota: {a['nota']}")
    else:
        print("Nenhum aluno encontrado.")

def busca_faixa_notas():
    """Busca por faixa de notas, mostrando todos os alunos dentro do intervalo."""
    minimo = input_float("Nota mínima: ")
    if minimo is None:
        return
    maximo = input_float("Nota máxima: ")
    if maximo is None:
        return

    # Filtra alunos dentro da faixa especificada
    encontrados = [a for a in alunos if minimo <= a["nota"] <= maximo]

    if encontrados:
        print(f"Alunos com nota entre {minimo} e {maximo}:")
        for a in encontrados:
            print(f"{a['nome']} | {a['disciplina']} | Nota: {a['nota']}")
    else:
        print("Nenhum aluno nessa faixa de nota.")

def excluir_aluno():
    """Exclui um aluno pelo nome — permite excluir se houver mais de um com mesmo nome."""
    if not alunos:
        print("Nenhum aluno cadastrado.")
        return

    nome_busca = input("Nome do aluno a excluir: ").strip().lower()
    # Procura alunos que contenham o nome
    encontrados = [(i, a) for i, a in enumerate(alunos) if nome_busca in a["nome"].lower()]

    if not encontrados:
        print("Nenhum aluno encontrado.")
        return

    print("\nAlunos encontrados:")
    for idx, (i, a) in enumerate(encontrados, start=1):
        print(f"[{idx}] {a['nome']} | {a['disciplina']} | Nota: {a['nota']}")

    try:
        escolha = int(input("Número do aluno para excluir (0 para cancelar): "))
        if escolha == 0:
            print("Operação cancelada.")
            return
        if 1 <= escolha <= len(encontrados):
            index_para_remover = encontrados[escolha - 1][0]
            aluno_removido = alunos.pop(index_para_remover)
            print(f"Aluno {aluno_removido['nome']} excluído com sucesso!")
        else:
            print("Número inválido.")
    except ValueError:
        print("Entrada inválida.")

def salvar_dados():
    """Salva a lista de alunos em um arquivo JSON."""
    with open("dados_alunos.json", "w") as f:
        json.dump(alunos, f)
    print("Dados salvos com sucesso.")

def carregar_dados():
    """Carrega os dados de alunos do arquivo JSON, se existir."""
    global alunos
    try:
        with open("dados_alunos.json", "r") as f:
            alunos = json.load(f)
        print("Dados carregados com sucesso.")
    except FileNotFoundError:
        alunos = []  # Se não houver arquivo, inicializa com lista vazia
    except json.JSONDecodeError:
        print("Erro ao carregar dados. Arquivo corrompido.")
        alunos = []

def menu():
    """Menu principal do programa, exibe as opções e executa conforme a escolha."""
    carregar_dados()  # Sempre tenta carregar dados ao iniciar

    # Mapeamento das opções com suas respectivas funções
    opcoes = {
        "1": cadastrar_aluno,
        "2": listar_alunos,
        "3": busca_linear_nome,
        "4": busca_binaria_nome,
        "5": busca_faixa_notas,
        "6": excluir_aluno,
        "7": salvar_dados
    }

    while True:
        print("\n=== Sistema de Notas ===")
        print("1 - Cadastrar aluno")
        print("2 - Listar alunos ordenados")
        print("3 - Buscar aluno por nome (linear)")
        print("4 - Buscar aluno por nome (binária)")
        print("5 - Buscar alunos por faixa de nota")
        print("6 - Excluir aluno")
        print("7 - Salvar e sair")

        op = input("Escolha: ")
        if op in opcoes:
            if op == "7":
                opcoes[op]()
                print("Até a próxima!")
                break
            else:
                opcoes[op]()  # Executa a função correspondente
        else:
            print("Opção inválida.")

# Executa o menu apenas se o script for rodado diretamente
if __name__ == "__main__":
    menu()
