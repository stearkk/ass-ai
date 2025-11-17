from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from backend.model import predict_schedule
from datetime import time, date
from enum import Enum
from typing import Union, List

class TaskType(str, Enum):
    ONCE = "once"
    HABIT = "habit"

class PeriodType(str, Enum):
    DAY = "day"
    WEEK = "week"
    MONTH = "month"
    YEAR = "year"
    CUSTOM_DAYS = "custom_days"

class TaskBase(BaseModel):
    name: str
    priority: int
    duration: int  

class TaskOnce(TaskBase):
    type: TaskType = TaskType.ONCE
    exact_time: str | None = None  # "HH:MM"
    exact_date: str | None = None  # "YYYY-MM-DD"
    deadline: str | None = None    # "YYYY-MM-DD"

class TaskHabit(TaskBase):
    type: TaskType = TaskType.HABIT
    times_per: int  # сколько раз выполнять за период
    period: PeriodType  # период повторения
    end_date: str | None = None  # "YYYY-MM-DD" - до какой даты
    custom_days: int | None = None  # для period=CUSTOM_DAYS
    exact_times: List[dict] = []  # список {time: "HH:MM", weekday: "mon", date: "YYYY-MM-DD"}
    selected_days: List[str] = []  # ["mon", "tue", ...]

class TaskList(BaseModel):
    tasks: List[Union[TaskOnce, TaskHabit]]


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "planner is runniing! wiiiiiiiiiin"}

@app.post("/analyze")
def analyze_tasks(task_list: TaskList):
    schedule = predict_schedule(task_list.tasks)
    return {"schedule" : schedule}
