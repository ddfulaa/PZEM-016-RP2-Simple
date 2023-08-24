import board
import busio
import time

def reset_energy(tx_pin = board.GP8, rx_pin = board.GP9):
    uart = busio.UART(tx=tx_pin, rx=rx_pin, baudrate=9600, bits=8, parity = None, stop=1, timeout=0.1)
    command = bytearray([0x01,0x42,0x80,0x11]) 
    uart.write(command)
    answer = uart.read()
    uart.deinit()
    return answer
    
def read_values(tx_pin = board.GP8, rx_pin = board.GP9):
    uart = busio.UART(tx=tx_pin, rx=rx_pin, baudrate=9600, bits=8, parity = None, stop=1, timeout=0.1)
    command = bytearray([0x01,0x04,0x00,0x00,0x00,0x0A,0x70,0x0D]) # Read all parameters
    uart.write(command)
    answer = uart.read()
    uart.deinit()
    if len(answer)==25:
        voltage = (answer[3]*256+answer[4])*0.1
        current = ((answer[7]*256+answer[8])*256**2+answer[5]*256+answer[6])*0.001
        power = ((answer[11]*256+answer[12])*256**2+answer[9]*256+answer[10])*0.1
        energy = ((answer[15]*256+answer[16])*256**2+answer[13]*256+answer[14])
        freq = (answer[17]*256+answer[18])*0.1
        pf = (answer[19]*256+answer[20])*0.01
        return (voltage,current,power,energy,freq,pf)
    else:
        return 0


reset_energy()
print('Se ha reiniciado el contador de la energía.')

while True:
    voltage, current, power, energy, freq, pf = read_values()
    print(f'V:{voltage}V, A:{current}A, P:{power}W, E:{energy}Wh, f:{freq}Hz, pf:{pf}')
    time.sleep(0.15)


