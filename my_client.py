from multiprocessing.spawn import import_main_path


from concurrent.futures import thread
from email.base64mime import header_length
from http import client
import socket
import sys
from threading import Thread
import threading



class client:


    def to_recieve(self,serv_ip,serv_port,username):
#        print("starting registration to recieve.")

        header_length = 7 + len(username)
        message = "2"+ "||"  + str(header_length) + "||" + username
        message = message.encode('utf-8')

        server_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#        print("message sent")
        server_socket.connect((serv_ip,serv_port))
        server_socket.send(message)
        
        
#        print("waiting")
        ack=server_socket.recv(2048)
        ack=ack.decode('utf-8')
        ack= ack.split('||')
        if int(ack[0])==6:
            print("\n")
            print("Registered to recieve succefully")
        else:
            print(ack[1])
            sys.exit()
        
        while True:
            message=server_socket.recv(2048)
            message=message.decode('utf-8')
            if message == "":
                sys.exit()
            message = message.split('||')
            if (int(message[0])==4):
                print("It is a broadcasted message.")

            print("\n")
            print("{} :> {}".format(message[1],message[2])) 
            


    def to_send(self,serv_ip,serv_port,username):
#        print("starting registration to send.") 
        header_length = 7 + len(username)
        message = "1"+ "||" + str(header_length) + "||" + username
        message = message.encode()

        server_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        server_socket.connect((serv_ip,serv_port))
        server_socket.send(message)
        
        while True:
            ack=server_socket.recv(2048)
            ack=ack.decode('utf-8')
            ack = ack.split('||')
            
            if int(ack[0])==6:
                print("\n")
                print("Registered to send succefully")
                break
            else:
                print(ack[1])
                sys.exit()
                
        while True:
            message = input("{} :> ".format(username))
            if message == "quit":
                message = "5" + "||" + username + "||" + "End connection" 
                message = message.encode()
                self.send_message(message,serv_ip,serv_port) 
                sys.exit()
            
            if message == "" or message == "\n":
                continue   
            
            if not message[0]=='@':
                print("Please mention reciever's Name.")
                continue
            
            reciever_name= message.split()[0][1:]

            header_length = 1 + len(username) + len(reciever_name) + 2 + 2
            if reciever_name == "all":
                message = "4" + "||" + str(header_length) + "||" + username + "||" + reciever_name + "||" + message 
            else:
                message = "3" + "||" + str(header_length) + "||" + username + "||" + reciever_name + "||" + message 
            message=message.encode()
            self.send_message(message,serv_ip,serv_port)           
    
    def send_message(self,message,serv_ip,serv_port):
        server_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        server_socket.connect((serv_ip,serv_port))
        server_socket.send(message)


    def start_client(self,serv_ip,serv_port):
        print("Starting client")            
        
        username = input("Enter your username: ")
        if not username.isalnum():                
            print("You can only use alpha-numeric user name.")
        threading.Thread(target=self.to_recieve,args=(serv_ip,serv_port,username)).start()
        threading.Thread(target=self.to_send,args=(serv_ip,serv_port,username)).start()

            

def main():
    serv_ip = input("Enter serverip to connect with: ")
    serv_port = input("Enter server port to connect with: ")


    st = client()
    st.start_client(serv_ip,int(serv_port))

main()
