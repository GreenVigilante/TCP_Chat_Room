import socket
import threading
host = "localhost"
port = 9999
nickname = input("Enter Name: ")

yappers = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
yappers.connect((host, port))

if nickname == "admin":
    password = str(input("Enter password for admin: "))
stop_func = False
write_func = True
def recieve():
    global stop_func
    while True:
        if stop_func:
            break
        try:
            message = yappers.recv(1024).decode("ascii")
            if message == "Nickname: ":
                yappers.send(nickname.encode("ascii"))
                admin_mess = yappers.recv(1024).decode("ascii")
                if admin_mess == "adminjumpsin":
                    yappers.send(password.encode("ascii"))
                    if yappers.recv(1024).decode("ascii") == "NO":
                        print("You ain't no admin!")
                        stop_func = True
                    else:
                        print("Hola admin. Who we harrassing today?")
                elif admin_mess == "BAN":
                    print("You have been banned ;)")
                    yappers.close()
                    stop_func = True
                elif admin_mess == "CHOOSEN":
                    print("Name already been choosen :)")
                    yappers.close()
                    stop_func = True
            else:
                print(message)
        except:
            print("An error has occured boomer")
            yappers.close()
            break

def write():
    while True:
        if stop_func:
            break
        message = f"""{nickname}: {input("")}"""
        if message[len(nickname)+2:].startswith("/"):
            if nickname == "admin":
                if message[len(nickname)+2:].startswith("/ban"):
                    yappers.send(f"ban {message[len(nickname)+2+5:]}".encode("ascii"))
                elif message[len(nickname)+2:].startswith("/kick"):
                    yappers.send(f"kick {message[len(nickname)+2+6:]}".encode("ascii"))
            else:
                print("You aint no admin boomer")
        elif message == f"{nickname}: ":
            pass
        elif message == f"{nickname}: exit()":
            yappers.close()
            exit
        else:
            yappers.send(message.encode("ascii"))

tr = threading.Thread(target=recieve)
tr.start()
tw = threading.Thread(target=write)
tw.start()