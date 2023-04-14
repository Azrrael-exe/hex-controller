import requests
from time import sleep

def temp_controller(temp: int) -> dict:
    return {
        "red": temp,
        "blue": 255 - temp,
        "green": 0,
    }

def main():
    while True:
        temp = requests.get(url="http://localhost:8080/temperature").json().get("temperature")
        print(f"Received temp {temp}")
        payload = temp_controller(temp=temp)
        print(payload)
        signal_send = requests.post(url="http://localhost:8080/controller", json=payload)
        print(signal_send.status_code)
        sleep(20)

if __name__ == "__main__":
    main()