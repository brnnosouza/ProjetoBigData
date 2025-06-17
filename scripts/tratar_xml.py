import os
import re
import pandas as pd
import xml.etree.ElementTree as ET
from datetime import datetime

pasta_xml = r'dados_brutos/xml_notas'
notas_data = []

formas_pagamento = {
    "01": "DINHEIRO", "02": "CHEQUE", "03": "CARTÃO DE CRÉDITO", "04": "CARTÃO DE DÉBITO",
    "05": "CRÉDITO LOJA", "10": "VALE ALIMENTAÇÃO", "11": "VALE REFEIÇÃO", "12": "VALE PRESENTE",
    "13": "VALE COMBUSTÍVEL", "15": "BOLETO BANCÁRIO", "16": "DEPÓSITO BANCÁRIO", "17": "PIX",
    "18": "TRANSFERÊNCIA BANCÁRIA", "19": "FIDELIDADE", "90": "SEM PAGAMENTO", "99": "OUTROS"
}

def remove_namespace(xml_string):
    xml_string = re.sub(r'\sxmlns(:\w+)?="[^"]+"', '', xml_string)
    xml_string = re.sub(r'<(/?)(\w+):', r'<\1', xml_string)
    return xml_string

for arquivo in os.listdir(pasta_xml):
    if arquivo.endswith('.xml'):
        caminho = os.path.join(pasta_xml, arquivo)
        with open(caminho, 'r', encoding='utf-8') as f:
            xml = f.read()

        root = ET.fromstring(remove_namespace(xml))

        emitente = root.findtext('.//emit/xNome')
        cnpj = root.findtext('.//emit/CNPJ')
        data_emissao_raw = root.findtext('.//ide/dhEmi')
        numero_nf = root.findtext('.//ide/nNF')
        valor_nota = root.findtext('.//pag/detPag/vPag')
        tpag = root.findtext('.//pag/detPag/tPag')
        forma_pagamento = formas_pagamento.get(tpag, 'DESCONHECIDO')

        try:
            data_formatada = datetime.fromisoformat(data_emissao_raw.replace('Z', '')).date()
        except:
            data_formatada = data_emissao_raw

        for det in root.findall('.//det'):
            notas_data.append({
                'arquivo': arquivo,
                'emitente': emitente,
                'data_formatada': data_formatada,
                'forma_pagamento': forma_pagamento,
                'codigo_produto': det.findtext('prod/cProd'),
                'descricao': det.findtext('prod/xProd'),
                'quantidade': det.findtext('prod/qCom'),
                'valor_unitario': det.findtext('prod/vUnCom'),
                'valor_total': det.findtext('prod/vProd'),
            })

df = pd.DataFrame(notas_data)
for col in ['quantidade', 'valor_unitario', 'valor_total']:
    df[col] = pd.to_numeric(df[col], errors='coerce')

df.to_excel(r'dados_tratados/nfe/tratamento_nfe.xlsx', index=False)
print("✅")
