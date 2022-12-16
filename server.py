import socket
from _thread import *
import pickle
from game import Game

server = "192.168.1.4"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen()
print("Kumpulkan NEN kalian dan Selamat Menikmati...")

# connected untuk menyimpan client yg terhubung
connected = set()
# games dictionary untuk menyimpan (id=key, games=value)
games = {}
# idcount untuk mentrack id saat ini
idCount = 0


def threaded_client(conn, p, gameId):
    global idCount
    conn.send(str.encode(str(p)))

    reply = ""
    while True:
        try:
            # 4096bit jaga2 kalo kebanyakan informasi
            data = conn.recv(4096).decode()

            if gameId in games:
                game = games[gameId]

                if not data:
                    break
                else:
                    if data == "reset":
                        game.resetWent()
                    # kalo bukan reset dan get berarti "move"
                    elif data != "get":
                        game.play(p, data)

                    conn.sendall(pickle.dumps(game))
            else:
                break
        except:
            break

    print("Koneksi hilang!!!")
    try:
        del games[gameId]
        print("Menutup Game", gameId)
    except:
        pass
    idCount -= 1
    conn.close()



while True:
    conn, addr = s.accept()
    print("Tersambung ke ", addr)

    # idcount untuk mentrack berapa user yang connect ke server bersamaan
    idCount += 1
    p = 0

    # setiap 2 orang yg connect akan increment gameid
    gameId = (idCount - 1)//2

    # Jika ada 1 orang yg join maka akan membuat game baru
    if idCount % 2 == 1:
        games[gameId] = Game(gameId)
        print("Buat game baru...")
    else:
        games[gameId].ready = True
        p = 1


    start_new_thread(threaded_client, (conn, p, gameId))