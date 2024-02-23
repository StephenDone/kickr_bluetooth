import asyncio

from convert import ToHex, unsigned_16

from bleak.uuids import normalize_uuid_16

weight_characteristic = normalize_uuid_16(0x2a98)

async def read(client):
    print('USER DATA')
    data = await client.read_gatt_char(weight_characteristic)
    if(len(data)==2):
        weight = unsigned_16(data[0],data[1]) / 200
    print(f'  {ToHex(data)} Weight = {weight}kg')
    print()