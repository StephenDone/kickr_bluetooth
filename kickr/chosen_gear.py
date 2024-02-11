from convert import ToHex

import kickr.uuids

async def start_notify(client):
    await client.start_notify(kickr.uuids.kickr_chosen_gear, chosen_gear_handler)

async def stop_notify(client):
    await client.stop_notify(kickr.uuids.kickr_chosen_gear)

def chosen_gear_handler(characteristic, data: bytearray):
    # print(f'Chosen Gear: {ToHex(data)}')
    print(f'Gear:   {ToHex(data):<35} {decode_gear(data)}')
    print()

def decode_gear(data):
    #print(f'decode_tilt( {ToHex(data)} )')

    # Gear configuration updated
    if(len(data)==4 and data==bytearray([0x02, 0x00, 0x00, 0x00])):
        return 'Gear Configuration Updated'

    # Current state - 11 bytes of data with 5x 0x00 bytes at the end
    if(len(data)==11 and data[0]==0x07 and data[1]==0 and data[6:11]==bytearray([0,0,0,0,0])):
        return f'REPEAT - {bytes_to_gear(data)}'
    
    # Update state - 6 bytes of data
    if(len(data)==6 and data[0]==0x01 and data[1]==0):
        return f'UPDATE - {bytes_to_gear(data)}'

    return f'Unknown gear data'

def bytes_to_gear(data):
        chainring = data[2] + 1
        chainring_count = data[4]
        cassette_index = data[3]+1
        cassette_size = data[5]
        return f'Chainring {chainring} of {chainring_count}, Cassette index {cassette_index} of {cassette_size}'
    