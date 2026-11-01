from sqlalchemy.orm import Session

from app.models import Task

def process_task(db: Session, task_id: int) -> bool:
    task = db.get(Task, task_id)

    if task is None:
        return False

    if task.status != "processing":
        return False

    try:
        print(f"processing task: {task_id} - {task.title}")
        #processing work

        task.status = "completed"
        db.commit()

        print(f"Task {task.id} completed")
        return True

    except Exception:
        db.rollback()
        raise
