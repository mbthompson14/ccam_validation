#!/usr/bin/env python

import pavlovia_np
import redcap_surveys
from config import token

def main():
    while True:
        record_screen = str(input("Enter participant screening number (e to exit): "))
        if record_screen == 'e':
            exit()
        record_id = input("Enter consented record number (e to exit): ")
        if record_id == 'e':
            exit()
        else:
            pavlovia_np.find_validate_files(record_screen)
            redcap_surveys.get_timing(record_id, token)

if __name__ == "__main__":
    main()