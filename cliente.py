import socket
import json
import sys 
from classeJogo import JogoVelha # Importa a classe JogoVelha

# IP padrão e Porta
HOST = '127.0.0.1'
PORTA = 7777

# Se o usuário passar um IP como argumento
if len(sys.argv) > 1:
    HOST = sys.argv[1]

# Status
DEF_NOME = "DEF_NOME"   # Status para definir nome
OBT_NOME = "OBT_NOME"   # Status para obter nome
AGUARDAR = "AGUARDAR"   # Status para aguardar
INICIAR = "INICIAR"     # Status para iniciar o jogo
JOGAR = "JOGAR"         # Status para jogar
ATUALIZAR = "ATUALIZAR" # Status para atualizar o jogo
SAIR = "SAIR"           # Status para sair do jogo
FINALIZAR = "FINALIZAR" # Status para finalizar o jogo

JOGADOR1 = "Jogador 1"
JOGADOR2 = "Jogador 2"

jogo = JogoVelha() # Instância da classe JogoVelha

# Conexão com o servidor
clienteSocket = socket.socket()
clienteSocket.connect((HOST, PORTA))

# Recebendo todas as respostas do servidor
while True:
    pacote = clienteSocket.recv(2048) # Recebendo pacote do servidor

    if not pacote:
        print("Desconectado do servidor")
        break

    pacote = json.loads(pacote.decode()) # Decodificando pacote
    jogo.casas = pacote["casas"]         # Atualizando tabuleiro

    # Verificando status do pacote
    # Se o status for OBT_NOME, o cliente irá definir o nome
    if pacote["status"] == OBT_NOME:
        print("Jogo da Velha\n")

        if(pacote["player"] == JOGADOR1):
            print("Você será o jogador 1 (X)\n") 
            mensagem = str(input("Por favor, digite seu nome: "))
        else:
            print("Você será o jogador 2 (O)\n")
            mensagem = str(input("Por favor, digite seu nome: "))

        pacote = {"casas": jogo.casas, "mensagem": mensagem, "player": pacote["player"], "status": DEF_NOME}
        pacoteJSON = json.dumps(pacote).encode()  # Codificando pacote
        clienteSocket.send(pacoteJSON)            # Enviando pacote 

    # Se o status for AGUARDAR, cliente fica aguardando
    elif pacote["status"] == AGUARDAR:
        jogo.atualizarTab()
        print(pacote["mensagem"])

    # Se o status for INICIAR, o jogo é iniciado
    elif pacote["status"] == INICIAR:
        jogo.atualizarTab()
        if pacote["player"] == JOGADOR1:
            mensagem = input(pacote["mensagem"])
            pacote = {"casas": jogo.casas, "mensagem": mensagem, "player": pacote["player"], "status": ATUALIZAR}
        else:
            print(pacote["mensagem"])
            pacote = {"casas": jogo.casas, "mensagem": "Aguardando o primeiro movimento do Jogador 1.", "player": pacote["player"], "status": AGUARDAR}

        pacoteJSON = json.dumps(pacote).encode() 
        clienteSocket.send(pacoteJSON)

    # Se o status for JOGAR, o cliente irá jogar
    elif pacote["status"] == JOGAR:
        jogo.atualizarTab()
        mensagem = input(pacote["mensagem"])
        pacote = {"casas": jogo.casas, "mensagem": mensagem, "player": pacote["player"], "status": ATUALIZAR}
        pacoteJSON = json.dumps(pacote).encode()
        clienteSocket.send(pacoteJSON)

    # Se o status for FINALIZAR, o cliente irá decidir se quer jogar novamente
    elif pacote["status"] == FINALIZAR:
        escolha = ""
        while escolha != "S" and escolha != "N":
            jogo.atualizarTab()
            print(pacote["mensagem"])
            escolha = str(input("Gostaria de jogar novamente? (S/N): "))
            escolha = escolha.upper()
            print()

        pacote = {"casas": jogo.casas, "mensagem": escolha, "player": pacote["player"], "status": FINALIZAR}
        pacoteJSON = json.dumps(pacote).encode()
        clienteSocket.send(pacoteJSON)
        
    # Se o status for SAIR, o cliente irá sair do jogo
    elif pacote["status"] == SAIR:
        print(pacote["mensagem"])
        mensagem = "Saindo do jogo.\n"
        pacote = {"mensagem": mensagem, "player": pacote["player"], "status": "SAIR"}
        pacoteJSON = json.dumps(pacote).encode()
        clienteSocket.send(pacoteJSON)
        break
    
    # Se o status for diferente, por exemplo "INTRUSO", 
    # mostrara a mensagem para quem tentou entrar no jogo
    else:
        print(pacote["mensagem"])
        break

clienteSocket.close() # Fechando conexão com o servidor