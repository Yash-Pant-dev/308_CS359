import socket			
import select 
# import the select function
socket_list=[]
sock_write=[]
socket_operation={}
socket_inp={}

""" socket_list=[] creates a list to store connected sockets.
sock_write=[] creates a list to store sockets ready for output.
socket_delete={} creates a dictionary to track deleted sockets.
socket_inp={} creates a dictionary to track input from sockets. """

def get_input(c):
    if(socket_operation[c]==0):
        input=c.recv(2048).decode()
        print("C",c.getpeername(),input)
        socket_inp[c]=input
    else:
        cont=c.recv(2048).decode()
        socket_inp[c]=cont
        
def send_output(c):
    if(socket_operation[c]==0):
        try:
            inp=socket_inp[c]
        except:
            return
        try:
            ans=str(eval(inp))
        except:
            ans="Input is invalid"
        print("S:",c.getpeername(),ans)
        # get client address
        c.send(ans.encode())
        socket_operation[c]=1
        del socket_inp[c]
    else:
        try:
            cont=socket_inp[c]
        except:
            return
        if(cont=="no"):
            # if not continued
            print("Connection closed.", c.getpeername())
            socket_list.remove(c)
            c.close()
            sock_write.remove(c)
        elif(cont=="yes"):
            c.send('Now Connected\nEnter input: '.encode())
            socket_operation[c]=0
            del socket_inp[c]
def take_conn(s):
    c,addr=s.accept()
    c.send('Connection made\nEnter input: '.encode())
    print ('Got connection from', addr )
    socket_list.append(c)
    sock_write.append(c)
    # writing on socket
    socket_operation[c]=0
def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)		
    print ("Socket created")
    port = 12999	
    s.bind(('', port))		
    # Socket is now listening

    print("Opened to port:")
    print(int(port))

    s.listen()
    socket_list.append(s)
    print("Listening to socket: ")
    while(True):
        """ read,write,err=select.select(socket_list,sock_write,[],0) selects sockets with input/output operations by looping through them as is needed the op are performed """
       
        read,write,err=select.select(socket_list,sock_write,[],0)
        for x in read:
            if(x==s):
                take_conn(s)
            else:
                get_input(x)
        for x in write:
            send_output(x)
            
                
                

                
if __name__ == "__main__":
    main()
