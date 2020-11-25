##########################################
## Autor: Thomaz Antonio Rossito Neto   ##
## Data: 24/11/2020                     ##
##                                      ##
## Software: Apache AirFlow             ##
## Modalidade: Criação de DAG           ##
## Execução: Condicionais c/ Containers ##
##                                      ##
##                                      ##
## Curso: BootCamp Engenheiro de Dados  ##    
## Instituição: IGTI                    ##
## Link: http://igti.com.br/            ## 
##########################################


from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator, BranchPythonOperator
from datetime import datetime, timedelta
import pandas as pd 
import random

# Argumentos default 
default_args = {
    'owner': 'Condicional Dados Titanic',                       # é o 'dono/proprietario' da DAG, informar um nome fácil para identificação
    'depends_on_past': False,                                   # se tem dependências com DAGs anteriores, deixar como False para manter a DAG como autônoma
    'start_date': datetime(2020, 11, 24, 18, 10),               # Data de início da DAG
    'email': ['email1@email1.com.br', 'email2@email2.com.br'],  # Email que irá receber informações sobre a DAG
    'email_on_failure': False,                                  # Se deseja ser notificado a cada falha que ocorrer na DAG
    'email_on_retry': False,                                    # Se der alguma falha, tentar fazer nova notificação 
    'retries': 1,                                               # Em caso de falha quantas tentativas serão notificadas
    'retry_delay': timedelta(minutes=1)                         # Em caso de falha qual o tempo de tentativa entre uma notificação e outra 
}

# Definindo - DAG (fluxo)
dag = DAG(
    "treino-03",                                                                        # Nome da DAG
    description="Calcular a idade média dos passageiros homens ou mulheres do Titanic", # Informação sobre a DAG
    default_args=default_args,                                                          # Argumentos definidos na lista acima
    schedule_interval=timedelta(minutes=2)                                              # Intervalo de cada execução 
)

# comando para efetuar o dowload dos dados 
get_data = BashOperator(
    task_id='get-data',
    bash_command='curl https://raw.githubusercontent.com/A3Data/hermione/master/hermione/file_text/train.csv -o /usr/local/airflow/data/train.csv', 
    dag=dag
)

# Função para sortiar entre homens e mulheres 
def sorteia_h_m():
     return random.choice(['male', 'female'])

# PythonOperator para a função - sorteia_h_m
escolhe_h_m = PythonOperator(
    task_id='escolhe-h-m',
    python_callable=sorteia_h_m,
    dag=dag
)    

# Função que realiza a condição entre homens e mulheres 
def condicao_M_ou_F(**context):
     value = context['task_instance'].xcom_pull(task_ids='escolhe-h-m')
     if value == 'male':
         return 'branch_homem'
     if value == 'female':
         return 'branch_mulher'    

# PythonOperator para a - condicao_M_ou_F
male_female = BranchPythonOperator(
    task_id='condicional',
    python_callable=condicao_M_ou_F,
    provide_context=True,
    dag=dag
)


# Função para calcular idade média dos homens
def mean_homem():
    df = pd.read_csv('/usr/local/airflow/data/train.csv') 
    df = df.loc[df.Sex == 'male']
    print(f"Média de idade dos homens no Titanic:  {df.Age.mean()}")


# PythonOperator para a função - mean_homem
branch_homem = PythonOperator(
    task_id='branch_homem',
    python_callable=mean_homem,
    dag=dag
)

# Função para calcular idade média das mulheres
def mean_mulher():
    df = pd.read_csv('/usr/local/airflow/data/train.csv') 
    df = df.loc[df.Sex == 'female']
    print(f"Média de idade das mulheres no Titanic:  {df.Age.mean()}")


# PythonOperator para a função - mean_mulhr
branch_mulher = PythonOperator(
    task_id='branch_mulher',
    python_callable=mean_mulher,
    dag=dag
)


# Definindo o encadeamento da execução
get_data >> escolhe_h_m >> male_female >> [branch_homem, branch_mulher]
