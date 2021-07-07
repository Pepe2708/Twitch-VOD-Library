from fastapi import FastAPI, Path
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from video_database import *
from video_scraper import *

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)



class AddVideoRequest(BaseModel):
    url: str

class UpdateLengthRequest(BaseModel):
    length: str

@app.get("/get-info/{sort_by}/{is_ascending}")
def get_info(sort_by: str, is_ascending: int):
    return get_video_info(sort_by, is_ascending)

@app.get("/get-amount")
def get_length():
    return get_video_amount()

@app.post("/new-video")
def new_video(request_body: AddVideoRequest):
    video = scrape_web_data(request_body, get_video_amount())
    add_video(video)

@app.delete("/delete-video/{video_id}")
def delete_video(video_id: int):
    remove_video(video_id)

@app.put("/change-order/{video_id}/{direction}")
def change_order(video_id: int, direction: str):
    update_video_order(video_id, direction)

@app.put("/update-done/{video_id}")
def update_done(video_id: int):
    toggle_done(video_id)

@app.put("/update-favorite/{video_id}")
def update_favorite(video_id: int):
    toggle_favorite(video_id)

@app.put("/update-length/{video_id}")
def update_length(video_id: int, request_body: UpdateLengthRequest):
    update_duration(video_id, request_body)