import os

from doipclient import DoIPClient
import binascii

# coding=utf8

mask=0x91587a05 # xxx Level1
# mask = 0xf042848c # xxx level2
# mask=0x9F034366 # xxx Level3

def SeedToKey(Seed_, Mask_):
    key = 0
    print("Seed is ",hex(Seed_))
    if (Seed_ != 0):
        for i in range(35):
            if (Seed_ & 0x80000000):
                Seed_ = Seed_ << 1
                Seed_ = Seed_ & 0xFFFFFFFF
                Seed_ = Seed_ ^ Mask_
            else:
                Seed_ = Seed_ << 1
        key = Seed_
    print("key  is ",hex(key))
    return key

def enterDefaultSession(doip_client):
        #进默认会话
        print('session control send ', doip_client.send_diagnostic(b'\x10\x01'))
        print('session control recv ', doip_client.receive_diagnostic())

def enterExtendSession(doip_client):
        #进拓展会话
        doip_client.send_diagnostic(b'\x10\x03')
        print('extend session control send ',(b'\x10\x03'))
        print('extend session control recv ', doip_client.receive_diagnostic())

def unlock_SecurityAccess(doip_client):
    doip_client.send_diagnostic(b'\x27\x01')
    print('unlock_SecurityAccess send ',(b'\x27\x01'))
    seed = doip_client.receive_diagnostic()
    print('unlock_SecurityAccess recv ', seed)
    seed = seed[2:]
    key = SeedToKey(int.from_bytes(seed,'big'),mask)
    request = bytearray(b'\x27\x02')
    request.extend(key.to_bytes(4,'big'))
    #doip_client.send_diagnostic(b'\x27\x12\xc4\x4e\xeb\xe8')
    doip_client.send_diagnostic(request)
    print('unlock_SecurityAccess send ',request)
    print('unlock_SecurityAccess recv ', doip_client.receive_diagnostic())


def readMcuConfiguration(doip_client_mcu):
    data = bytearray(b'\x22\xF0\x11') # 立时读did
    doip_client_mcu.send_diagnostic(data)
    print('读取 did '+'0xF0111 '+'xxx MCU configuration: ',str(binascii.hexlify((data))))
    response = doip_client_mcu.receive_diagnostic()
    print('获得 did '+'0xF011'+'xxx MCU configuration:', response) # str(binascii.hexlify((response)))

def mainWork():
    # 目标IP地址
    target_ecu_ip = '172.16.12.xxx'
    # 目标逻辑地址
    target_ecu_logical_address = 0x40 # for xxx MCU
    # ecu_logical_address = 0x41 # for xxx MPU

    source_client_logical_address = 0xF00 # 0x0E80
    doip_client_mcu = DoIPClient(target_ecu_ip, target_ecu_logical_address, protocol_version=0x03, client_logical_address=source_client_logical_address)

    readMcuConfiguration(doip_client_mcu)


if __name__ =='__main__':
    mainWork()
    os.system("pause")

