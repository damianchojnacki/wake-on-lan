from fastapi import FastAPI, Body, HTTPException
import re

app = FastAPI()

def is_valid_mac_address(mac):
  """
  Validates a MAC address using a regular expression.

  Args:
      mac (str): The MAC address to validate.

  Returns:
      bool: True if the MAC address is valid, False otherwise.
  """
  # Regular expression for a valid MAC address
  mac_address_pattern = r"^([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}$|^([0-9A-Fa-f]{2}-){5}[0-9A-Fa-f]{2}$"

  return bool(re.match(mac_address_pattern, mac))

@app.post("/")
async def wake_on_lan(data: dict = Body(...)):
  """
  Receive POST request with MAC in body and send magic packet.
  """  
  mac = data.get("mac")

  if not mac:
    raise HTTPException(status_code=422, detail="Missing 'mac' field in request body")

  if not is_valid_mac_address(mac):
    raise HTTPException(status_code=422, detail="Invalid MAC address format")
  
  import subprocess

  process = subprocess.run(["awake", mac], capture_output=True)

  error = process.stderr.decode()

  if error:
    raise HTTPException(status_code=500, detail=error)

  return {"message": process.stdout.decode()}
  
@app.get("/")
async def health():
  """
  Health check
  """
  return {"status": "OK"}

if __name__ == "__main__":
  import uvicorn
  uvicorn.run("app:app", host="0.0.0.0", port=8080)