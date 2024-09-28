from fastapi import FastAPI, HTTPException
from openai import OpenAI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from pydantic import BaseModel, EmailStr
import os, shutil
import gdown

from Utils.SendingEmailUtil import send_email, send_rating_email
from Utils.RecommendationAnalyze import recommendation_algorithm, dataSetUp
load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    folder_path = 'downloaded_folder'

    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)

    gdown.download_folder(recommendation_file_url, output=folder_path, quiet=False)

    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

backend_port = int(os.getenv("BACKEND_PORT", '8000'));
ip_address = os.getenv("IP_ADDRESS", '127.0.0.1')
fileResearch = os.getenv("fileResearch", "")
client = OpenAI(api_key=os.getenv("OPENAI_KEY", ''), )

recommendation_file_url=os.getenv("FILE_SEARCH_URL", "");


class EmailRequest(BaseModel):
    recipient: EmailStr
    subject: str
    detail: str
    recommendation: str
    prompt: str


class RatingEmailRequest(BaseModel):
    rating: int
    userPrompt: str
    summary: str



@app.post("/send-email")
async def send_email_endpoint(email_request: EmailRequest):
    success = send_email(email_request.recipient, email_request.subject, email_request.detail,
                         email_request.recommendation, email_request.prompt, False, False, email_request.recipient)
    success1 = send_email("pascalsharpe@proservicemobile.com", "Vehicle Diagnostic ChatBot", email_request.detail,
                          email_request.recommendation, email_request.prompt, True, False, email_request.recipient)
    # success2 = send_email("tortrex8@gmail.com", "Vehicle Diagnostic ChatBot", email_request.detail,
    #                       email_request.recommendation, email_request.prompt, True, False, email_request.recipient)
    print(success1)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to send email")
    return {"message": "Email sent successfully"}


@app.post("/demo-send-email")
async def send_email_endpoint(email_request: EmailRequest):
    success = send_email(email_request.recipient, email_request.subject, email_request.detail,
                         email_request.recommendation, email_request.prompt, False, True, email_request.recipient)
    success1 = send_email("pascalsharpe@proservicemobile.com", "Vehicle Diagnostic ChatBot", email_request.detail,
                          email_request.recommendation, email_request.prompt, True, True, email_request.recipient)
    # success2 = send_email("tortrex8@gmail.com", "Vehicle Diagnostic ChatBot", email_request.detail,
    #                       email_request.recommendation, email_request.prompt, True, True, email_request.recipient)
    print(success1)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to send email")
    return {"message": "Email sent successfully"}


@app.post("/rating-email")
async def send_rating_email_endpoint(RatingEmailRequest: RatingEmailRequest):
    success = send_rating_email("pascalsharpe@proservicemobile.com", "Rating Check Email", RatingEmailRequest.rating,
                                RatingEmailRequest.userPrompt, RatingEmailRequest.summary)
    # success1 = send_rating_email("tortrex8@gmail.com", "Rating Check Email", RatingEmailRequest.rating,
    #                              RatingEmailRequest.userPrompt, RatingEmailRequest.summary)
    print(success);
    if not success:
        raise HTTPException(status_code=500, detail="Failed to send email")
    return {"message": "Email sent successfully"}

@app.get("/access-recommendation")
async def assess_recommendation():
    technicians, integrated_factors = dataSetUp();
    response = {
        "technicians": technicians,
        "integrated_factors": integrated_factors
    }
    return response



if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=ip_address, port=backend_port);
