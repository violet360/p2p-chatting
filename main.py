import os, socket,sys, time
from threading import Thread


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
            recv_message = self.shout.recv(1024)              

            recv_string_message = str(recv_message.decode('utf-8'))

            if recv_string_message.find(':') != -1:
            

                print(recv_string_message)      

            elif recv_string_message.find('!@#') != -1 and recv_string_message.find(':') == -1 and recv_string_message[3:] in self.online_num:

                self.online_num.remove(recv_string_message[3:])     

                print('currently online>> ' + str(len(self.online_num)))  

            elif not(recv_string_message in self.online_num) and recv_string_message.find(':') == -1:


                self.online_num.append(recv_string_message)         

                lis.append(self.shout)
                print('currently online>> ' + str(len(self.online_num)))  



# to broadcast packets

    def send(self):

        self.send_sock.setblocking(False)           

        while True: 
            data = input()                            

            if data == 'exit()':               
           

                exit_msg = '!@#' + self.name   

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

        recvThread = Thread(target=self.get)               


        sendMsgThread = Thread(target=self.send)                                        


        sendOnlineThread = Thread(target=self.shout_status)


        recvThread.start()                                          

        sendMsgThread.start()                                       

        sendOnlineThread.start()                                   


        recvThread.join()                                           

        sendMsgThread.join()                                       

        sendOnlineThread.join()




c = converse()
c.start()



