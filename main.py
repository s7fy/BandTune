import serial

# set com port 
port = 'your_comport' # check your device manager and look USB-SERIAL (COMxx) 

# list of band rates to try (17 types)
baud_rates = [
    1200, 2400, 4800, 9600, 19200, 38400, 57600, 
    115200, 230400, 460800, 500000, 576000, 921600, 
    100000, 11520000, 1500000, 2000000
]

# list of encodings list to try (17 types)
encodings = [
    "utf-8", "utf-16", "utf-32", "ascii", "latin-1", "shift_jis",
    "euc-jp", "iso-8859-1", "iso-8859-2", "cp1252", "big5", "gb2312",
    "gbk", "hz", "koi8-r", "mac-roman", "windows-1251"
]

# reset index for baud rates list and encodings list
i = 0  # for band rates
j = 0  # for encodings

# start connection
while True:
    try:
        # open serial connection 
        with serial.Serial(port, baud_rates[i], timeout=1) as ser:
            print(f"Connected to {port} at {baud_rates[i]} baud with encoding {encodings[j]}")

            while True:
                data = ser.readline()
                if data:
                    try:
                        # decode and show
                        print(data.decode(encodings[j]).strip())
                    except UnicodeDecodeError:
                        # show data and end to loop if decode error
                        print(f"Binary data: {data}")
                        print(f"Hexadecimal: {data.hex()}")
                        raise ValueError("Decoding failed")

    except (serial.SerialException, ValueError):
        # change band rate or encoding
        i += 1
        if i >= len(baud_rates):
            i = 0  # return to the top of the baud rates list 
            j += 1
            if j >= len(encodings):
                j = 0  # return to the top of the encodings list
        
        print(f"Switching to baud rate {baud_rates[i]} and encoding {encodings[j]}")
    
    # other error
    except Exception as e:
        print(f"Unexpected error: {e}")
        break
