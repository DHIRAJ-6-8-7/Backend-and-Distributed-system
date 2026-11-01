from app.database import SessionLocal, claim_task

task_id = 2

with SessionLocal() as db:
    first_result = claim_task(db, task_id)
    print("first claim:", first_result)
with SessionLocal() as db:
    second_result = claim_task(db, task_id)
    print("first claim:", second_result)
