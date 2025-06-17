import pdfplumber
import pandas as pd
import re

caminho_pdf = r"dados_brutos/relatorio_cliente.pdf"

def extrair_texto_pdf(caminho_pdf):
    texto = ""
    with pdfplumber.open(caminho_pdf) as pdf:
        for pagina in pdf.pages:
            conteudo = pagina.extract_text()
            if conteudo:
                texto += conteudo + "\n"
    return texto

def tratar_dados(texto):
    linhas = texto.split('\n')
    dados = []

    for linha in linhas:
        if re.match(r'^\s*(Codigo|--|DROGARIAS|Relatorio)', linha):
            continue

        match = re.match(r'(\d{5})\s+(.{1,30})\s+(.{20,50})\s+(.*?RJ|AC)\s+(\d{8,})', linha)
        if match:
            codigo = match.group(1).strip()
            nome = match.group(2).strip()
            endereco = match.group(3).strip()
            cidade_uf = match.group(4).strip()
            telefone = match.group(5).strip()

            endereco_limpo = re.sub(r'N\.?\s?\d+.*', '', endereco)
            endereco_limpo = re.sub(r'\d+.*', '', endereco_limpo)

            dados.append([codigo, nome, endereco_limpo.strip(), cidade_uf, 'REMOVIDO'])

    df = pd.DataFrame(dados, columns=['Codigo', 'Nome', 'Endereco', 'Cidade_UF', 'Telefone'])
    return df

texto = extrair_texto_pdf(caminho_pdf)
df_limpo = tratar_dados(texto)

df_limpo.to_excel(r"dados_tratados/clientes_tratados.xlsx", index=False)
print("✅")
