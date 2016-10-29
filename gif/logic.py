#!/usr/bin/env python3

def it_is_gif(bytes):
    gif = ""
    for byte in bytes:
        gif += chr(int(byte, 16))
    if gif == "GIF":
        return True
    return False

def get_version(bytes):
    return chr(int(bytes[3], 16))+chr(int(bytes[4], 16))+chr(int(bytes[5], 16))

def get_w(bytes):
    return int(bytes[7]+bytes[6], 16)

def get_h(bytes):
    return int(bytes[9]+bytes[8], 16)

def get_bytes(file_name):
    result = []
    with open(file_name, mode='br') as file:
        char = file.read(1)
        while char:
            result.append("%02x" % char[0])
            char = file.read(1)
    return result

def get_str_byte(bytes):
    text = str(bin(int(bytes[10], 16)))
    text = text[2:]
    while len(text) != 8:
        text = "0" + text
    return text

def get_exsisting_colors(byte):
    if byte[0] == "1":
        return "используется"
    return "не используется"

def get_num_colors(byte):
    return 2**(int("".join(byte[1:4]), 2)+1)

def miss_numbers(bytes):
    number = 13
    while bytes[number] == "21" or bytes[number] == "00":
        while bytes[number] != "00":
            number += 1
        number += 1
    return number