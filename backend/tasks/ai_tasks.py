from celery_config import celery
import subprocess

@celery.task
def retrain_ai():

    subprocess.run(
        [
            "python",
            "ai_model/train_model.py"
        ]
    )

    return {
        "status": "completed"
    }