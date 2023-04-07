# Import socket module
import socket		
import sys	
def main():
# Create a socket object
    n=len(sys.argv)
    print("Client Program \n")
    if(n!=3):
        print("There should be two arguments: IP address and the Port number separated by spaces.")
        quit()
    
    server_instance = socket.socket(socket.AF_INET, socket.SOCK_STREAM)		

    try: # try catch block to connect and catch exceptions
        server_instance.connect((sys.argv[1], int(sys.argv[2])))
    except ConnectionRefusedError:
        print("Server is busy, try again later.\n")
        quit()
    except:
        print("Invalid IP or Port\n")
        quit()
    while(1):
    # receive data from the server and decoding to get the string.
        
        start_message=server_instance.recv(2048).decode()
        print (start_message)
        expr=input()
        server_instance.send(expr.encode())
        print("Server Response: ",server_instance.recv(2048).decode())
        flag = 1
        while(flag):
            #while not exited flag is 1
            print("Take another question ?(yes / no)")
            repeat=input()
            if(repeat=="yes"):
                server_instance.send(repeat.encode())
                break
            elif(repeat=="no"):
                # close down the server
                server_instance.send(repeat.encode())
                server_instance.shutdown(2)
                server_instance.close()
                flag = 0
            else:
                "Answer yes / no only"

if __name__ == "__main__":
    main()
	
