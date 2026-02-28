import os
import shutil
from fastapi import FastAPI, UploadFile, File
from openIDscan import simple_scan

# Initialize the API
app = FastAPI(
    title="OpenIDScan API",
    description="A simple, CC0 open-source API for extracting DOB and Nation from ID cards.",
    version="1.0.0"
)

@app.post("/scan")
async def scan_id(file: UploadFile = File(...)):
    """
    Endpoint that accepts an image file upload and returns the OpenIDScan JSON.
    """
    # 1. Save the uploaded file temporarily
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # 2. Run your scanner
    result = simple_scan(temp_path)
    
    # 3. Clean up the temporary file (Privacy friendly!)
    if os.path.exists(temp_path):
        os.remove(temp_path)
        
    # 4. Return the JSON
    return result

# This allows the server to run if executed directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
