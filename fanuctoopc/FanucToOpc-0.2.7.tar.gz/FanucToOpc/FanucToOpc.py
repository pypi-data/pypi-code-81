#fanuc-opcua library
from opcua import Client
def connect(url):
    '''
    Creates connection with the opc client.
    Takes one argument: the url in the form "opc.tcp:// IP Adress :4880/FANUC/NanoUaServer"
    returns the client or an error

    If it is not possible to create a connection,
    this function will terminate the program.   
    '''
    print('connecting to ',url)
    client = Client(url)
    connected = False
    while connected == False:
        try:
            client.connect()
            print('client Connected')
            connected = True
            return client, connected
        except ConnectionRefusedError:
            print('connection refused')
            #print('exiting program')
            return None, connected
            break
            #sys.exit(0)
        except TimeoutError:
            print('connection timed out')
            #print('exiting program')
            return None, connected
            break
            #sys.exit(0)
def get_reg_state(regnum, node, client): #maybe make client and logfilepath a global var?
    '''
    This function returns the value of one or more registers.
    It takes 3 arguments:
    regnum: the number of the register it returns (can be list, string or integer)
    node: the addres at which the registers are stored
    client: the connection with the server (predifiend)

    Returns int or string (if int is given) or list if list is given
    '''  
    Register = client.get_node(node)
    if type(regnum)==list:
        regvalue=[]
        for i in range(len(regnum)):
            regvalue.append((Register.get_value())[int(regnum[i])-1])
            
    elif type(regnum)==int:
        regvalue=Register.get_value()[regnum-1]

    return regvalue
def update_reg_state(regnum, node, newVal,client,logfilepath):
    '''
    Updates one register (and automatically creates a log)
    Takes 5 arguments;
    Regnum: the registernumber you want to change
    Node: the addres the registers are stored
    newVal: The new value of the register
    client: the connection with the server (predifiend)
    logfilepath: path to store the logfile
    '''
    Register = client.get_node(node)
    register = Register.get_value()
    register[regnum-1] = newVal
    Register.set_data_value(register, varianttype=Register.get_data_type_as_variant_type())