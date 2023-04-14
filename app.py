from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from serial import Serial
from random import randint

app = FastAPI()

port = Serial(
    port="/dev/tty.usbmodem1101",
    baudrate=115200,
)

class Color(BaseModel):
    red: int
    green: int
    blue: int

@app.post("/controller")
def set_bed(color: Color):
    output = [0x7e, color.red & 0xFF, color.green & 0xFF, color.blue & 0xFF, 0xAA, 0x0A]
    cheksum = 0xFF - (sum(output[1:]) & 0xFF)
    output.append(cheksum)
    print(output)
    port.write(bytearray(output))
    return cheksum

@app.get("/temperature")
def status():
    return {"temperature": randint(0, 255)}

@app.get("/")
def status():
    return "Welcome to the Internet, I will be your guide"

if __name__ == "__main__":
    uvicorn.run(
        app, host="0.0.0.0", port=8080, workers=1, log_level="debug"
    )
