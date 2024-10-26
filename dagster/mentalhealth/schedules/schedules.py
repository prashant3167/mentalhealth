# schedules.py
from dagster import ScheduleDefinition
from pipelines.mongo_pipeline import mongo_partitioned_job

# Schedule the job to run daily at midnight
daily_schedule = ScheduleDefinition(
    job=mongo_partitioned_job,
    cron_schedule="0 0 * * *",  # Run at midnight every day
)