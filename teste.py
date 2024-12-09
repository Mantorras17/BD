#importar dependências
import sqlite3
import pandas as pd

#ler as diferentes tabelas de excel (em formato .xlsx)
df = pd.read_excel("nome_do_ficheiro.xlsx",header=0, engine="openpyxl")

#conectar à base de dados (se ainda não existir é automaticamente criado)
connection = sqlite3.connect("nome_da_base_de_dados.db")

#cria uma tabela chamada "nome_da_tabela" criando as mesmas colunas que estão no excel e preenchendo conforme está no excel
df.to_sql("nome_da_tabela",connection,if_exists="replace")

#PKs e FKs foram depois escolhidas dentro do SQLiteStudio