import pickle
import numpy as np
from typing import List
from contextlib import asynccontextmanager

from sklearn.decomposition import PCA

from fastapi import FastAPI


def fake_answer_to_everything_ml_model(x: float):
    return x * 42


ml_models = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ML model
    ml_models["answer_to_everything"] = fake_answer_to_everything_ml_model
    ml_models["4dmodel"] = load_model()
    yield
    # Clean up the ML models and release the resources
    ml_models.clear()


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def index():
    return {"message": "Hello World"}


@app.post("/predict")
async def predict(x: List[float]):
    data = np.array(x).reshape(1, -1)
    result = model_predict(ml_models["4dmodel"], data)
    serialized = result[0].tolist()
    return serialized


def load_model():
    with open('../model.pkl', 'rb') as f:
        model = pickle.load(f)
    return model


def model_predict(model: PCA, x: List[float]):
    return model.transform(x)
