# Buat Class Game untuk diakses client sama server
class Game:
    def __init__(self, id):

        # Player 1 sudah memilih atau player 2 sudah memilih
        self.p1Went = False
        self.p2Went = False
        self.ready = False

        # Current game id
        self.id = id

        # Currently moves are none
        self.moves = [None, None]

        self.wins = [0,0]
        self.ties = 0

    # 0 untuk player1, 1 untuk player2
    def get_player_move(self, p):
        """
        :param p: [0,1]
        :return: Move
        """
        return self.moves[p]

    # Mengupdate Currently moves
    def play(self, player, move):
        self.moves[player] = move
        if player == 0:
            self.p1Went = True
        else:
            self.p2Went = True

    # Kalo siap akan mengupdate di bagian server
    def connected(self):
        return self.ready

    # Kalo kedua pemain meninggalkan permainan
    def bothWent(self):
        return self.p1Went and self.p2Went

    def winner(self):

        p1 = self.moves[0].upper()[0]
        p2 = self.moves[1].upper()[0]
        # Jika P1 menang maka 0, jika P2 menang maka 1, jika seri makan -1
        winner = -1
        if p1 == "B" and p2 == "G":
            winner = 0
        elif p1 == "G" and p2 == "B":
            winner = 1
        elif p1 == "K" and p2 == "B":
            winner = 0
        elif p1 == "B" and p2 == "K":
            winner = 1
        elif p1 == "G" and p2 == "K":
            winner = 0
        elif p1 == "K" and p2 == "G":
            winner = 1

        return winner

    def resetWent(self):
        self.p1Went = False
        self.p2Went = False