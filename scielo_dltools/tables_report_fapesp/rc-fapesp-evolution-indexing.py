# coding: utf-8

import argparse
import csv
import numpy as np
import os
import pandas as pd
import scielo_scholarly_data.standardizer as standardizer
import tempfile

from scielo_dltools.libs import gstorage

def main():
    parser = argparse.ArgumentParser(description = 'Produces the data object Evolution of SciELO Brazil indexing for the FAPESP report.')

    parser.add_argument('-d1', '--file_1_to_download',
        dest = 'path_file_1_to_download', required = True,
        help = 'Path of the Data Lake to download metadata file. e.g: "scielo-datalake-raw/index/scielo/documents_licenses.csv"')

    parser.add_argument('-d2', '--file_2_to_download',
        dest = 'path_file_2_to_download', required = True,
        help = 'Path of the Data Lake to download the file with collection entry and exit dates. e.g: "scielo-datalake-raw/index/scielo/scielo-year-of-entry-exit-bra.csv"')

    parser.add_argument('-u', '--file_to_upload', dest = 'path_file_to_upload',
        required = True, help = 'Path file to upload results to Data Lake.')

    arguments = parser.parse_args()

    BUCKET_1_DOWNLOAD = arguments.path_file_1_to_download.split('/')[0]
    SOURCE_FILE_1_DOWNLOAD = '/'.join(arguments.path_file_1_to_download.split('/')[1:])
    BUCKET_2_DOWNLOAD = arguments.path_file_2_to_download.split('/')[0]
    SOURCE_FILE_2_DOWNLOAD = '/'.join(arguments.path_file_2_to_download.split('/')[1:])
    BUCKET_NAME_UPLOAD = arguments.path_file_to_upload.split('/')[0]
    DESTINATION_FILE_UPLOAD = '/'.join(arguments.path_file_to_upload.split('/')[1:])

    temp, path_1 = tempfile.mkstemp()
    gstorage.download_file(
    BUCKET_1_DOWNLOAD,
    SOURCE_FILE_1_DOWNLOAD,
    path_1
    )

    temp, path_2 = tempfile.mkstemp()
    gstorage.download_file(
    BUCKET_2_DOWNLOAD,
    SOURCE_FILE_2_DOWNLOAD,
    path_2
    )

    # Carga do CSV com os metadados de documentos
    df = pd.read_csv(path_1, low_memory=False, keep_default_na=False)

    # Filtra documento a parti de 1997
    ndf = df[df['document publishing year'] >= 1997]

    # Agrupa por ISSN e documento
    gb_docs_issn = ndf.groupby(['ISSN SciELO','document publishing year']).count()\
    .unstack(fill_value=0).stack()['document publishing ID (PID SciELO)']

    # Converte o objeto tipo Series (do groupby) em DataFrame
    docs_issn = pd.DataFrame(gb_docs_issn.to_frame().to_records())

    # Renomeia colunas para facilitar o uso posteriormente
    docs_issn.rename(columns={'ISSN SciELO': 'issn_scielo',
                              'document publishing year':'publication_year',
                              'document publishing ID (PID SciELO)':'docs_count'},
                              inplace=True)

    # Carga do CSV com os anos de entrada e saída dos periódicos
    dfio = pd.read_csv(path_2)

    # Garante tipagem Int para exit_year e troca NaN por Zero
    dfio['exit_year'] = pd.to_numeric(dfio['exit_year'], errors='coerce')
    dfio['exit_year'] = dfio['exit_year'].fillna(0).astype(int)

    # Concatena DataFrames
    # Agrega a docs_issn os anos de entrada e saída do periódico criando assim um novo DF
    cdf = pd.concat([pd.merge(docs_issn, dfio, how='inner', on='issn_scielo')])

    # Aplica a regra para Ativo ou Nao-Ativo
    '''
    SE (ano_entrada <= ano_publicacao AND (data_saida == None OR data_saida >= ano_publicacao) AND num_docs > 0):
    esta ativo no ano (1)
    SENÃO
    não está ativo no ano (0)
    '''
    cdf["active"] = np.where(
        	(cdf['year_of_entry'] <= cdf['publication_year']) &
        	((cdf['exit_year'] == 0) | (pd.to_numeric(cdf['exit_year']) >= cdf['publication_year'])) &
        	(cdf['docs_count'] > 0), 1, 0)

    # Tabula Ativos
    # Filtra periódicos ativos e ano de publicação até o ano corrente.
    # Agrupa por ano de publicação e renomeia a coluna "issn_scielo" para "ativos".
    ativos = pd.DataFrame(cdf[(cdf["active"] == 1)].groupby('publication_year').count()['issn_scielo'])
    ativos.rename(columns={'issn_scielo':'ativos'}, inplace=True)

    # Tabula Indexados
    # Agrupa por ano de entrada
    indexados = pd.DataFrame(dfio.groupby(['year_of_entry']).count()['issn_scielo'])

    # Cria coluna "indexados" com o acumulado a cada ano.
    indexados['indexados'] = indexados.issn_scielo.cumsum()

    # Renomeia o index "year_of_entry" para "publication_year" para uso posterior;
    indexados.index.name='publication_year'

    # Remove a coluna "issn_scielo"
    del indexados['issn_scielo']

    # Concatena Ativos e Indexados
    # Concatena pela ativos e indexados pela chave publication_year
    tab = pd.concat([pd.merge(ativos, indexados, how='inner', on='publication_year')])

    # Desindexados
    # Desindexados é subtração de indexados de ativos
    tab['desindexados'] = tab['indexados']-tab['ativos']

    # Renomeia o index "publication_year" para "ano_publicacao"
    tab.index.name='ano_publicacao'

    # Exporta resultados para CSV e faz upload para DataLake
    tab.to_csv(path_1)
    gstorage.upload_file(
    BUCKET_NAME_UPLOAD,
    path_1,
    DESTINATION_FILE_UPLOAD
    )

    # Remocao de temporarios
    os.remove(path_1)
    os.remove(path_2)

if __name__ == '__main__':
    main()
