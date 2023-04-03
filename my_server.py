from concurrent.futures import thread
from email.base64mime import header_length
from http import client
from re import A
import socket
import sys
from threading import Thread
import threading
import time
from matplotlib import use



class server:
    host=""  
    port=""
    clients_list_recieve={}
    clients_list_send={}

    def __init__(self,host,port):
        self.host=host
        self.port=port

    def to_listen(self,client_socket,client_address):
        try:
#            print("got connection request")
            data = client_socket.recv(2048)
            if not data:
                print("Error")
            else:
                data=data.decode("utf-8").split('||')
#                print(data)
                type=int(data[0])
#                print(type)
                if type==1:                  #Register Tosend
                    username=data[2]
                    if username in self.clients_list_send:
                        ack = "7" + "||" + "Error 105 : User name already taken. Please choose a different username."
                        ack = ack.encode()
                        client_socket.send(ack)
                    else:
                        if username.isalnum():
                            self.clients_list_send[username]=client_socket
                            print("Registered with name : {} to send message".format(username))
                            ack = "6" + "||" + "registered"
                            ack = ack.encode()
                            client_socket.send(ack)
                        else:
                            ack = "7" + "||" + "Error 100: Username can only be alpha-numeric."
                            ack = ack.encode()
                            client_socket.send(ack)                            

                    
                if type==2:               #Register Torecieve                   
                    username=data[2]
#                    print(username)
                    if username in self.clients_list_recieve:
                        ack = "7" + "||" + "Error 105 : User name already taken. Please choose a different username."
                        ack = ack.encode()
                        client_socket.send(ack)
                    else:
                        if username.isalnum():
                            self.clients_list_recieve[username] = client_socket
                            print("Registered with name: {} to receive message".format(username))
                            ack = "6" + "||" + "registered"
                            ack = ack.encode()
                            client_socket.send(ack)
                        else:
                            ack = "7" + "||" + "Error 100: Username can only be alpha-numeric."
                            ack = ack.encode()
                            client_socket.send(ack) 
                
                if type==3:      #to send message from one user to another
                    if not len(data)== 5:
                            ack = "7" + "||" + "Error 109: header incomplete."
                            ack = ack.encode()
                            client_socket.send(ack)
                            client_socket.close()
                    
                    sendername=data[2]
                    receivername=data[3]
                    
                    if sendername not in self.clients_list_send or receivername not in self.clients_list_recieve:
                        ack = "7" + "||" + "Error 101 : User not registered Please register first."
                        ack = ack.encode()
                        client_socket.send(ack)

                    print(data[4])
                    message = data[4].split()
                    
                    final = ' '.join(message[1:])
                    
                    receiversocket= self.clients_list_recieve[receivername]
#                    print(receiversocket)
                    message = "3"+"||"+sendername + "||" + final
                    receiversocket.send(message.encode())


                
                if type == 4:             #broadcast message
                    sendername = data[2]
                    if sendername not in self.clients_list_send:
                        ack = "7" + "||" + "Error 101 : User not registered Please register first."
                        ack = ack.encode()
                        client_socket.send(ack)
                    message = data[4].split()
                    final = ' '.join(message[1:])                       
                    message = "4"+"||"+sendername + "||" + final
                    message= message.encode()

                    for i in self.clients_list_recieve:
                        if i == sendername:
                            continue
                        self.clients_list_recieve[i].send(message)
                
                if type == 5:
                    username = data[1]
                    del self.clients_list_recieve[username]
                    del self.clients_list_send[username]
                    print("Remove user {}".format(username))
                    
            return True
        except:
            client_socket.close()
            return False
        



    def start_server(self):
        chat_server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        chat_server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR, 1)
        chat_server.bind((self.host,int(self.port)))
        chat_server.listen()
        print("Started server.")
        while True:
            client_socket , client_address = chat_server.accept()
#            client_socket.settimeout(60)
            threading.Thread(target=self.to_listen,args=(client_socket,client_address)).start()
        
def main():
    host = sys.argv[1]
    port = sys.argv[2]

    st = server(host,port)
    st.start_server()


main()