from fastapi import FastAPI
from pydantic import BaseModel
from typing import Literal
from uuid import uuid4
from datetime import datetime, timezone
import requests
import time
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

app = FastAPI(title="Task Service")

NOTIFICATION_URL = "http://127.0.0.1:8002/api/webhooks/task_created"

tasks = {}


class TaskCreate(BaseModel):
    title: str
    description: str = ""


class Task(BaseModel):
    id: str
    title: str
    description: str
    status: Literal["new", "in_progress", "done"] = "new"
    created_at: str


def send_webhook(task: dict) -> bool:
    for attempt in range(1, 4):
        try:
            response = requests.post(
                NOTIFICATION_URL,
                json=task,
                timeout=3
            )

            if response.status_code == 200:
                logging.info("Webhook отправлен успешно")
                return True

            logging.warning(
                "Webhook вернул код %s",
                response.status_code
            )

        except Exception as error:
            logging.warning(
                "Попытка %s отправить webhook не удалась: %s",
                attempt,
                error
            )

        time.sleep(1)

    logging.error("Не удалось отправить webhook после 3 попыток")
    return False


@app.post("/api/tasks", response_model=Task, status_code=201)
def create_task(payload: TaskCreate):
    task = Task(
        id=str(uuid4()),
        title=payload.title,
        description=payload.description,
        status="new",
        created_at=datetime.now(timezone.utc).isoformat()
    )

    tasks[task.id] = task

    # Отправляем вебхук. Если не получится — задача всё равно создана.
    send_webhook(task.model_dump())

    return task


@app.get("/api/tasks")
def get_tasks():
    return list(tasks.values())


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8001)
