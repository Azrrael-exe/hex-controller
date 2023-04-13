from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from serial import Serial

app = FastAPI()

port = Serial(
    port="/dev/tty.usbmodem21201",
    baudrate=115200,
)

class Color(BaseModel):
    red: int
    green: int
    blue: int

@app.post("/sum")
def set_bed(color: Color):
    output = [0x7e, color.red & 0xFF, color.green & 0xFF, color.blue & 0xFF, 0xAA, 0x0A]
    cheksum = 0xFF - (sum(output[1:]) & 0xFF)
    output.append(cheksum)
    print(output)
    port.write(bytearray(output))
    return cheksum

if __name__ == "__main__":
    uvicorn.run(
        app, host="localhost", port=8080, workers=1, log_level="debug"
    )
