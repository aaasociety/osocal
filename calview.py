#!/bin/python3

import sys
import src.term as trm

def main():
    try:
        trm.init()
        trm.print("Hello World!");
        print("HELLO WORLD!")
    except KeyboardInterrupt:
        print(trm.debug())
        sys.exit(1)

if __name__ == "__main__":
    main()
else:
    print("Do not import this program")
    leave()
    sys.exit(1)
