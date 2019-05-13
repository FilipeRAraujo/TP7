from psutil import net_if_addrs, net_io_counters, Process
from netifaces import AF_INET, gateways
import json

def checar_Adaptador(adapt):
    interface = net_io_counters(pernic=True)
    for key in adapt.items():
        if key[0] == 'Wi-Fi' or key[0] == 'Wi-Fi 2' or key[0] == 'Wi-Fi 3':
            if interface[key[0]].bytes_sent != 0:
                bob = adapt[key[0]][1].address, adapt[key[0]][1].netmask, key[0], interface[key[0]]
        if key[0] == 'Ethernet' or key[0] == 'Ethernet 2' or key[0] == 'Ethernet 3':
            if interface[key[0]].bytes_sent != 0:
                bob = adapt[key[0]][1].address, adapt[key[0]][1].netmask, key[0], interface[key[0]]
    return bob

def Gerar_Dicionario(ip, mask, gateway, adapt, sent, received, packet_send, packet_received):
    dictionary = {}
    dictionary[adapt] = {'ip': ip, 'mask': mask, 'gateway': gateway, 'sent': sent, 'received': received, 'packet_send': packet_send, 'packet_received': packet_received}
    return dictionary

def Obter_Gateway(list):
    return list['default'][AF_INET][0]

def gerar_processo(PID):
    process = Process(PID)
    conn = process.connections()
    return json.dumps(conn)

def Exec():
    PID = int(input('Entre com o PID: '))
    process_result = gerar_processo(PID)
    ip, mascara, adaptador, interface = checar_Adaptador(net_if_addrs())
    gateway = Obter_Gateway(gateways())
    resultado = Gerar_Dicionario(ip, mascara, gateway, adaptador, interface.bytes_sent, interface.bytes_recv, interface.packets_sent, interface.packets_recv)
    print(resultado)
    print(process_result)
Exec()