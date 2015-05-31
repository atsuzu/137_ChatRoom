from network import Listener, Handler, poll
import Queue

customerList = Queue.Queue()
currentCustomer = None


#------CONTROLLER------
class MyHandler(Handler):
     
    def on_open(self):
        print "Calling Server Open"
        
         
    def on_close(self):
        global currentCustomer
        global customerList
        print "Calling Server Close"
        
        if currentCustomer == self:
            print "NEXT CUSTOMER"
            if customerList.empty():
                currentCustomer = None
            else:
                currentCustomer = customerList.get()    #dequeue, set currentCustomer handler to next Customer in line.
                currentCustomer.do_send("Thank you for waiting, how may I help you?")
     
    def on_msg(self, msg):
        global currentCustomer  #need this global here because python wants to declare local variables even thoug same name or something... ugh
        global customerList
        tempParse = " "
        print "SERVER ON_MSG"    
        if len(handlers) < 1 or parseUser(str(msg)) == "Me":
            print "INSIDE HANDLER ADDER"
            tempParse = parseUser(str(msg))
            if tempParse != "%$$--#":
                # if the "Me" (client) opens, then that handler is put into a Queue
                if tempParse == "Me": 
                    print "ADDED CLIENT"   
                    if currentCustomer == None: 
                        print "FIRST CUSTOMER"
                        currentCustomer = self
                    else:
                        print "CUSTOMER QUEUED"
                        self.do_send("Admin is busy with another customer")                        
                        customerList.put(self)
                # if admin, then he is put into the handlers... 
                else:
                    print "HANDLER INSERT: [" + tempParse + "]"
                    handlers[tempParse] = self
            else:
                tempParse = " "
        elif tempParse == " ":
            strArr = str(msg).split("|", 2)
            print "["+strArr[0]+"]"
            if strArr[0] == "Me" and self == currentCustomer:
                handlers["Admin"].do_send("Customer: "+strArr[1])
            elif strArr[0] == "Admin":
                if currentCustomer != None:
                    currentCustomer.do_send("Admin: "+strArr[1])
                else:
                    handlers["Admin"].do_send("There are no customers!")

    def on_accept(self, msg):
        print "SERVER ON_ACCEPT"
        print msg
        print self

class MyListener(Listener):
    def on_accept(self, h):
        print "MYLISTENER CLASS ON_ACCEPT"
        print h
        print self

def parseUser(msg):
    #print "MSG: " + msg
    if msg.find('join') != -1:
        strArr = msg.split("'")
        return strArr[3]
    else:
        return "%$$--#"
#------MODEL------
handlers = {}  # map client handler to user name
port = 7577
server = MyListener(port, MyHandler)    

#------CONTROLLER------
try:
    while 1:
        poll(timeout=0.1)
except KeyboardInterrupt:
    print "CLOSING"
    handlers["Admin"].do_send("ADMIN IS CLOSING")
    currentCustomer.do_send("ADMIN IS CLOSING")
