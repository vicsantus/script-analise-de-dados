import csv
from datetime import datetime

# Optei por fazer o path dessa forma
# por questão de deixar extencivel
year = '2022'

path_exp = f"EXP_{year}.csv"
path_imp = f"IMP_{year}.csv"
path_rst = "./resultados"


def process(path_exp, path_imp, path_rst):
    with open(path_exp, 'r') as fileEXP, open(path_imp, 'r') as fileIMP:
        # O delimiter dos arquivos littlesample são virgulas
        leitor_csv_exp = csv.reader(fileEXP, delimiter=";", quotechar='"')
        # O delimiter dos arquivos normais do gov são ponto e vírgula
        leitor_csv_imp = csv.reader(fileIMP, delimiter=";", quotechar='"')
        cabecalho_exp = next(leitor_csv_exp)
        cabecalho_imp = next(leitor_csv_imp)
        result_exp = ler_lista(cabecalho_exp, leitor_csv_exp)
        result_imp = ler_lista(cabecalho_imp, leitor_csv_imp)

    criar_csv_estados(result_exp, result_imp, path_rst)


def criar_csv_estados(dados_exp, dados_imp, path):
    meses_ordenados = [str(i) for i in range(1, 13)]

    # Complexidade dessa função ficou O(n * m)
    # mas está gerando resultados bem rápido
    # pois está sendo usado dicionarios
    for estado, valor1 in dados_exp.items():
        valor2 = dados_imp.get(estado, {})

        # Rota para onde se deve enviar os resultados
        nome_arquivo = f"{path}/{estado}.csv"

        with open(nome_arquivo, 'w', newline='') as arquivo_csv:
            escritor_csv = csv.writer(arquivo_csv)

            # Cria o cabeçalho com exp-mes imp-mes e net-mes
            cabecalho = ['NCM']
            for ncm in meses_ordenados:
                mes_nome = datetime.strptime(ncm, '%m').strftime('%B')
                cabecalho.append(f"exp-{mes_nome[:3]}")
                cabecalho.append(f"imp-{mes_nome[:3]}")
                cabecalho.append(f"net-{mes_nome[:3]}")
            cabecalho.append(f"Exp-{year}")
            cabecalho.append(f"Imp-{year}")
            cabecalho.append(f"Net-{year}")
            escritor_csv.writerow(cabecalho)

            indices = set(valor1.keys()) | set(valor2.keys())

            for idx in indices:
                valores_meses = []
                soma_exp = 0
                soma_imp = 0
                for mes in meses_ordenados:
                    valor_mes_exp = valor1.get(idx, {}).get(mes, 0)
                    valor_mes_imp = valor2.get(idx, {}).get(mes, 0)
                    valor_net = int(valor_mes_exp) + int(valor_mes_imp)
                    valores_meses.extend(
                        [int(valor_mes_exp), int(valor_mes_imp), valor_net])
                    soma_exp += int(valor_mes_exp)
                    soma_imp += int(valor_mes_imp)
                valores_meses.extend([soma_exp, soma_imp, soma_exp + soma_imp])
                escritor_csv.writerow([idx] + valores_meses)

# Essa função ficou lenta com 1 milhao de dados
# apesar da complexidade ser O(n)


def ler_lista(cabecalho, leitor_csv):
    indice_ncm = cabecalho.index('CO_NCM')
    indice_mes = cabecalho.index('CO_MES')
    indice_uf = cabecalho.index('SG_UF_NCM')
    indice_fob = cabecalho.index('VL_FOB')
    resultado = {}

    # Nessa função optei por retornar um dict por ser
    # mais facil de manipular e pela complexidade baixar bastante
    for linha in leitor_csv:
        ncm = linha[indice_ncm]
        mes = linha[indice_mes]
        uf = linha[indice_uf]
        vl_fob = float(linha[indice_fob])

        # Caso esse if não exista, os meses de janeiro a setembro,
        # ficam com um 0 na frente pois são strings
        # Sem esse if na função criar_csv_estados
        # só contabiliza do mes 10 para frente
        if int(mes) < 10:
            mes = str(int(mes))

        chave = uf
        if chave not in resultado:
            resultado[chave] = {ncm: {mes: float(vl_fob)}}
        else:
            if ncm not in resultado[uf]:
                resultado[uf][ncm] = {mes: vl_fob}
            else:
                if mes in resultado[uf][ncm]:
                    resultado[uf][ncm][mes] += vl_fob
                else:
                    resultado[uf][ncm][mes] = vl_fob

    return resultado


if __name__ == "__main__":
    process(path_exp, path_imp, path_rst)
