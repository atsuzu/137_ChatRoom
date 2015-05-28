from network import Handler, poll
import sys
from threading import Thread
from time import sleep

#Model
class Client(Handler):
    
    def on_close(self):
        pass
    
    def on_msg(self, msg):
        print msg

        
host, port = 'students.ics.uci.edu', 7577
client = Client(host, port)
client.do_send({'join': "Admin"})
#client.on_msg('yes')

def periodic_poll():
    while 1:
        poll()
        sleep(0.05)  # seconds
                            
thread = Thread(target=periodic_poll)
thread.daemon = True  # die when the main thread dies 
thread.start()

v_continue = True

#Controller
while v_continue:
    mytxt = raw_input("Admin " + ' >> ')
    if mytxt == ":q":
        client.do_close()
        v_continue = False
    else:
        client.do_send("Admin" + '|' + mytxt)