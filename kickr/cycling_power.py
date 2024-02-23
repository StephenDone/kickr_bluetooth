from enum import IntFlag, IntEnum

from bleak.backends.characteristic import BleakGATTCharacteristic

from convert import ToHex, unsigned_16, signed_16, unsigned_32

class feature_flags(IntFlag):   
    Pedal_Power_Balance                 = 0x00000001,
    Accumulated_Torque                  = 0x00000002,
    Wheel_Revolution_Data               = 0x00000004,
    Crank_Revolution_Data               = 0x00000008,
    Extreme_Magnitudes                  = 0x00000010,
    Extreme_Angles                      = 0x00000020,
    Top_and_Bottom_Dead_Spot_Angles     = 0x00000040,
    Accumulated_Energy                  = 0x00000080,
    Offset_Compensation_Indicator       = 0x00000100,
    Offset_Compensation                 = 0x00000200,
    Measurement_Content_Masking         = 0x00000400,
    Multiple_Sensor_Locations           = 0x00000800,
    Crank_Length_Adjustment             = 0x00001000,
    Chain_Length_Adjustment             = 0x00002000,
    Chain_Weight_Adjustment             = 0x00004000,
    Span_Length_Adjustment              = 0x00008000,
    Sensor_Measurement_Torque_Based     = 0x00010000,
    Instantaneous_Measurement_Direction = 0x00020000,
    Factory_Calibration_Date            = 0x00040000,
    
class sensor_location(IntEnum):
    Other = 0,
    Top_of_Shoe = 1,
    In_Shoe = 2,
    Hip = 3,
    Front_Wheel = 4,
    Left_Crank = 5,
    Right_Crank = 6,
    Left_Pedal = 7,
    Right_Pedal = 8,
    Front_Hub = 9,
    Rear_Dropout = 10,
    Chainstay = 11,
    Rear_Wheel = 12,
    Rear_Hub = 13,
    Chest = 14,

class PowerMeasurementFlags(IntFlag):
    Pedal_power_balance_present = 0x0001,
    Pedal_power_balance_reference_left = 0x0002,
    Accumulated_torque_present = 0x0004,
    Accumulated_torque_source_crank_based = 0x0008,
    Wheel_revolution_data_present = 0x0010,
    Crank_revolution_data_present = 0x0020,
    Extreme_force_magnitudes_present = 0x0040,
    Extreme_torque_magnitudes_present = 0x0080,
    Extreme_angles_present = 0x0100,
    Top_dead_spot_angle_present = 0x0200,
    Bottom_dead_spot_angle_present = 0x0400,
    Accumulated_energy_present = 0x0800,
    Offset_compensation_indicator = 0x1000,

PowerMeasurementDataSize = [
        1,
        0,
        2,
        0,
        6,
        4,
        4,
        4,
        3,
        2,
        2,
        2,
        0
    ]

async def start_notify(client):
    await client.start_notify('00002a63-0000-1000-8000-00805f9b34fb', power_handler)

async def stop_notify(client):
    await client.stop_notify('00002a63-0000-1000-8000-00805f9b34fb')

def power_handler(characteristic: BleakGATTCharacteristic, data: bytearray):
    print(f'Power:  {ToHex(data):<23}')
    decode_power(data)
    print()

def decode_power(data):

    def CheckDataLength(data) -> bool:

        Flags = PowerMeasurementFlags( unsigned_16(data[0],data[1]) )
        FlagValues = list(PowerMeasurementFlags)

        # At a minimum, the data always contains flags(2) and power(2) = 4 bytes
        DataLength = 4

        for i in range( len(FlagValues)-1 ):
            if FlagValues[i] in Flags:
                #print(f'Found Flag {FlagValues[i]}')
                DataLength += PowerMeasurementDataSize[i]
        
        result = DataLength == len(data)

        if not result:
            print("data.Length={data.Length}, Expected Length={DataLength}")

        return result

    if not CheckDataLength(data):
        print("Bad CyclingPowerMeasurement Data Length")
        return 

    Flags = PowerMeasurementFlags( unsigned_16(data[0],data[1]) )

    print(f'Flags: {[e.name for e in Flags]}')

    Power = signed_16(data[2], data[3])
    print(f'Power:{Power}')

    index = 4

    # Pedal Power Balance - uint8
    if PowerMeasurementFlags.Pedal_power_balance_present in Flags:
        index += 1
        print('Pedal_power_balance_present')

    # Accumulated Torque - uint16
    if PowerMeasurementFlags.Accumulated_torque_present in Flags:
        AccumulatedTorqueInt = unsigned_16(data[index], data[index+1])
        AccumulatedTorque = AccumulatedTorqueInt / 32
        index += 2
        print(f'AccumulatedTorque:{AccumulatedTorque}')

    # Wheel Revolution Data - Cumulative Wheel Revolutions - uint32
    # Wheel Revolution Data - Last Wheel Event Time        - uint16
    if PowerMeasurementFlags.Wheel_revolution_data_present in Flags:
        CumulativeWheelRevolutions = unsigned_32(data[index], data[index+1],data[index+2], data[index+3])
        index += 4

        LastWheelEventTimeInt = unsigned_16(data[index], data[index+1])
        LastWheelEventTime = LastWheelEventTimeInt / 2048
        index += 2

        print(f'CumulativeWheelRevolutions:{CumulativeWheelRevolutions}')
        print(f'LastWheelEventTime:{LastWheelEventTime:.2f}')

    # Crank Revolution Data- Cumulative Crank Revolutions - uint16
    # Crank Revolution Data- Last Crank Event Time - uint16
    if PowerMeasurementFlags.Crank_revolution_data_present in Flags:
        CumulativeCrankRevolutions = unsigned_16(data[index], data[index+1])
        index += 2

        LastCrankEventTimeInt = unsigned_16(data[index], data[index+1])
        LastCrankEventTime = LastCrankEventTimeInt / 1024
        index += 2

        print(f'CumulativeCrankRevolutions:{CumulativeCrankRevolutions}')
        print(f'LastCrankEventTime:{LastCrankEventTime:.2f}')

    # Extreme Force Magnitudes - Maximum Force Magnitude - sint16
    # Extreme Force Magnitudes - Minimum Force Magnitude - sint16
    if PowerMeasurementFlags.Extreme_force_magnitudes_present in Flags: 
        index += 4
        print('Extreme_force_magnitudes_present')

    # Extreme Torque Magnitudes - Maximum Torque Magnitude - sint16
    # Extreme Torque Magnitudes - Minimum Torque Magnitude - sint16
    if PowerMeasurementFlags.Extreme_torque_magnitudes_present in Flags: 
        index += 4
        print('Extreme_torque_magnitudes_present')

    # Extreme Angles - Maximum Angle - uint12
    # Extreme Angles - Minimum Angle - uint12
    if PowerMeasurementFlags.Extreme_angles_present in Flags: 
        index += 3
        print('Extreme_angles_present')

    # Top Dead Spot Angle - uint16
    if PowerMeasurementFlags.Top_dead_spot_angle_present in Flags: 
        index += 2
        print('Top_dead_spot_angle_present')

    # Bottom Dead Spot Angle - uint16
    if PowerMeasurementFlags.Bottom_dead_spot_angle_present in Flags: 
        index += 2
        print('Bottom_dead_spot_angle_present')

    # Accumulated Energy - uint16
    if PowerMeasurementFlags.Accumulated_energy_present in Flags: 
        index += 2
        print('Accumulated_energy_present')

    if index != len(data): 
        print("CyclingPowerMeasurement: data index not consistent with data length")


async def cycling_power_tests(client):
    print('CYCLING POWER')

    # Cycling Power Feature
    data = await client.read_gatt_char('00002a65-0000-1000-8000-00805f9b34fb')
    #data = [ 0x0e, 0x00 ]

    bitfield = unsigned_16(data[0], data[1])

    flags = feature_flags(bitfield)

    print(f'  Feature: data {ToHex(data)} -> bitfield 0x{bitfield:04x} -> {bitfield:016b}b')

    for flag in flags: print(f'    0x{flag.value:08x} {flag.name}')

    # Sensor Location
    data = await client.read_gatt_char('00002a5d-0000-1000-8000-00805f9b34fb')
    location_byte = data[0]
    location = sensor_location(location_byte)
    print(f'  Sensor Location: {ToHex(data)} -> 0x{location_byte:02x} -> {location.name}')

    print()
