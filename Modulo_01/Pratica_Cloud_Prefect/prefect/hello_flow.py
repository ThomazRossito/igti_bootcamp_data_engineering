import prefect
from prefect import task, Flow

@task
def hello_flow():
    logger = prefect.context.get("logger")
    logger.info("Hello world do Prefect em Cloud!!!")

with Flow("Hello Flow") as flow:
    hello_flow()

# Registra um Flow com a API do Prefect
flow.register(project_name="Hello Flow")    

# Gera um agente local e executa um processo
flow.run_agent()
