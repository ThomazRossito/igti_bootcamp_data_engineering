# Como instalar o <b>`brModelo`</b> no Linux `Ubuntu 20.04`

1 - Efetue o download do arquivo `brModelo.jar` através do link abaixo:

<b>Link:</b> [SourceForge-brModelo](https://sourceforge.net/projects/brmodelo/)

<br>

2 - Para ficar organizado, crie um diretório em `/opt` e de privilégios, conforme os comandos abaixo:

#### sudo mkdir /opt/brModelo
#### sudo chmod +s /opt/brModelo
#### sudo chmod 777 /opt/brModelo

<br>

3 - Acesse o diretório onde efetuou o download do arquivo `brModelo.jar` e efetue a cópia para o diretório que foi criado em `/opt`, segue o comando abaixo:

#### sudo cp brModelo.jar /opt/brModelo/ 

<br>

4 - Para executar o `brModelo` informe o comando abaixo no terminal:

#### java -jar /opt/brModelo/brModelo.jar

<br>

5 - É possível obter a imagem do ícone do brModelo, segue o comando:

#### curl -o ~/brModelo.png -OL https://github.com/chcandido/brModelo/raw/master/src/imagens/logico.png

#### sudo mv ~/brModelo.png /opt/brModelo/

<br>

6 - Use um editor de sua preferência para criar o atalho no menu do Ubuntu: 

#### sudo vi /usr/share/applications/brModelo.desktop 

<br>

7 - Copie as linhas, que seguem logo abaixo no arquivo aberto e salve:

[Desktop Entry]                                                      
Version=3.2                                                      
Name=brModelo                                                      
Exec=java -jar /opt/brModelo/brModelo.jar                                                      
Icon=/opt/brModelo/brModelo.png                                                      
Type=Application                                                      
Comment=The software for MER                                                      
Path=/opt/brModelo                                                      
Terminal=false                                                      
StartupNotify=true                                                      
Categories=Development;Education;                                                       