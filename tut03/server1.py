import socket			

def main():
    
    while True:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)		
        print ("Socket successfully created")
        port = 12999	
        s.bind(('', port))	
        # s.bind() binds the socket to the specified port.	
        print ("socket binded to %s" %(port))
        s.listen(0)
        print("Socket is listening..")
        # socket starts listening
        c, addr = s.accept()
        print ('Got connection from', addr )
        s.close()
        while(True):	
            # establish the coonnnection
            c.send('Connection established.\nProvide your input: '.encode())
            input=c.recv(2048).decode()
            print("C: ",input)
            # print clients input 
            try:
                ans=str(eval(input))
            except:
                ans="Invalid input format"
            print("Response: ",ans)
            # c.send() sends a message to the connected client.
            c.send(ans.encode())
            cont=c.recv(2048).decode()
            # receive 2048 bytes of data, any extra is truncated for this query
            # if no continuation
            if(cont=="no"):
                print("Connection closed.", addr)
                c.close()
                break

if __name__ == "__main__":
    main()
