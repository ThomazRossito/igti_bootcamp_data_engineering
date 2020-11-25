#########################################
## Autor: Thomaz Antonio Rossito Neto  ##
## Data: 24/11/2020                    ##
##                                     ##
## Software: Apache AirFlow            ##
## Modalidade: Criação de DAG          ##
## Execução: Média dos Passageiros     ##
##           Dados do Titanic          ##
##                                     ##
## Curso: BootCamp Engenheiro de Dados ##    
## Instituição: IGTI                   ##
## Link: http://igti.com.br/           ## 
#########################################


from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import pandas as pd 

# Argumentos default 
default_args = {
    'owner': 'Dados Titanic',                                   # é o 'dono/proprietario' da DAG, informar um nome fácil para identificação
    'depends_on_past': False,                                   # se tem dependências com DAGs anteriores, deixar como False para manter a DAG como autônoma
    'start_date': datetime(2020, 11, 24, 11),                   # Data de início da DAG
    'email': ['email1@email1.com.br', 'email2@email2.com.br'],  # Email que irá receber informações sobre a DAG
    'email_on_failure': False,                                  # Se deseja ser notificado a cada falha que ocorrer na DAG
    'email_on_retry': False,                                    # Se der alguma falha, tentar fazer nova notificação 
    'retries': 1,                                               # Em caso de falha quantas tentativas serão notificadas
    'retry_delay': timedelta(minutes=1)                         # Em caso de falha qual o tempo de tentativa entre uma notificação e outra 
}

# Definindo - DAG (fluxo)
dag = DAG(
    "treino-02",                                                                   # Nome da DAG
    description="Calcular a idade média dos passageiros com os dados do Titanic",  # Informação sobre a DAG
    default_args=default_args,                                                     # Argumentos definidos na lista acima
    schedule_interval="*/2 * * * *"                                                # Intervalo de cada execução 
)

# comando para efetuar o dowload dos dados 
get_data = BashOperator(
    task_id='get-data',
    bash_command='curl https://raw.githubusercontent.com/A3Data/hermione/master/hermione/file_text/train.csv -o ~/airflow/raw/train.csv', 
    dag=dag
)

# Função para calcular idade média dos passageiros
def calculate_mean_age():
    df = pd.read_csv('~/airflow/raw/train.csv') 
    med = df.Age.mean()
    return med

# Função para impressão da média 
def print_age(**context):
    value = context['task_instance'].xcom_pull(task_ids='calcula-idade-media')
    print(f"A idade média no Titanic era {value} anos")    

# Task para calculo da idade média 
task_idade_media = PythonOperator(
    task_id='calcula-idade-media',
    python_callable=calculate_mean_age,
    dag=dag     
)    

# Task para print média da idade 
task_print_idade = PythonOperator(
    task_id='mostra-idade',
    python_callable=print_age,
    provide_context=True,
    dag=dag
)

# Definindo o encadeamento da execução
get_data >> task_idade_media >> task_print_idade