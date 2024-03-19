import os

def limpar_tela():
    sistema_operacional = os.name
    if sistema_operacional == "nt": # Windows
        os.system("cls")
    elif sistema_operacional == "posix": # Linux, Mac, etc
        os.system("clear")

# Limpar a tela
limpar_tela()

class JogoVelha:
    # Inicializando o tabuleiro
    def __init__(self):
        self.casas = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]

    # Mostra o tabuleiro
    def mostrarTab(self):
        print("\n\t╔═════════════════════════════════════════════╗")
        print("\t║                                             ║")
        print("\t║                Jogo da Velha                ║")
        print("\t║                                             ║")
        print("\t║                                             ║")
        print("\t║                ╔═══╦═══╦═══╗                ║")
        print("\t║                ║ %s ║ %s ║ %s ║                ║" % (self.casas[0], self.casas[1], self.casas[2]))
        print("\t║                ╠═══╬═══╬═══╣                ║")
        print("\t║                ║ %s ║ %s ║ %s ║                ║" % (self.casas[3], self.casas[4], self.casas[5]))
        print("\t║                ╠═══╬═══╬═══╣                ║")
        print("\t║                ║ %s ║ %s ║ %s ║                ║" % (self.casas[6], self.casas[7], self.casas[8]))
        print("\t║                ╚═══╩═══╩═══╝                ║")
        print("\t║                                             ║")
        print("\t║                                             ║")
        print("\t╚═════════════════════════════════════════════╝")
        print()

    # Atualiza o tabuleiro
    def atualizarTab(self):
        limpar_tela()
        self.mostrarTab()

    # Verifica se tem um vencedor
    def verificarVencedor(self, jogadorAtual):
        movimento = "X" if jogadorAtual == "Jogador 1" else "O"
        for x, y, z in [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]:
            if self.casas[x] == self.casas[y] == self.casas[z]:
                if self.casas[x] == movimento:
                    return True
        return False

    # Verifica se o jogo deu velha
    def deuVelha(self):
        for casa in self.casas:
            if casa.isdigit():
                return False
        return True
    
    # Reseta o tabuleiro
    def resetar(self):
        self.casas = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]