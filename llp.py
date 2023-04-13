import struct
from serial import Serial
from threading import Thread
from queue import Queue
from time import sleep



class Llp():
    def __init__(self, header: int, port: Serial, queue: Queue):
        self.__header = header
        self.__queue = queue
        self.__running = False
        self.__port = port

    @staticmethod
    def __parse_payload(payload: list[int]) -> dict:
        output = {}
        for index in range(0, len(payload), 3):
            output[payload[index]] = payload[index + 1] << 8 | payload[index + 2]
        return output

    @staticmethod
    def __calculate_checksum(payload: list[int]) -> int:
        return (0xFF - (sum(payload) & 0xFF))

    def __verify_checksum(self, payload: list[int], checksum: int) -> bool:
        return self.__calculate_checksum(payload=payload) == checksum
    
    def __loop(self) -> None:
        while self.__running:
            header = self.__port.read()
            if ord(header) == self.__header:
                lenght = ord(self.__port.read())
                payload = list(struct.unpack(f"<{lenght}B", self.__port(lenght)))
                checksum = ord(self.__port.read())
                assert self.__verify_checksum(payload=payload, checksum=checksum)
                payload = self.__parse_payload(payload=payload)
                self.__queue.put(payload)
                print(payload)
            sleep(0.01)

    def listen(self):
        self.__running = True
        Thread(target=self.__loop)

    def stop(self):
        self.__running


def main():
    port = Serial(
        port="/dev/tty.usbmodem2143401",
        baudrate=115200,
    )

    input = Queue()

    llp = Llp(header=0x7e, port=port, queue=input)
    llp.listen()

    while True:
        payload = input.get()
        print(payload)

if __name__ == '__main__':
    main()