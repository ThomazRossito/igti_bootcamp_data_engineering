# Pratica extraída das vídeos aulas do Bootcamp da IGTI

Efetue o download e abra o projeto com o Visual Studio Code

No terminal do VSCode para instalar o Prefect, segue abaixo a instrução contida no site do Prefect

Utilizei para o projeto o sistema operacional linux `Ubuntu 20.04`


## Prefect

[http://prefect.io/](http://prefect.io/)


## 1 - Instalação 

Para instalar o Prefect execute o comando abaixo:

#### pip install prefect

Fonte: [Prefect](https://docs.prefect.io/core/getting_started/installation.html)


## 2 - Configure seu Ambiente no formato - Cloud

Para usar o Prefect com qualquer um dos back-end, você deve primeiro configurar esse back-end por meio da CLI:

#### prefect backend cloud



## 3 - Autenticação com Prefect Cloud 


### 3.1 - Criando um Personal Access Token

Para autenticar, você precisará criar um token de acesso pessoal e configurá-lo com a interface de linha de comando Prefect.

- Faça login em https://cloud.prefect.io
- No menu de 'hamburger' no canto superior esquerdo, vá para `Usuário -> Tokens de acesso pessoais -> Criar um token.`
- Copie o token criado
- Configure a CLI para usar o token de acesso executando

#### prefect auth login -t <COPIED_TOKEN>


### 3.2 - Criando um Runner Token

A implantação e execução de fluxos com um agente também requer um token de API com RUNNER-scoped para o agente. Você pode criar um usando a CLI:

#### prefect auth create-token -n my-runner-token -s RUNNER

You'll need this token later in the tutorial. You can save it in your local configuration either as an environment variable

#### export PREFECT__CLOUD__AGENT__AUTH_TOKEN=<COPIED_RUNNER_TOKEN>

**Obs:** informe entre aspas simples o token


Fonte: [Configure-Environment](https://docs.prefect.io/orchestration/tutorial/configure.html)