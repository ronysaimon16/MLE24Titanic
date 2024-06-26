from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
import pickle
import os

app = FastAPI()

# Load the trained model
with open('best_rf_clf.pkl', 'rb') as file:
    model = pickle.load(file)

# Assuming main.py is in the same directory as the templates and static directories
templates_dir = os.path.join(os.path.dirname(__file__), "templates")
static_dir = os.path.join(os.path.dirname(__file__), "static")
templates = Jinja2Templates(directory=templates_dir)

@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/predict/")
async def predict(request: Request,
                  pclass: int = Form(...),
                  sex: int = Form(...),  # Change type to int
                  age: int = Form(...),
                  sibsp: int = Form(...),
                  parch: int = Form(...),
                  fare: int = Form(...),
                  embarked: int = Form(...),  # Change type to int
                  familysize: int = Form(...)):

    features = [pclass, sex, age, sibsp, parch, fare, embarked, familysize]

    # Make prediction
    prediction = model.predict([features])[0]
    result = "High probability for " if prediction == 1 else "Very less probability "

    return templates.TemplateResponse("results.html", {"request": request, "prediction": result})

# Mounting the static files directory
@app.get("/static/{filename}")
async def get_static_file(filename: str):
    return FileResponse(os.path.join(static_dir, filename), media_type="text/css")
