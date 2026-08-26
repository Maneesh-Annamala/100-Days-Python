from fastapi import FastAPI,UploadFile,File,Request
import numpy as np
from PIL import Image
from io import BytesIO
from fastapi.templating import Jinja2Templates


app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def home(request : Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )


@app.post("/analyze")
async def analyze_image(image : UploadFile = File(...) ):
    contents = await image.read()
    img = Image.open(BytesIO(contents))
    img = img.convert("RGB")
    img_arr = np.array(img)

    pixels = img_arr.reshape(-1,3)

    colors,count = np.unique(pixels,axis=0,return_counts=True)

    indices = np.argsort(count)[::-1]

    top_colors = colors[indices[:10]]
    hex_codes = []
    for color in top_colors:
        r,g,b = color
        hex_code = f"#{r:02x}{g:02x}{b:02x}"
        hex_codes.append(hex_code)

    return {"colors" : hex_codes }
