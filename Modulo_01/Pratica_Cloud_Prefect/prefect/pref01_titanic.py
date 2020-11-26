from datetime import datetime, timedelta
import prefect
from prefect import task, Flow
from prefect.schedules import IntervalSchedule
import pandas as pd

# Realizar tentativas 
retry_delay = timedelta(minutes=1)
schedule = IntervalSchedule(interval=timedelta(minutes=2))

@task
def get_data():
    df = pd.read_csv('https://raw.githubusercontent.com/A3Data/hermione/master/hermione/file_text/train.csv')
    return df

@task
def calcula_media_idade(df):
    return df.Age.mean()

@task
def exibe_media_calculada(m):
    logger = prefect.context.get("logger")
    logger.info(f"A média de todas as idades calculadas foi: {m}")

@task
def exibe_dataset(df):
    logger = prefect.context.get("logger")
    logger.info(df.head().to_json())


with Flow("Titanic-Media-Idade", schedule=schedule) as flow:
    df = get_data()
    med = calcula_media_idade(df)
    ex = exibe_media_calculada(med)
    ed = exibe_dataset(df)


# Código para criar um projeto com uma descrição via terminal
# prefect create project Titanic-Media-Idade --description "Projetos do Bootcamp de Eng. de Dados do IGTI com a Cloud Prefect"

# Registra um Flow com a API do Prefect
flow.register(project_name="Titanic-Media-Idade", idempotency_key=flow.serialized_hash())    

# Gera um agente local e executa um processo
flow.run_agent()    