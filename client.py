from network import Handler, poll
import sys
from threading import Thread
from time import sleep

import webbrowser
new = 2 # open in a new tab, if possible

# open a public URL, in this case, the webbrowser docs
url = "http://www.youtube.com/watch?v=xGgk1sYY3GI"


#View
def beep():
    print "\a"
def getInput():
    mytemptxt = raw_input()
    return mytemptxt
def print_msg(msg):
    if str(msg) == "ADMIN IS CLOSING":
        client.do_close()
        global v_continue
        v_continue = False
    print msg
    global stringSoFar
    stringSoFar = stringSoFar + str(msg) + "\n"

#Controller
class Client(Handler):
    def on_close(self):
        #pass
        print "Client Closing..."

    def on_msg(self, msg):
        if str(msg) == "close":
            client.do_close()
        print_msg(msg)
def periodic_poll():
    while 1:
        poll()
        sleep(0.05)  # seconds
def parseSubject():
    if len(topic2)>20:
        topic2[:20]
    topic2.replace(" ", "_")

def main_funct():
    v_continue = True 
    while v_continue:
        mytxt = getInput()
        if mytxt == ":q":
            client.do_close()
            v_continue = False
        elif mytxt == ":e":
            beep()
            global webbrowser, new
            webbrowser.open(url,new=new)
        elif mytxt == ":s":
            file_wr = open(topic2+".txt", 'w+')
            file_wr.write(stringSoFar)
            file_wr.close()
        else:
            client.do_send("Me" + '|' + mytxt)
            global stringSoFar
            stringSoFar = "Me: " + stringSoFar + mytxt+ "\n"


#Model
                           
thread = Thread(target=periodic_poll)
thread.daemon = True  # die when the main thread dies 
thread.start()
topic1 = raw_input("Please select your topic\n 1: Feedback\t2: Complaint\t3: Misc\n")
topic2 = raw_input("What is the name of the topic? (20 character limit): ")
#host, port = 'students.ics.uci.edu', 7577
host, port = 'localhost', 7577
client = Client(host, port)
client.do_send({'join': "Me"})
client.do_send("Me|TOPIC: ("+topic1 +") "+topic2 )
stringSoFar = ""
#client.on_msg('yes')
parseSubject()
main_funct()







