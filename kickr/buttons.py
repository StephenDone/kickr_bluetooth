from enum import Enum

import asyncio

import bleak
from bleak.backends.characteristic import BleakGATTCharacteristic

from convert import ToHex, unsigned_16

import kickr.uuids

class Button_bits(Enum):
    Brake_Left              = 0x0001
    Top_Front_Left_Decline  = 0x0002
    Top_Back_Left_Incline   = 0x0004
    Shift_Back_Left         = 0x0008
    Shift_Front_Left        = 0x0010
    Steer_Left              = 0x0020
    Brake_Right             = 0x0040
    Top_Back_Right          = 0x0080
    Top_Front_Right         = 0x0100
    Shift_Back_Right        = 0x0200
    Shift_Front_Right       = 0x0400
    Steer_Right             = 0x0800

class Button_index(Enum):
    Brake_Left              = 2
    Top_Front_Left_Decline  = 3
    Top_Back_Left_Incline   = 4
    Shift_Back_Left         = 5
    Shift_Front_Left        = 6
    Steer_Left              = 7
    Brake_Right             = 8
    Top_Back_Right          = 9
    Top_Front_Right         = 10
    Shift_Back_Right        = 11
    Shift_Front_Right       = 12
    Steer_Right             = 13

async def start_notify(client):
    await client.start_notify(kickr.uuids.kickr_buttons, button_handler)

async def stop_notify(client):
    await client.stop_notify(kickr.uuids.kickr_buttons)

def button_handler(characteristic: BleakGATTCharacteristic, data: bytearray):
    print(f'Buttons:   {ToHex(data):<43} {decode_buttons(data)}')
    print()

def decode_buttons(data):

    if(len(data)==14 and data[0]==0xFF and data[1]==0x0F):
        result='state  '

        for button in Button_index:
            click_count = data[button.value]
            result = result + f'{button.name}={click_count}  '

        return result

    elif(len(data)==3):
        bitfield = unsigned_16(data[0], data[1])
        button_down = data[2] & 0x80 == 0x80
        click_count = data[2] & 0x7F
        return f'event  {Button_bits(bitfield).name:<22}  {"down" if button_down else "up":<4}  click_count={click_count}'

    return f'Unknown button data'


