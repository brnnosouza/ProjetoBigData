# BigData

Este repositório contém scripts Python desenvolvidos para extrair, tratar e organizar dados provenientes de:
- Arquivos XML de Notas Fiscais Eletrônicas (NF-e)
- Relatórios em PDF com dados de clientes

Os dados tratados são salvos em arquivos Excel e utilizados para análise no Power BI.

---

## 🛠 Tecnologias Utilizadas

| Tecnologia | Finalidade |
|------------|------------|
| **Python** | Linguagem principal usada para automação e tratamento dos dados |
| **pandas** | Manipulação de dados, criação de DataFrames e exportação para Excel |
| **regex (re)** | Limpeza e extração de padrões em textos complexos (endereços, nomes etc.) |
| **pdfplumber** | Leitura e extração de texto estruturado a partir de arquivos PDF |
| **xml.etree.ElementTree** | Leitura e parsing dos arquivos XML de nota fiscal |
| **datetime** | Conversão e tratamento de datas das notas fiscais |
| **openpyxl** | Biblioteca auxiliar usada implicitamente pelo `pandas.to_excel()` |

---

## 📊 Power BI

O arquivo `DashBoard.pbix` traz visualizações com base nos dados tratados, como:
- Produtos vendidos por nota
- Formas de pagamento
- Distribuição por clientes ou localidades


---
