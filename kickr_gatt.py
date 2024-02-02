import asyncio
import bleak
from bleak import BleakClient
from bleak import BleakScanner
from bleak.backends.characteristic import BleakGATTCharacteristic

#device_name = 'Train.Red FYER 0220'

device_name = 'KICKR BIKE 69A8'

kickr_virtual_bike_svc          = 'a026ee0d-0a7d-4ab3-97fa-f1500f9feb8b'
kickr_buttons                   = 'a026e03c-0a7d-4ab3-97fa-f1500f9feb8b'
kickr_chosen_gear               = 'a026e03a-0a7d-4ab3-97fa-f1500f9feb8b'
kickr_groupset                  = 'a026e039-0a7d-4ab3-97fa-f1500f9feb8b'

kickr_cycling_power_extension   = 'a026e005-0a7d-4ab3-97fa-f1500f9feb8b'

kickr_tilt_svc                  = 'a026ee0b-0a7d-4ab3-97fa-f1500f9feb8b'
kickr_tilt_characteristic       = 'a026e037-0a7d-4ab3-97fa-f1500f9feb8b'

def register_kickr_uuids():
    bleak.uuids.register_uuids({
        kickr_virtual_bike_svc: '### KICKR Virtual Bike',
        kickr_buttons:      '### KICKR Buttons', 
        kickr_chosen_gear:  '### KICKR Chosen Gear', 
        kickr_groupset:     '### KICKR Groupset',
        kickr_cycling_power_extension: '### KICKR Cycling Power Extension',
        kickr_tilt_svc: '### KICKR Tilt Service',
        kickr_tilt_characteristic: '### KICKR Tilt Characteristic'
    })

def enumerate_services(client:BleakClient):
        for handle in client.services.services:
            svc = client.services.services[handle]
            print(f"{handle}        {svc.uuid}  {' '*44}  {svc.description}")

            for char in svc.characteristics:
                # s = f"{char.properties}"
                print(f"   {char.handle}     {char.uuid}  {f'{char.properties}':<44}  {char.description}")

                for des in char.descriptors:
                    print(f"      {des.handle}  {des.uuid}  {' '*44}  {des.description.replace('Client Characteristic Configuration','CCCD')}")

            print()

async def main():
    register_kickr_uuids()

    print("Scanning for device...")
    bledevice = await BleakScanner.find_device_by_name(device_name)

    if bledevice == None: 
        print("Device not found")
        exit()

    print("Connecting to device...")
    client = BleakClient(bledevice)
    try:
        await client.connect()

        if(client.is_connected):
            print(f"Connected to {device_name} with address {client.address}")
        else:
            return
        
        #enumerate_services(client)

        # print("read_gatt_char('00002a29-0000-1000-8000-00805f9b34fb'):")
        # try:
        #     manufacturer_name = await client.read_gatt_char('00002a29-0000-1000-8000-00805f9b34fb')
        #     print(f"  {bytesToString(manufacturer_name)}")
        # except Exception as e:
        #     print(f"  {e}")

        print(f'Tilt first read: {decode_tilt(await client.read_gatt_char(kickr_tilt_characteristic))}')

        # await client.start_notify(kickr_chosen_gear, chosen_gear_handler)
        await client.start_notify(kickr_tilt_characteristic, tilt_handler)

        while(True):
            await asyncio.sleep(1)
            print('Read Tilt Lock...')
            await client.write_gatt_char(kickr_tilt_characteristic, bytearray.fromhex('67'), response=False)
            await asyncio.sleep(1)
            print('Read Tilt Angle...')
            await client.write_gatt_char(kickr_tilt_characteristic, bytearray.fromhex('68'), response=False)
            await asyncio.sleep(1)
            print('Read Tilt Angle Limits...')
            await client.write_gatt_char(kickr_tilt_characteristic, bytearray.fromhex('69'), response=False)
            await asyncio.sleep(1)
            print('Write Tilt Angle...')
            await client.write_gatt_char(kickr_tilt_characteristic, bytearray.fromhex('68 00 03'), response=False)
            await asyncio.sleep(10)

        # await client.stop_notify(kickr_chosen_gear)
        await client.stop_notify(kickr_tilt_characteristic)

    finally:
        await client.disconnect()

def sign_extend(value, bits):
    sign_bit = 1 << (bits - 1)
    return (value & (sign_bit - 1)) - (value & sign_bit)

def chosen_gear_handler(characteristic: BleakGATTCharacteristic, data: bytearray):
    print(f'Chosen Gear: {ToHex(data)}')

def tilt_handler(characteristic: BleakGATTCharacteristic, data: bytearray):
    print(f'Tilt:        {decode_tilt(data)}')

def bytes_to_tilt(b1, b2):
            signedint = sign_extend(b1 | b2 << 8, 16)
            #print(f'signedint={signedint}')
            angle = signedint / 100
            return angle

def decode_tilt(data):
    if(data[0]==0xFD or data[0]==0xFE):
        # Lock status
        if(len(data)==3 and data[1]==0x33):
            locked:bool = (data[2] & 0x01) == 0x01
            return f'Locked={locked} {ToHex(data)}'
        
        # Tilt Angle
        if(len(data)==4 and data[1]==0x34):
            # signedint = sign_extend(data[2] | data[3] << 8, 16)
            # print(f'signedint={signedint}')
            # angle = signedint / 100
            angle = bytes_to_tilt(data[2], data[3])
            return f'tilt angle={angle}°'

        if(len(data)==4 and data[1]==0x67):
            locked = (data[3] & 0x01) == 0x01
            return f'Locked = {locked} {ToHex(data)}'

        if(len(data)==5 and data[1]==0x68):
            angle = bytes_to_tilt(data[3], data[4])
            return f'tilt angle = {angle}°'
        
        if(len(data)==7 and data[1]==0x69):
            angle_max = bytes_to_tilt(data[3], data[4])
            angle_min = bytes_to_tilt(data[5], data[6])
            return f'tilt angle range = {angle_min} -> {angle_max}°'

    return f'unknown tilt data: {ToHex(data)}'

def bytesToString(bytes): 
    return "".join(map(chr, bytes))

def ToHex(data):
    # return '[{}]'.format(' '.join(f"{x:02x}" for x in data))
    # return f'[{" ".join(f"{x:02x}" for x in data)}]'
    # return f'[{" ".join(map(lambda x: f"{x:02x}", data))}]'
    return f'[{" ".join(map("{:02x}".format, data))}]'

asyncio.run(main())

bytes=b'hello'
print(ToHex(bytes))
