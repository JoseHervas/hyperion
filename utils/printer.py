# -*- coding: utf-8 -*-

import pyfiglet

def print_banner():
    print("\n==========================================")
    ascii_banner = pyfiglet.figlet_format("Hyperion")
    print(ascii_banner)
    print("version: 1.0.0")
    print("author: jhervas <https://github.com/JoseHervas>\n")
