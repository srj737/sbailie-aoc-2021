import math
from math import prod


def ingest_string(filename):
    with open(filename) as file:
        lines = file.readlines()
    output = lines[0].strip()
    return output


hex_to_four_digit_binary = {
    '0': '0000', '1': '0001', '2': '0010', '3': '0011', '4': '0100', '5': '0101', '6': '0110', '7': '0111',
    '8': '1000', '9': '1001', 'A': '1010', 'B': '1011', 'C': '1100', 'D': '1101', 'E': '1110', 'F': '1111'
}

# These two values are numbers; all numbers encoded in any packet are represented
# as binary with the most significant bit first. For example, a version encoded as the binary sequence 100
# represents the number 4.
three_digit_binary_to_hex = {
    '000': '0', '001': '1', '010': '2', '011': '3', '100': '4', '101': '5', '110': '6', '111': '7'
}


def translate_hex(hex):
    # Step 1) Convert Hex to Binary
    binary = ""
    for char in hex:
        binary += hex_to_four_digit_binary[char]
    return decode_packet(binary, 0)


def round_up_to_4(x, base=4):
    return base * math.ceil(x / base)


def decode_packet(binary_stream, offset=0):
    index = offset

    # Step 2) Extract header
    # Every packet begins with a standard header: the first three bits encode the packet version, and the next three
    # bits encode the packet type ID. These two values are numbers; all numbers encoded in any packet are represented
    # as binary with the most significant bit first. For example, a version encoded as the binary sequence 100
    # represents the number 4.
    version = int(three_digit_binary_to_hex[binary_stream[index:index + 3]])
    type_id = int(three_digit_binary_to_hex[binary_stream[index + 3:index + 6]])
    value = 0

    # Step 3) Decoding literal values (type ID 4)
    if type_id == 4:
        # Packets with type ID 4 represent a literal value. Literal value packets encode a single binary number.
        # To do this, the binary number is padded with leading zeroes until its length is a multiple of four bits,
        # and then it is broken into groups of four bits. Each group is prefixed by a 1 bit except the last group,
        # which is prefixed by a 0 bit. These groups of five bits immediately follow the packet header.
        literal_value_binary = ''
        index += 6  # Start at 7th digit due to 6 digit header
        while index < len(binary_stream):
            prefix = binary_stream[index]
            digits = binary_stream[index + 1:index + 5]
            if prefix in ['0', '1']:
                literal_value_binary = literal_value_binary + digits
                index += 5
            if prefix == '0':
                break
        value = int(literal_value_binary, 2)


    # Step 4) Decode operators
    # Every other type of packet (any packet with a type ID other than 4) represent an
    # operator that performs some calculation on one or more sub-packets contained within. Right now, the specific
    # operations aren't important; focus on parsing the hierarchy of sub-packets.
    else:
        # Step 5) Analyse operator's length type ID An operator packet contains one or more packets. To indicate
        # which subsequent binary data represents its sub-packets, an operator packet can use one of two modes 
        # indicated by the bit immediately after the packet header; this is called the length type ID: 
        length_type_id = binary_stream[index + 6]

        subpackets_values = []

        if length_type_id == '0':
            # If the length type ID is 0, then the next 15 bits are a number that represents the total length in bits
            # of the sub-packets contained by this packet.
            subpackets_start = index + 7 + 15
            length_of_subpackets = int(binary_stream[index + 8:subpackets_start], 2)
            subpkts_end = subpackets_start + length_of_subpackets
            # Step 6) Iterate through subpackets
            index = subpackets_start
            while index < subpkts_end:
                decoded = decode_packet(binary_stream, index)
                version += decoded['version']
                subpackets_values.append(decoded['value'])
                index = decoded['index']

        elif length_type_id == '1':
            # If the length type ID is 1, then the next 11 bits are a number that represents the number of 
            # sub-packets immediately contained by this packet. 
            subpackets_start = index + 7 + 11
            number_of_subpackets = int(binary_stream[index + 8:subpackets_start], 2)
            # Step 6) Iterate through subpackets
            index = subpackets_start
            unprocessed_stream = binary_stream[index:]
            for i in range(number_of_subpackets):
                if unprocessed_stream != '':
                    decoded = decode_packet(binary_stream, index)
                    version += decoded['version']
                    subpackets_values.append(decoded['value'])
                    index = decoded['index']

        # Step 7) Calculate the operator value based on the value of the type Id (AoC2021-16-Part2)
        if type_id == 0:
            value = sum(subpackets_values)
        elif type_id == 1:
            value = prod(subpackets_values)
        elif type_id == 2:
            value = min(subpackets_values)
        elif type_id == 3:
            value = max(subpackets_values)
        elif type_id == 5:
            if subpackets_values[0] > subpackets_values[1]:
                value = 1
            else:
                value = 0
        elif type_id == 6:
            if subpackets_values[0] < subpackets_values[1]:
                value = 1
            else:
                value = 0
        elif type_id == 7:
            if subpackets_values[0] == subpackets_values[1]:
                value = 1
            else:
                value = 0
        else:
            value = 0  # (Theoretically impossible)
            print("Something weird happened")

    return {'version': version, 'value': value, 'index': index}


###########################################

hex_string = "D2FE28"
transmission = translate_hex(hex_string)
print("Part 1 Mini Test 1 Input (version: 6, value: 2021): " + str(transmission))

###########################################

hex_string = "38006F45291200"
transmission = translate_hex(hex_string)
print("Part 1 Mini Test 2 Input (version: 9): " + str(transmission))

###########################################

hex_string = "EE00D40C823060"
transmission = translate_hex(hex_string)
print("Part 1 Mini Test 3 Input (value:6 - now changed by Part 2 code): " + str(transmission))

###########################################

hex_string = "8A004A801A8002F478"
transmission = translate_hex(hex_string)
print("Part 1 Mini Test 4 Input (version: 16): " + str(transmission))

###########################################

hex_string = "620080001611562C8802118E34"
transmission = translate_hex(hex_string)
print("Part 1 Mini Test 5 Input (version: 12): " + str(transmission))

###########################################

hex_string = "C0015000016115A2E0802F182340"
transmission = translate_hex(hex_string)
print("Part 1 Mini Test 6 Input (version: 23): " + str(transmission))

###########################################

hex_string = "A0016C880162017C3686B18A3D4780"
transmission = translate_hex(hex_string)
print("Part 1 Mini Test 7 Input (version: 31): " + str(transmission))

###########################################

hex_string = ingest_string('inputs/16-1')
transmission = translate_hex(hex_string)
print("Part 1 Real Input (version: 901): " + str(transmission))

###########################################

hex_string = "C200B40A82"
transmission = translate_hex(hex_string)
print("Part 2 Mini Test 1 Input (value: 3): " + str(transmission))

###########################################

hex_string = "04005AC33890"
transmission = translate_hex(hex_string)
print("Part 2 Mini Test 2 Input (value: 54): " + str(transmission))

###########################################

hex_string = "880086C3E88112"
transmission = translate_hex(hex_string)
print("Part 2 Mini Test 3 Input (value: 7): " + str(transmission))

###########################################

hex_string = "CE00C43D881120"
transmission = translate_hex(hex_string)
print("Part 2 Mini Test 4 Input (value: 9): " + str(transmission))

###########################################

hex_string = "D8005AC2A8F0"
transmission = translate_hex(hex_string)
print("Part 2 Mini Test 5 Input (value: 1): " + str(transmission))

###########################################

hex_string = "F600BC2D8F"
transmission = translate_hex(hex_string)
print("Part 2 Mini Test 6 Input (value: 0): " + str(transmission))

###########################################

hex_string = "9C005AC2F8F0"
transmission = translate_hex(hex_string)
print("Part 2 Mini Test 7 Input (value: 0): " + str(transmission))

###########################################

hex_string = "9C0141080250320F1802104A08"
transmission = translate_hex(hex_string)
print("Part 2 Mini Test 8 Input (value: 1): " + str(transmission))

###########################################

hex_string = ingest_string('inputs/16-1')
transmission = translate_hex(hex_string)
print("Part 2 Real Input (value: 110434737925): " + str(transmission))

###########################################
