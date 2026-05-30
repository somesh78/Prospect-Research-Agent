from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import json
import os
from scraper import enrich_company

app = FastAPI(title="Prospect Research Agent")

RESULTS_FILE = "results.json"

if not os.path.exists(RESULTS_FILE):
    with open(RESULTS_FILE, "w") as f:
        json.dump([], f)


class EnrichRequest(BaseModel):
    website_name: str
    url: str


@app.get("/", response_class=HTMLResponse)
def home():
    with open("templates/index.html", "r", encoding="utf-8") as f:
        return f.read()


@app.post("/enrich")
def enrich(data: EnrichRequest):

    try:
        result = enrich_company(data.url)

        result["website_name"] = data.website_name

        with open(RESULTS_FILE, "r") as f:
            records = json.load(f)

        records.append(result)

        with open(RESULTS_FILE, "w") as f:
            json.dump(records, f, indent=2)

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/results")
def get_results():

    with open(RESULTS_FILE, "r") as f:
        return json.load(f)