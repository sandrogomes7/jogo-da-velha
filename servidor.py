import socket
import threading
import json
import random
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

jogadores = {"Jogador 1": {}, "Jogador 2": {}} # Dicionário para armazenar os jogadores

JOGADOR1 = "Jogador 1" 
JOGADOR2 = "Jogador 2"

jogo = JogoVelha() # Instância da classe JogoVelha

primeiroJogador = ""

# Classe para criar threads
class ClienteThread(threading.Thread):
    # Inicializa a thread
    def __init__(self, ip, porta, clienteSocket):
        threading.Thread.__init__(self)
        self.ip = ip
        self.porta = porta
        self.conexaoCliente = clienteSocket
        print("Nova thread iniciada: " + ip)
        
        # Escolhe aleatoriamente o jogador que irá começar
        global primeiroJogador
        jogador_atual = random.choice([JOGADOR1, JOGADOR2])

        if jogadores[jogador_atual]:
            jogador_atual = JOGADOR2 if jogador_atual == JOGADOR1 else JOGADOR1

        if (jogador_atual == JOGADOR1 and primeiroJogador == ""):
            primeiroJogador = JOGADOR1
        elif (jogador_atual == JOGADOR2 and primeiroJogador == ""):
            primeiroJogador = JOGADOR2

        # Atualiza o dicionário com as informações do jogador atual
        print(f"Conexão do {jogador_atual} estabelecida.")
        jogadores[jogador_atual].update({"conexao": {}})
        jogadores[jogador_atual]["conexao"]["ip"] = self.ip
        jogadores[jogador_atual]["conexao"]["porta"] = self.porta
        jogadores[jogador_atual]["conexao"]["socket"] = self.conexaoCliente
        jogadores[jogador_atual]["nome"] = jogador_atual
        jogadores[jogador_atual]["status"] = OBT_NOME

    # Função para executar a thread e receber as requisições do cliente
    def run(self):
        global primeiroJogador
        print("Conexão de : " + self.ip)
        mensagem = "Bem-vindo ao servidor.\n\n"

        # Servidor envia primeira requisição para o cliente 
        if primeiroJogador == JOGADOR1:
            if not jogadores[JOGADOR2] and jogadores[JOGADOR1]["nome"] == JOGADOR1:
                enviarRequisicao(mensagem, JOGADOR1, OBT_NOME)

            if jogadores[JOGADOR2] and jogadores[JOGADOR2]["nome"] == JOGADOR2:
                enviarRequisicao(mensagem, JOGADOR2, OBT_NOME)
        else:
            if not jogadores[JOGADOR1] and jogadores[JOGADOR2]["nome"] == JOGADOR2:
                enviarRequisicao(mensagem, JOGADOR2, OBT_NOME)

            if jogadores[JOGADOR1] and jogadores[JOGADOR1]["nome"] == JOGADOR1:
                enviarRequisicao(mensagem, JOGADOR1, OBT_NOME)
        try:
            while True:
                pacote = self.conexaoCliente.recv(2048) # Recebe as requisições do cliente

                if not pacote:
                    break

                pacote = pacote.decode()    # Decodifica o pacote
                pacote = json.loads(pacote) # Converte o pacote para JSON

                if (pacote["player"] == JOGADOR1):
                    print("Recebendo informação do Jogador 1 (%s) (IP: %s):\nMensagem: %s\nPlayer: %s\nStatus: %s \n" % (jogadores[pacote["player"]]["nome"], self.ip, pacote["mensagem"], pacote["player"], pacote["status"]))

                    if pacote["mensagem"].isdigit():
                        if int(pacote["mensagem"]) >= 1 and int(pacote["mensagem"]) <= 9:
                            if not jogo.casas[int(pacote["mensagem"]) - 1].isdigit():
                                print(jogadores[pacote["player"]]["nome"] + " jogou na casa " + pacote["mensagem"] + " que já foi jogada.")
                        elif (int(pacote["mensagem"]) < 1 or int(pacote["mensagem"]) > 9):
                            print(jogadores[pacote["player"]]["nome"] + " jogou na casa " + pacote["mensagem"] + " que é inválida.")
                        else:
                            print(jogadores[pacote["player"]]["nome"] + " jogou na casa " + pacote["mensagem"] + " que é válida.")

                else:
                    print("Recebendo informação do Jogador 2 (%s) (%s):\nMensagem: %s\nPlayer: %s\nStatus: %s \n" % (jogadores[pacote["player"]]["nome"],self.ip, pacote["mensagem"], pacote["player"], pacote["status"]))

                    if pacote["mensagem"].isdigit():
                        if int(pacote["mensagem"]) >= 1 and int(pacote["mensagem"]) <= 9:
                            if not jogo.casas[int(pacote["mensagem"]) - 1].isdigit():
                                print(jogadores[pacote["player"]]["nome"] + " jogou na casa " + pacote["mensagem"] + " que já foi jogada.")
                        elif (int(pacote["mensagem"]) < 1 or int(pacote["mensagem"]) > 9):
                            print(jogadores[pacote["player"]]["nome"] + " jogou na casa " + pacote["mensagem"] + " que é inválida.")
                        else:
                            print(jogadores[pacote["player"]]["nome"] + " jogou na casa " + pacote["mensagem"] + " que é válida.")

                # Se servidor receber um status de "DEF_NOME"
                if pacote["status"] == DEF_NOME:
                    jogadorAtual = pacote["player"]
                    jogadores[jogadorAtual]["nome"] = pacote["mensagem"]

                    if primeiroJogador == JOGADOR1:
                        if jogadorAtual == JOGADOR1:
                            enviarRequisicao("Esperando o 2º jogador se conectar...", JOGADOR1, AGUARDAR)

                        elif jogadorAtual == JOGADOR2:
                            enviarRequisicao("Você é X. Insira o número da casa (1-9): ", JOGADOR1, INICIAR)
                            enviarRequisicao("Esperando o outro jogador fazer a jogada", JOGADOR2, INICIAR)
                        else:
                            print("Erro!")

                    else:
                        if jogadorAtual == JOGADOR2:
                            enviarRequisicao("Esperando o 2º jogador se conectar...", JOGADOR2, AGUARDAR)

                        elif jogadorAtual == JOGADOR1:
                            enviarRequisicao("Você é X. Insira o número da casa (1-9): ", JOGADOR1, INICIAR)
                            enviarRequisicao("Esperando o outro jogador fazer a jogada", JOGADOR2, INICIAR)
                        else:
                            print("Erro!")

                # Se servidor receber um status de "ATUALIZAR"
                elif pacote["status"] == ATUALIZAR:
                    jogada = pacote["mensagem"]
                    if not jogada.isdigit() or int(jogada) < 1 or int(jogada) > 9 or not jogo.casas[int(jogada) - 1].isdigit():
                        enviarRequisicao("Casa inválida\nInsira o número da casa (1-9): ", pacote["player"], JOGAR)

                    else:
                        atualizarCasas(pacote["player"], int(jogada) - 1)
                        # Verificar se o jogador atual ganhou
                        if jogo.verificarVencedor(pacote["player"]):
                            print("\t" + jogadores[pacote["player"]]["nome"] + " (" + pacote["player"] + ")" + " GANHOU!")
                            enviarRequisicao(jogadores[pacote["player"]]["nome"].upper() + " VOCÊ GANHOU !!", pacote["player"], FINALIZAR)
                            pacote["player"] = inverterJogadores(pacote["player"])
                            print("\t" + jogadores[pacote["player"]]["nome"] + " (" + pacote["player"] + ")" + " PERDEU!")
                            enviarRequisicao(jogadores[pacote["player"]]["nome"].upper() + " VOCÊ PERDEU !!", pacote["player"], FINALIZAR)
                        # Verificar se deu velha
                        elif jogo.deuVelha():
                            enviarRequisicao("DEU VELHA!!!\n", pacote["player"], FINALIZAR)
                            pacote["player"] = inverterJogadores(pacote["player"])
                            enviarRequisicao("DEU VELHA!!!\n", pacote["player"], FINALIZAR)
                            print("\tJOGO DEU VELHA")
                        # Se não houve vencedor
                        else:
                            if jogadores[pacote["player"]]:
                                pacote["player"] = inverterJogadores(pacote["player"])
                                if jogadores[pacote["player"]]:
                                    pacote["player"] = inverterJogadores(pacote["player"]) 
                                    enviarRequisicao("Não digite nada! Espere o outro jogador jogar", pacote["player"], AGUARDAR) 
                                    pacote["player"] = inverterJogadores(pacote["player"])
                                    if (pacote["player"] == JOGADOR1):
                                        enviarRequisicao("Você é X. Insira o número da casa (1-9): ", pacote["player"], JOGAR)
                                    else:
                                        enviarRequisicao("Você é O. Insira o número da casa (1-9): ", pacote["player"], JOGAR)
                                else:
                                    jogo.resetar()
                                    enviarRequisicao(jogadores[pacote["player"]]["nome"] + " saiu do jogo.\nEsperando jogador...", inverterJogadores(pacote["player"]), AGUARDAR) 
                            else:
                                pacote["player"] = inverterJogadores(pacote["player"])
                                jogo.resetar()
                                enviarRequisicao(jogadores[pacote["player"]]["nome"] + "saiu do jogo.\nEsperando jogador...", inverterJogadores(pacote["player"]), AGUARDAR)
                
                    if pacote["mensagem"].isdigit() and int(pacote["mensagem"]) >= 1 and int(pacote["mensagem"]) <= 9:
                        jogo.mostrarTab()
                    elif not pacote["mensagem"].isdigit():
                        print("A jogada foi inválida.\n")

                # Se servidor receber um status de "AGUARDAR"
                elif pacote["status"] == AGUARDAR:
                    print(pacote["player"] + " enviou um status de ""AGUARDAR"". Mensagem:\n" + pacote["mensagem"] + "\n")
                
                # Se servidor receber um status de "FINALIZAR"
                elif pacote["status"] == FINALIZAR:
                    if pacote["mensagem"] == "S":
                        if jogadores[JOGADOR1] and jogadores[JOGADOR2]:
                            listaCasas = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]

                            if jogo.casas != listaCasas:
                                if pacote["player"] == JOGADOR1:
                                    enviarRequisicao("Esperando se o outro jogador quer jogar novamente ", JOGADOR1, AGUARDAR)
                                    jogo.casas = listaCasas
                                else:
                                    enviarRequisicao("Esperando se o outro jogador quer jogar novamente", JOGADOR2, INICIAR)
                                    jogo.casas = listaCasas
                            else:
                                enviarRequisicao("Você é X. Insira o número da casa (1-9): ", JOGADOR1, INICIAR)
                                enviarRequisicao("Esperando o outro jogador fazer a jogada", JOGADOR2, INICIAR)

                    elif pacote["mensagem"] == "N":
                        if  pacote["player"] == JOGADOR1:
                            enviarRequisicao("Você saiu do jogo.", JOGADOR1, SAIR)
                            enviarRequisicao("Jogo acabou! Jogador 2 não quis continuar.", JOGADOR2, SAIR)
                            
                        if pacote["player"] == JOGADOR2:
                            enviarRequisicao("Você saiu do jogo.", JOGADOR2, SAIR)
                            enviarRequisicao("Jogo acabou! Jogador 1 não quis continuar.", JOGADOR1, SAIR) 
                
                # Se servidor receber um status de "SAIR"
                elif pacote["status"] == SAIR:
                    print(pacote["player"] + " enviou um status de ""SAIR"". Mensagem:\n" + pacote["mensagem"])
                    jogadores[pacote["player"]] = {}
            # Fim do while    
        except ConnectionResetError:
            print()

        jogo.resetar()
        if jogadores[JOGADOR1] and self.porta == jogadores[JOGADOR1]["conexao"]["porta"]:
            print("*\n*\n*\nCliente (JOGADOR1) em " + str(self.ip) + " desconectado...\n")
            jogadores[JOGADOR1] = {}

        elif jogadores[JOGADOR2] and self.porta == jogadores[JOGADOR2]["conexao"]["porta"]:
            print("*\n*\n*\nCliente (JOGADOR2) em " + str(self.ip) + " desconectado...\n")
            jogadores[JOGADOR2] = {}

# Função para enviar requisição para o cliente
def enviarRequisicao(mensagemEnviada, jogadorAtual, statusAtual):
    if jogadorAtual in jogadores and "conexao" in jogadores[jogadorAtual]:
        pacote = {"casas": jogo.casas, "mensagem": mensagemEnviada, "player": jogadorAtual, "status": statusAtual}
        pacoteJSON = json.dumps(pacote).encode()
        jogadores[jogadorAtual]["conexao"]["socket"].send(pacoteJSON)

# Função para atualizar as casas
def atualizarCasas(jogadorAtual, indice):
    if jogadorAtual == JOGADOR1:
        jogo.casas[indice] = "X"
    elif jogadorAtual == JOGADOR2:
        jogo.casas[indice] = "O"

# Função para inverter jogadores
def inverterJogadores(jogadorAtual):
    if jogadorAtual == JOGADOR1:
        return JOGADOR2
    elif jogadorAtual == JOGADOR2:
        return JOGADOR1
    else:
        print("Erro!")
        exit(-1)

# Main
# Cria o socket do servidor com IPv4 e TCP
socketServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Permite que o servidor reutilize a porta
socketServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

socketServer.bind((HOST, PORTA))

print("Servidor iniciado!\n")
print("IP: " + HOST + "\n")

while True:
    socketServer.listen(3)
    print("Esperando conexões/jogadas...\n")

    (conexaoCliente, (IP, PORTA)) = socketServer.accept()

    # Verifica se o servidor já está cheio
    if jogadores[JOGADOR1] and jogadores[JOGADOR2]:
        print("Um intruso tentou conectar no servidor! Conexão negada!\n")
        pacote = {"casas": "{}", "mensagem": "Jogo permitido apenas para 2 jogadores!", "status": "INTRUSO"}
        conexaoCliente.send(json.dumps(pacote).encode())
        conexaoCliente.close()
        continue
    else:
        novaThread = ClienteThread(IP, PORTA, conexaoCliente)
        novaThread.start()