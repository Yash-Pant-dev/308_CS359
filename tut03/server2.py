import socket
import threading


def calculator(c, addr):
    print("calc called")
    # calc function is the target for the thread
    while (True):
        c.send('Connection established. \nProvide your input: '.encode())
        # connection has been established
        input = c.recv(2048).decode()

        print("Client", addr, input)
        try:
            ans = str(eval(input)) #evaluate the input 
        except:
            ans = "Input is invalid."

        print("Response:", addr, ans)
        c.send(ans.encode())
        cont = c.recv(2048).decode()
        # take 2048 bytes of data here it only checks yes or no
        if (cont == "n"):
            print("Connection has been closed. ", addr)
            c.close()
            break
        
            


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Socket successfully created")
    port = 12999
    # server listens on port 12999
    s.bind(('', port))
    print("Socket is bound on:")
    print(port)
    s.listen()
    print("Listening on the socket:")
    while (True):
        c, addr = s.accept()
        print('Connection accepted on :', addr)
        t1 = threading.Thread(target=calculator, args=(c, addr))
        t1.start()


if __name__ == "__main__":
    main()
