
import pandas as pd

df = pd.read_csv('/home/andre/neuro/apps/tests/srs2/tabelas-normativas/idade_escolar_feminino.csv')

# Remove os limites de exibição
pd.set_option('display.max_rows', None)    # Mostra todas as linhas
pd.set_option('display.max_columns', None) # Mostra todas as colunas
pd.set_option('display.width', None)       # Ajusta a largura da tela

print(df)
