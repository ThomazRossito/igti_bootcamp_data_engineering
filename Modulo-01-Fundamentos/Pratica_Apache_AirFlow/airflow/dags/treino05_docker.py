###############################################
## Autor: Thomaz Antonio Rossito Neto        ##
## Data: 24/11/2020                          ##
##                                           ##
## Software: Apache AirFlow                  ##
## Modalidade: Criação de DAG                ##
## Execução: Paralelismos - Dados Enade 2019 ##
## Obs1: Execução em Containers              ##
## Obs2: Contém mais task do que o treino04  ##
##                                           ##
## Curso: BootCamp Engenheiro de Dados       ##    
## Instituição: IGTI                         ##
## Link: http://igti.com.br/                 ## 
###############################################


from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator, BranchPythonOperator
from datetime import datetime, timedelta
import pandas as pd 
import zipfile

# Constantes 
data_path = '/usr/local/airflow/data/microdados_enade_2019/2019/3.DADOS/'
arquivo = data_path + 'microdados_enade_2019.txt'

# Argumentos default 
default_args = {
    'owner': 'Paralelismos Dados Enade 2019',                   # é o 'dono/proprietario' da DAG, informar um nome fácil para identificação
    'depends_on_past': False,                                   # se tem dependências com DAGs anteriores, deixar como False para manter a DAG como autônoma
    'start_date': datetime(2020, 11, 24, 23),                   # Data de início da DAG
    'email': ['email1@email1.com.br', 'email2@email2.com.br'],  # Email que irá receber informações sobre a DAG
    'email_on_failure': False,                                  # Se deseja ser notificado a cada falha que ocorrer na DAG
    'email_on_retry': False,                                    # Se der alguma falha, tentar fazer nova notificação 
    'retries': 1,                                               # Em caso de falha quantas tentativas serão notificadas
    'retry_delay': timedelta(minutes=1)                         # Em caso de falha qual o tempo de tentativa entre uma notificação e outra 
}

# Definindo - DAG (fluxo)
dag = DAG(
    "treino-05-docker",                                          # Nome da DAG
    description="Paralelismos",                           # Informação sobre a DAG
    default_args=default_args,                            # Argumentos definidos na lista acima
    schedule_interval=timedelta(minutes=5)                # Intervalo de cada execução 
)

# BashOperator - para marcar o início da execução
start_processing = BashOperator(
    task_id='start_processing',
    bash_command='echo "Start processing!" ',
    dag=dag
)

# Task para efetuar o download dos dados 
get_data = BashOperator(
    task_id='get-data',
    bash_command='curl http://download.inep.gov.br/microdados/Enade_Microdados/microdados_enade_2019.zip -o /usr/local/airflow/data/microdados_enade_2019.zip', 
    dag=dag
)

# função para extrair o arquivo
def unzip_file():
    with zipfile.ZipFile('/usr/local/airflow/data/microdados_enade_2019.zip', 'r') as zipped:
        zipped.extractall('/usr/local/airflow/data')

# PythonOperator para o - unzip_file        
unzip_file = PythonOperator(
    task_id='unzip_data',
    python_callable=unzip_file,
    dag=dag
)


# Função para executar um Filtro
def aplica_filtros():
    cols = ['CO_GRUPO','TP_SEXO','NU_IDADE','NT_GER','NT_FG','NT_CE','QE_I01','QE_I02','QE_I04','QE_I05','QE_I08']  # seleciona apenas algumas colunas do dataset
    enade = pd.read_csv(arquivo, sep=";", decimal=",", usecols=cols)             # carrega o dataset 
    enade = enade.loc[
        (enade.NU_IDADE > 20) &
        (enade.NU_IDADE < 40) &
        (enade.NT_GER > 0)
    ]                                                               # realiza o filtro 
    enade.to_csv(data_path + 'enade_filtro.csv', index=False)       # salva o arquivo em um diretório 

# PythonOperator para o - aplica_filtros        
task_aplica_filtro = PythonOperator(
    task_id='aplica_filtro',
    python_callable=aplica_filtros,
    dag=dag
)


### Cálculos com dependências ###
# Idade Centralizada na Média 
# Idade Centralizada ao Quadrado

# Idade Centralizada na Média 
def constroi_idade_centralizada():
    idade = pd.read_csv(data_path + 'enade_filtro.csv')                     # carrega o dataset 
    idade['idadecent'] = idade.NU_IDADE - idade.NU_IDADE.mean()            # Idade Centralizada
    idade[['idadecent']].to_csv(data_path + 'idadecent.csv', index=False)  # salva o arquivo em um diretório - idade[['idadecent']] => retorna um dataframe   

# Idade Centralizada ao Quadrado
def constroi_idade_cent_quad():
    idadecent = pd.read_csv(data_path + 'idadecent.csv')
    idadecent['idade2'] = idadecent.idadecent ** 2                               # faz o cálculo ao quadrado 
    idadecent[['idade2']].to_csv(data_path + 'idadequadrado.csv', index=False)


# PythonOperator para o - constroi_idade_centralizada        
task_idade_cent = PythonOperator(
    task_id='constroi_idade_centralizada',
    python_callable=constroi_idade_centralizada,
    dag=dag
)

# PythonOperator para o - constroi_idade_cent_quad        
task_idade_quad = PythonOperator(
    task_id='constroi_idade_ao_quadrado',
    python_callable=constroi_idade_cent_quad,
    dag=dag
)


# Função para realizar um replace e um filtro na coluna estado civil 
def constroi_est_civil():
    filtro = pd.read_csv(data_path + 'enade_filtro.csv')
    filtro['estcivil'] = filtro.QE_I01.replace({
        'A': 'Solteiro',
        'B': 'Casado',
        'C': 'Separado',
        'D': 'Viúvo',
        'E': 'Outros'
    })
    filtro[['estcivil']].to_csv(data_path + 'estcivil.csv', index=False)

# PythonOperator para o - constroi_est_civil        
task_est_civil = PythonOperator(
    task_id='constroi_est_civil',
    python_callable=constroi_est_civil,
    dag=dag
)


# Função para realizar um replace e um filtro na coluna Cor da Pele
def constroi_cor():
    filtro = pd.read_csv(data_path + 'enade_filtro.csv')
    filtro['cor'] = filtro.QE_I02.replace({
        'A': 'Branca',
        'B': 'Preta',
        'C': 'Amarela',
        'D': 'Parda',
        'E': 'Indígena',
        'F': "",
        ' ': ""
    })
    filtro[['cor']].to_csv(data_path + 'cor.csv', index=False)

# PythonOperator para o - constroi_cor        
task_cor = PythonOperator(
    task_id='constroi_cor_da_pele',
    python_callable=constroi_cor,
    dag=dag
)


# Função para realizar um replace e um filtro - Escolaridade do Pai
def constroi_escopai():
    filtro = pd.read_csv(data_path + 'enade_filtro.csv')
    filtro['escopai'] = filtro.QE_I04.replace({
        'A': 0,
        'B': 1,
        'C': 2,
        'D': 3,
        'E': 4,
        'F': 5
    })
    filtro[['escopai']].to_csv(data_path + 'escopai.csv', index=False)

# PythonOperator para o - constroi_escopai        
task_escopai = PythonOperator(
    task_id='constroi_escopai',
    python_callable=constroi_escopai,
    dag=dag
)


# Função para realizar um replace e um filtro - Escolaridade do Mãe
def constroi_escomae():
    filtro = pd.read_csv(data_path + 'enade_filtro.csv')
    filtro['escomae'] = filtro.QE_I05.replace({
        'A': 0,
        'B': 1,
        'C': 2,
        'D': 3,
        'E': 4,
        'F': 5
    })
    filtro[['escomae']].to_csv(data_path + 'escomae.csv', index=False)

# PythonOperator para o - constroi_escomae        
task_escomae = PythonOperator(
    task_id='constroi_escomae',
    python_callable=constroi_escomae,
    dag=dag
)

# Função para realizar um replace e um filtro - Renda
def constroi_renda():
    filtro = pd.read_csv(data_path + 'enade_filtro.csv')
    filtro['renda'] = filtro.QE_I08.replace({
        'A': 0,
        'B': 1,
        'C': 2,
        'D': 3,
        'E': 4,
        'F': 5,
        'G': 6
    })
    filtro[['renda']].to_csv(data_path + 'renda.csv', index=False)

# PythonOperator para o - constroi_renda        
task_renda = PythonOperator(
    task_id='constroi_renda',
    python_callable=constroi_renda,
    dag=dag
)


# Task JOIN 

def join_data():
    filtro        = pd.read_csv(data_path + 'enade_filtro.csv')
    idadecent     = pd.read_csv(data_path + 'idadecent.csv')
    idadequadrado = pd.read_csv(data_path + 'idadequadrado.csv')
    estcivil      = pd.read_csv(data_path + 'estcivil.csv')
    cor           = pd.read_csv(data_path + 'cor.csv')
    escopai       = pd.read_csv(data_path + 'escopai.csv')
    escomae       = pd.read_csv(data_path + 'escomae.csv')
    renda         = pd.read_csv(data_path + 'renda.csv')
    

    final = pd.concat([filtro,
                       idadecent,
                       idadequadrado,
                       estcivil,
                       cor,
                       escopai,
                       escomae,
                       renda],
                       axis=1) # realizar o concat por coluna     

    final.to_csv(data_path + 'enade_tratado.csv', index=False)
    print(final)

# PythonOperator para o - join_data        
task_join = PythonOperator(
    task_id='join_data',
    python_callable=join_data,
    dag=dag
)    

# Definindo o encadeamento da execução
start_processing >> get_data >> unzip_file >> task_aplica_filtro 

task_aplica_filtro >> [task_idade_cent, 
                       task_est_civil, 
                       task_cor,
                       task_escopai,
                       task_escomae,
                       task_renda]

task_idade_quad.set_upstream(task_idade_cent)

task_join.set_upstream([task_est_civil, 
                        task_cor, 
                        task_idade_quad, 
                        task_escopai, 
                        task_escomae, 
                        task_renda])