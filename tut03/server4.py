import socket
import select

socket_list = []
sock_write = []
socket_del = {}
socket_inp = {}
""" socket_list=[] creates a list to store connected sockets.
sock_write=[] creates a list to store sockets ready for output.
socket_delete={} creates a dictionary to track deleted sockets.
socket_inp={} creates a dictionary to track input from sockets. """

def take_input(c):
    if (socket_del[c] == 0):
        input = c.recv(2048).decode()
        print("C:", c.getpeername(), input)
        socket_inp[c] = input
    else:
        cont = c.recv(2048).decode()
        socket_inp[c] = cont


def send_output(c):
    if (socket_del[c] == 0):
        try:
            inp = socket_inp[c]
        except:
            return
        print("S:", c.getpeername(), inp)
        # get client address
        c.send(inp.encode())
        socket_del[c] = 1
        del socket_inp[c]
    else:
        try:
            cont = socket_inp[c]
        except:
            return
        if (cont == "no"):
            # if not continued
            print("Connect closed: ", c.getpeername())
            socket_list.remove(c)
            c.close()
            #conn closed
            sock_write.remove(c)
        elif (cont == "yes"):
            c.send('yes'.encode())
            socket_del[c] = 0
            del socket_inp[c]


def accept_conn(s):
    c, addr = s.accept()
    c.send('Connection made\nEnter input: '.encode())
    print('Got connection from: ', addr)
    socket_list.append(c)
    sock_write.append(c)
    socket_del[c] = 0


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Socket successfully created: ")
    """ s.bind(('', port)) binds the socket to the specified port. """

    port = 12999
    s.bind(('', port))
    print("socket bound to")
    print(port)
    # Socket is now listening

    s.listen()
    socket_list.append(s)
    print("Listening on socket")
    
    while (1):
        """ read,write,err=select.select(socket_list,sock_write,[],0) selects sockets with input/output operations by looping through them as is needed the op are performed """

        read, write, err = select.select(socket_list, sock_write, [], 0)
        for x in read:
            if (x == s):
                accept_conn(s)
            else:
                take_input(x)
        for x in write:
            send_output(x)


if __name__ == "__main__":
    main()
