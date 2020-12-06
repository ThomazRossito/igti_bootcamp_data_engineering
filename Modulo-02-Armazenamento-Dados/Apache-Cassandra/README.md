# Instalação do Apache Cassandra no Ubuntu 20.04

Apache Cassandra é um software de banco de dados NoSQL popular e de código aberto. Ele fornece alta disponibilidade ao lidar com uma grande quantidade de dados. 

<br>

## ETAPA 1: Instale os pacotes necessários para o Apache Cassandra

Antes de iniciar a instalação do Cassandra no Ubuntu, certifique-se de instalar o <b>`Java OpenJDK 8`</b> e o pacote <b>`api-transport-https`</b> .

<br>

1.1 - Instale Java OpenJDK

O Apache Cassandra precisa do OpenJDK 8 para rodar em um sistema Ubuntu. Atualize seu repositório de pacotes primeiro:

### sudo apt update

Quando o processo terminar, instale o OpenJDK 8 usando o seguinte comando:

### sudo apt install openjdk-8-jdk -y

Quando a instalação for concluída, teste se o Java foi instalado com sucesso, verificando a versão do Java :

### java -version

A saída deve imprimir a versão Java.

<img src="https://phoenixnap.com/kb/wp-content/uploads/2020/06/java-version-cassandra.png">

<br>

1.2 - Instale o pacote <b>`apt-transport-https`</b>

Em seguida, instale o pacote de transporte APT. Você precisa adicionar este pacote ao seu sistema para permitir o acesso aos repositórios usando HTTPS.

Digite este comando:

### sudo apt install apt-transport-https

A saída deve imprimir um exemplo que destaca as duas etapas finais do processo de instalação do `apt-transport-https`

<img src="https://phoenixnap.com/kb/wp-content/uploads/2020/06/apt-transport-package-cassandra.png">

<br>

## ETAPA 2: Adicionar Repositório Apache Cassandra e Importar Chave GPG

Você precisa adicionar o repositório Apache Cassandra e extrair a chave GPG antes de instalar o banco de dados.

Digite o comando abaixo para adicionar o repositório Cassandra à lista de fontes:

### sudo sh -c 'echo "deb http://www.apache.org/dist/cassandra/debian 40x main" > /etc/apt/sources.list.d/cassandra.list'

Em seguida, use o wget comando para extrair a chave pública do URL abaixo:

### wget -q -O - https://www.apache.org/dist/cassandra/KEYS | sudo apt-key add -

<br>

## ETAPA 3: Instale o Apache Cassandra

Agora você está pronto para instalar o Cassandra no Ubuntu.

Atualize a lista de pacotes do repositório:

### sudo apt update

Em seguida, execute o comando de instalação:

### sudo apt install cassandra

<br>

## ETAPA 4: Verifique a instalação do Apache Cassandra 

### nodetool status

<img src="https://phoenixnap.com/kb/wp-content/uploads/2020/06/nodetool-cassandra.png">

### sudo systemctl status cassandra

A saída deve ser exibida `active (running)` em verde.

<img src="https://phoenixnap.com/kb/wp-content/uploads/2020/06/cassandra-status.png">

Comandos para iniciar, parar, reiniciar 

### sudo systemctl start cassandra
### sudo systemctl stop cassandra
### sudo systemctl restart cassandra

<br>

Para iniciar o Cassandra automaticamente após a inicialização, use o seguinte comando:

### sudo systemctl enable cassandra

<br>

## ETAPA 5: teste o shell de linha de comando do Cassandra

O pacote de software Cassandra vem com sua ferramenta de linha de comando (CLI). Esta ferramenta usa Cassandra Query Language (CQL) para comunicação.

Para iniciar um novo shell, abra o terminal e digite:

### cqlsh

<br>

<br>


<b>Link:</b> [Comandos: Apache Cassandra](https://www.tutorialspoint.com/cassandra/index.htm) 
<b>Fonte:</b> [Instalação Apache Cassandra Ubuntu](https://phoenixnap.com/kb/install-cassandra-on-ubuntu)