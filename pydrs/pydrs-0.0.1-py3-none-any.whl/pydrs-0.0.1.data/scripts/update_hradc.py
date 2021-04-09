import pydrs
import time
import struct

hradcVariant = ['HRADC-FBP','HRADC-FAX-A','HRADC-FAX-B','HRADC-FAX-C','HRADC-FAX-D']

def check_hradc_boarddata(drs,hradc_id):
    print('\n######################################################################')
    print('\nConfigurando placa ' + str(hradc_id+1) + ' em UFM mode...')
    print(drs.ConfigHRADCOpMode(hradc_id,1))
    time.sleep(0.5)

    print('\nExtraindo dados da placa...')
    payload_size   = drs.size_to_hex(1+2) #Payload: ID + hradcID
    hex_hradcID    = drs.double_to_hex(hradc_id)
    send_packet    = drs.ComFunction+payload_size+drs.index_to_hex(31)+hex_hradcID
    send_msg       = drs.checksum(drs.SlaveAdd+send_packet)
    drs.ser.write(send_msg.encode('ISO-8859-1'))
    print(drs.ser.read(6))

    print('\nLendo dados da placa...')
    drs.read_var(drs.index_to_hex(50+hradc_id))
    reply_msg = drs.ser.read(1+1+2+56+1)
    print(reply_msg)
    print(len(reply_msg))
    val = struct.unpack('BBHLLHHHHHHfffffffffB',reply_msg)
    print(val)
    
    try:
        boardData = drs.InitHRADC_BoardData(val[3]+val[4]*pow(2,32),val[5],
                                            val[6],val[7],val[8],val[9],
                                            hradcVariant[val[10]],val[11],
                                            val[12],val[13],val[14],val[15],
                                            val[16],val[17],val[18],val[19])

        print('\n###############################')
        print('### Placa ' + str(hradc_id + 1) + ' ja possui dados ###')
        print('###############################')
    
        print('\nColocando a placa em Sampling mode...')
        print(drs.ConfigHRADCOpMode(hradc_id,0))    
        time.sleep(0.5)
        
        return True
    except:
        print('\n#########################')
        print('### Placa ' + str(hradc_id + 1) + ' sem dados ###')
        print('#########################')
               
        print('\nColocando a placa em Sampling mode...')
        print(drs.ConfigHRADCOpMode(hradc_id,0))
        time.sleep(0.5)
        
        return False

def update_hradc_boarddata(drs,hradc_id,board_data):

    drs.ConfigHRADCOpMode(hradc_id,1)
    time.sleep(0.1)
    drs.EraseHRADC_UFM(hradc_id)
    time.sleep(0.5)
    drs.ResetHRADCBoards(1)
    time.sleep(0.5)
    drs.ResetHRADCBoards(0)
    time.sleep(1.5)
    drs.WriteHRADC_BoardData(hradc_id,board_data)
    
drs = pydrs.SerialDRS()

comport = input('\nDigite a porta serial utilizada: ')

drs.Connect(comport,115200)

n_hradc = int(input('\nDigite o numero de placas HRADC deste bastidor: '))

print('Configurando numero de placas HRADC ...')
drs.Config_nHRADC(n_hradc)

for hradc_id in range(n_hradc):
    if not check_hradc_boarddata(drs,hradc_id):
    
        board_data = drs.InitHRADC_BoardData(serial = 1234567890, day = 27, mon = 9,
                            year = 2019, hour = 4, minutes = 20,
                            variant = 'HRADC-FBP', rburden = 20, calibtemp = 40,
                            vin_gain = 1, vin_offset = 0, iin_gain = 1,
                            iin_offset = 0, vref_p = 5, vref_n = -5, gnd = 0)
    
        update_hradc_boarddata(drs,hradc_id,board_data)
        