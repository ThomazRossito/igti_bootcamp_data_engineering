# Pratica extraída das vídeos aulas do Bootcamp da IGTI

Efetue o download e abra o projeto com o Visual Studio Code

No terminal para instalar o Apache AirFlow segue abaixo a instrução contida no site do Apache AirFlow

Utilizei para o projeto o sistema operacional `linux Ubuntu 20.04`


## Instalação do Apache AirFlow

airflow needs a home, ~/airflow is the default,                    
but you can lay foundation somewhere else if you prefer                    
(optional)
### export AIRFLOW_HOME=~/airflow

install from pypi using pip
### pip install apache-airflow

initialize the database
### airflow initdb

start the web server, default port is 8080
### airflow webserver -p 8080

start the scheduler
### airflow scheduler

visit localhost:8080 in the browser and enable the example dag in the home page

Fonte: [Apache AirFlow](https://airflow.apache.org/docs/stable/start.html)
