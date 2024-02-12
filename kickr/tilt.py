import asyncio

import bleak
from bleak.backends.characteristic import BleakGATTCharacteristic

from convert import ToHex

import kickr.uuids

async def read_tests(client):
    print('TILT TESTS:')
    await write_tilt(client, '01')
    await write_tilt(client, '03')
    await write_tilt(client, '0B')
    await write_tilt(client, '0C')
    await write_tilt(client, '32')
    await write_tilt(client, '33')
    await write_tilt(client, '5D')
    await write_tilt(client, '5E')
    await write_tilt(client, '65')
    await write_tilt(client, '67', 'Read Tilt Lock')
    await write_tilt(client, '68', 'Read Tilt Angle')
    await write_tilt(client, '69', 'Read Tilt Angle Limits')
    await write_tilt(client, '6A 00 00')
    await write_tilt(client, '6B')
    print

async def write_tilt(client, hex, comment=None):
    data = bytearray.fromhex(hex)
    s = f'write_tilt({ToHex(data)})'
    print(f'{s:<32}' + ('Unknown' if(comment==None) else comment))
    await client.write_gatt_char(kickr.uuids.kickr_tilt_characteristic, data, response=False)
    await asyncio.sleep(0.5)

async def start_notify(client):
    await client.start_notify(kickr.uuids.kickr_tilt_characteristic, tilt_handler)

async def stop_notify(client):
    await client.stop_notify(kickr.uuids.kickr_tilt_characteristic)

def tilt_handler(characteristic: BleakGATTCharacteristic, data: bytearray):
    print(f'Tilt:   {ToHex(data):<23} {decode_tilt(data)}')
    print()

def decode_tilt(data):
    #print(f'decode_tilt( {ToHex(data)} )')

    if(len(data)==6 and data[0]==0x0D):
        PowerCycles = unsigned_16(data[4], data[5])
        return f'Power cycles = {PowerCycles}'

    if(data[0]==0xFD or data[0]==0xFE):

        # Lock status
        if(len(data)==3 and data[1]==0x33):
            locked:bool = (data[2] & 0x01) == 0x01
            return f'Locked={locked}'
        
        # Tilt Angle
        if(len(data)==4 and data[1]==0x34):
            # signedint = sign_extend(data[2] | data[3] << 8, 16)
            # print(f'signedint={signedint}')
            # angle = signedint / 100
            angle = bytes_to_tilt(data[2], data[3])
            return f'Tilt angle = {angle}°'

        if(len(data)==4 and data[1]==0x67):
            locked = (data[3] & 0x01) == 0x01
            return f'Locked = {locked}'

        if(len(data)==5 and data[1]==0x68):
            angle = bytes_to_tilt(data[3], data[4])
            return f'Tilt angle = {angle}°'
        
        if(len(data)==7 and data[1]==0x69):
            angle_min = bytes_to_tilt(data[3], data[4])
            angle_max = bytes_to_tilt(data[5], data[6])
            return f'Tilt angle range = {angle_min}° -> {angle_max}°'

    return f'Unknown tilt data'

def bytes_to_tilt(b1, b2):
            signedint = sign_extend(b1 | b2 << 8, 16)
            #print(f'signedint={signedint}')
            angle = signedint / 100
            return angle

def unsigned_16(b1, b2):
    return b1 | b2 << 8

def sign_extend(value, bits):
    sign_bit = 1 << (bits - 1)
    return (value & (sign_bit - 1)) - (value & sign_bit)


#print(f'Tilt first read: {decode_tilt(await client.read_gatt_char(kickr_tilt_characteristic))}')
