import os, socket,sys, time
from threading import Thread
import hashlib


class converse():

#constructor to init common vars
    def __init__(self):
        self.shout = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)     
        self.shout.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)   
        self.shout.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)   
        self.shout.bind(('0.0.0.0', 8080))
        self.send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)           
        self.send_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST,1)
        self.name = ''
        self.online_num = []  
        self.identity = hashlib.sha224(("i am out, need some air").encode('utf-8')).hexdigest()
        self.identity_size = len(self.identity)



# getting started.....

    def initialise(self):
        while True:                                                 
            self.name = input('your name>> ')

            if not self.name:
                print('Enter a non-empty name!')

            else:
                break



#to catch the broadacasted packets

    def get(self):
        lis = []
        while True:
            recvd_msg = self.shout.recv(1024)              

            recvd_str_msg = str(recvd_msg.decode('utf-8'))

            if recvd_str_msg.find(':') != -1:
                print(recvd_str_msg)      

            elif recvd_str_msg.find(self.identity) != -1 and recvd_str_msg.find(':') == -1 and recvd_str_msg[self.identity_size:] in self.online_num:

                self.online_num.remove(recvd_str_msg[self.identity_size:])     

                print('currently online>> ' + str(len(self.online_num)))  

            elif not(recvd_str_msg in self.online_num) and recvd_str_msg.find(':') == -1:


                self.online_num.append(recvd_str_msg)         

                lis.append(self.shout)
                print('currently online>> ' + str(len(self.online_num)))  



# to broadcast packets

    def send(self):

        self.send_sock.setblocking(False)           

        while True: 
            data = input()                            

            if data == 'exit()':               
           

                exit_msg = self.identity + self.name   

                self.send_sock.sendto(exit_msg.encode('utf-8'), ('255.255.255.255', 8080))


                os._exit(1)                     

            elif data != '' and data != 'exit()':
           

                send_msg = self.name + ': ' + data   

                self.send_sock.sendto(send_msg.encode('utf-8'), ('255.255.255.255', 8080))  

            
            else:

                print('write the message first!')        



    def shout_status(self):

        self.send_sock.setblocking(False)           

        while True:                             

            time.sleep(1)                       

            self.send_sock.sendto(self.name.encode('utf-8'), ('255.255.255.255', 8080))


#to run everything together in sync...using multithreading...and here we go!!

    def start(self):

        self.initialise()

        Thread1 = Thread(target=self.get)               

        Thread2 = Thread(target=self.shout_status)

        Thread3 = Thread(target=self.send)                                        


        Thread1.start()                                          

        Thread2.start()                                       

        Thread3.start()                                   


        Thread1.join()                                           

        Thread2.join()                                       

        Thread3.join()




c = converse()
c.start()






