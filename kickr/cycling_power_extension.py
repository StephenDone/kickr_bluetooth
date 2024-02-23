from enum import IntFlag, IntEnum

import asyncio

from bleak.backends.characteristic import BleakGATTCharacteristic

from convert import ToHex

import kickr.uuids

async def start_notify(client):
    await client.start_notify(kickr.uuids.kickr_cycling_power_extension, power_extension_handler)

async def stop_notify(client):
    await client.stop_notify(kickr.uuids.kickr_cycling_power_extension)

async def power_extension_tests(client):
    print('POWER EXTENSION TESTS')
    await write_power_extension(client, '09 ec fc')
    await write_power_extension(client, '0a ec fc')
    await write_power_extension(client, '54 01 00', 'Cadence from ANT+ - off')
    await write_power_extension(client, '54 02 00', 'Control with ANT+ Power Meter- off')
    await write_power_extension(client, '54 03 01', 'Erg Mode Speed Simulation - on')
    await write_power_extension(client, '54 06 00', 'Erg Mode Power Smoothing - off')
    await write_power_extension(client, '41 05', 'Level - 5')
    await write_power_extension(client, '42 64 00', 'Erg Mode - 100 Watts')
    await write_power_extension(client, '43 34 21 28 00 58 02', 'Sim Mode - 86kg / CRR 0.04 / Drag 0.6')
    await write_power_extension(client, '44 21 00', 'CRR 0.033')
    await write_power_extension(client, '45 a0 01', 'Drag 0.416')
    await write_power_extension(client, '46 5c 7f', 'Set Slope - 0.5%')
    await write_power_extension(client, '47 15 81', 'Set Wind Speed: 1 km/h')
    print()

async def write_power_extension(client, hex, comment=None):
    data = bytearray.fromhex(hex)
    s = f'write_power_extension( {ToHex(data)} )'
    print(f'{s:<48}' + ('Unknown' if(comment==None) else comment))
    await client.write_gatt_char(kickr.uuids.kickr_cycling_power_extension, data, response=False)
    await asyncio.sleep(0.5)

def power_extension_handler(characteristic: BleakGATTCharacteristic, data: bytearray):
    print(f'Power Extension:    {ToHex(data)}')
    decode_power_extension(data)
    print()

def decode_power_extension(data):
    pass