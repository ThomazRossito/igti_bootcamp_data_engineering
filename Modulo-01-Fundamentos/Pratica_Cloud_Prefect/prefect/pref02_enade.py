from datetime import datetime, timedelta
import pendulum
import prefect
from prefect import task, Flow
from prefect.schedules import CronSchedule
import pandas as pd
from io import BytesIO
import zipfile
import requests


schedule = CronSchedule(
    cron = "*/10 * * * * ",  # *minutos *horas *dia *mês *dia semana 
    start_date=pendulum.datetime(2020, 11, 25, 18, 17, tz='America/Sao_Paulo')
)

@task
def get_raw_data():
    # Atribuindo o link a um objeto 'url'
    url = 'http://download.inep.gov.br/microdados/Enade_Microdados/microdados_enade_2019.zip'

    # Faz o download do conteúdo 
    filebytes = BytesIO(requests.get(url).content)

    # Extrair o conteúdo do 'zipfile'
    myzip = zipfile.ZipFile(filebytes)
    myzip.extractall()
    path = './microdados_enade_2019/2019/3.DADOS/'
    return path

@task
def aplica_filtros(path):
    cols = ['CO_GRUPO','TP_SEXO','NU_IDADE','NT_GER','NT_FG','NT_CE','QE_I01','QE_I02','QE_I04','QE_I05','QE_I08'] 
    enade = pd.read_csv(path + 'microdados_enade_2019.txt', sep=";", decimal=",", encoding='latin1', usecols=cols)   
    enade = enade.loc[
        (enade.NU_IDADE > 20) &
        (enade.NU_IDADE < 40) &
        (enade.NT_GER > 0)
    ]       
    return enade

@task
def constri_idade_centralizada(df):
    idade = df[['NU_IDADE']]   
    idade['idadecent'] = idade.NU_IDADE - idade.NU_IDADE.mean() 
    return idade[['idadecent']]    

@task
def constroi_idade_cent_quad(df):
    idadecent = df.copy()
    idadecent['idade2'] = idadecent.idadecent ** 2    
    return idadecent[['idade2']]

@task
def constroi_est_civil(df):
    filtro = df[['QE_I01']]
    filtro['estcivil'] = filtro.QE_I01.replace({
        'A': 'Solteiro',
        'B': 'Casado',
        'C': 'Separado',
        'D': 'Viúvo',
        'E': 'Outros'
    })
    return filtro[['estcivil']]

@task
def constroi_cor(df):
    filtro = df[['QE_I02']]
    filtro['cor'] = filtro.QE_I02.replace({
        'A': 'Branca',
        'B': 'Preta',
        'C': 'Amarela',
        'D': 'Parda',
        'E': 'Indígena',
        'F': "",
        ' ': ""
    })
    return filtro[['cor']]

@task
def constroi_escopai(df):
    filtro = df[['QE_I04']]
    filtro['escopai'] = filtro.QE_I04.replace({
        'A': 0,
        'B': 1,
        'C': 2,
        'D': 3,
        'E': 4,
        'F': 5
    })
    return filtro[['escopai']]

@task
def constroi_escomae(df):
    filtro = df[['QE_I05']]
    filtro['escomae'] = filtro.QE_I05.replace({
        'A': 0,
        'B': 1,
        'C': 2,
        'D': 3,
        'E': 4,
        'F': 5
    })
    return filtro[['escomae']]

@task
def constroi_renda(df):
    filtro = df[['QE_I08']]
    filtro['renda'] = filtro.QE_I08.replace({
        'A': 0,
        'B': 1,
        'C': 2,
        'D': 3,
        'E': 4,
        'F': 5,
        'G': 6
    })
    return filtro[['renda']]


@task
def join_data(df, idadecent, idadequadrado, estcivil, cor, escopai, escomae, renda):

    final = pd_concat([df, 
                       idadecent, 
                       idadequadrado, 
                       estcivil, 
                       cor, 
                       escopai, 
                       escomae, 
                       renda],axis=1)

    final = final[['CO_GRUPO', 
                   'TP_SEXO', 
                   'idadecent', 
                   'idade2', 
                   'estcivil', 
                   'cor', 
                   'escopai', 
                   'escomae', 
                   'renda']]                  

    logger = prefect.context.get("logger")
    logger.info(final.head().to_json())    

    final.to_csv('enade_tratado_2019.csv', index=False)               

# Encadeamento 
with Flow("Enade_2019", schedule=schedule) as flow:
    path = get_raw_data()
    filtro = aplica_filtros(path)
    idadecent = constri_idade_centralizada(filtro)
    idadequadrado = constri_idade_centralizada(idadecent)
    estcivil = constroi_est_civil(filtro)
    cor = constroi_cor(filtro)
    escomae = constroi_escomae(filtro)
    escopai = constroi_escopai(filtro)
    renda = constroi_renda(filtro)

    j = join_data(filtro,
                  idadecent,
                  idadequadrado,
                  estcivil,
                  cor,
                  escomae,
                  escopai,
                  renda)


# Código para criar um projeto com uma descrição via terminal
# prefect create project Dados_Enade_2019 --description "Projeto de ETL com Dados do Enade 2019 na Cloud Prefect"

# Registra um Flow com a API do Prefect
flow.register(project_name="Dados_Enade_2019", idempotency_key=flow.serialized_hash())    

# Gera um agente local e executa um processo
flow.run_agent()    