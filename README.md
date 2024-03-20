# Jogo da velha

## Sobre

Este é um projeto desenvolvido como parte da disciplina de Redes de Computadores. Consiste em uma implementação do jogo da velha utilizando a biblioteca `socket` e `threads` em Python.

O jogo da velha é um clássico passatempo para dois jogadores, onde cada um deles marca alternadamente espaços em uma grade de 3x3. O objetivo é conseguir uma linha, coluna ou diagonal com três símbolos iguais (X ou O).

Neste projeto, o jogo da velha foi implementado como uma aplicação cliente-servidor. O servidor gerencia as conexões entre os jogadores e coordena o progresso do jogo, enquanto os clientes (os jogadores) se conectam ao servidor para jogar entre si.

Este projeto visa fornecer uma experiência prática na implementação de conceitos de redes de computadores, como comunicação entre processos através de sockets e o uso de threads para permitir a interação simultânea de 2 jogadores.


## Instruções de Uso

### Windows
- Certifique-se de ter o Python instalado em sua máquina. Você pode baixá-lo em [python.org](https://www.python.org/downloads/).
  
### Linux
- Para instalar o Python3 no Linux, execute os seguintes comandos no terminal:  
sudo apt update  
sudo apt install python3  

### Executando o Servidor e o Cliente

1. **Clonar ou Baixar**:  
Para clonar:  
git clone https://github.com/sandrogomes7/jogo-da-velha.git  
Se quiser baixar apenas, clique em CODE e clique em *DOWNLOAD ZIP*  


3. **Executar o Servidor**:
No terminal, execute o seguinte comando para iniciar o servidor:  
python3 ./servidor.py *IP do Computador*  

4. **Executar o Cliente**:
No terminal, execute o seguinte comando para iniciar o cliente:  
python3 ./cliente.py *IP do Servidor*  
