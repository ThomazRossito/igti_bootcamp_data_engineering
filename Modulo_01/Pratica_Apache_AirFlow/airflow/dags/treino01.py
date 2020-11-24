#########################################
## Autor: Thomaz Antonio Rossito Neto  ##
## Data: 24/11/2020                    ##
##                                     ##
## Software: Apache AirFlow            ##
## Modalidade: Criação de DAG          ##
## Execução: print Hello AirFlow       ##
##                                     ##
## Curso: BootCamp Engenheiro de Dados ##    
## Instituição: IGTI                   ##
## Link: http://igti.com.br/           ## 
#########################################

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta

# Argumentos default 
default_args = {
    'owner': 'Thomaz Rossito',                                  # é o 'dono/proprietario' da DAG, informar um nome fácil para identificação
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
    "treino-01",                                             # Nome da DAG
    description="Básico Bash Operators e Python Operators",  # Informação sobre a DAG
    default_args=default_args,                               # Argumentos definidos na lista acima
    schedule_interval=timedelta(minutes=2)                   # Intervalo de cada execução 
)

# Definindo a tarefa - Bash Operator
hello_bash = BashOperator(
    task_id="Hello_Bash",                            # Nome que será visualizado no fluxo
    bash_command='echo "Hello Airflow from Bash"',   # O que será executado
    dag=dag                                          # É o fluxo que foi criado acima 
)

# Criando uma função para ser executada no Python Operator
def say_hello():
    print("Hello AirFlow from Python")

# Definindo a tarefa -  Python Operator
hello_python = PythonOperator(
    task_id="Hello_Python",        # Nome que será visualizado no fluxo
    python_callable=say_hello,     # Executa uma função
    dag=dag                        # É o fluxo que foi criado acima 
)

# Definindo o encadeamento da execução
hello_bash >> hello_python