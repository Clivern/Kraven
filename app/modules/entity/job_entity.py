"""
Job Entity Module
"""

# standard library
import json
from datetime import timedelta

# Django
from django.utils import timezone

# local Django
from app.models import Job


class Job_Entity():

    ONCE = "once"
    ONCE_AT = "once_at"
    EVERY = "every"
    AFTER = "after"

    PENDING = "pending"
    FAILED  = "failed"
    PASSED  = "passed"
    DAEMON  = "daemon"
    ERROR   = "error"


    def insert_one(self, job):
        """Insert a New Job"""
        job = Job(
            name=job["name"],
            status=self.PENDING if job["interval"]["type"] == self.ONCE or job["interval"]["type"] == self.AFTER or job["interval"]["type"] == self.ONCE_AT else self.DAEMON,
            last_status=self.PENDING if job["interval"]["type"] == self.ONCE or job["interval"]["type"] == self.AFTER or job["interval"]["type"] == self.ONCE_AT else self.DAEMON,
            executor=job["executor"],
            parameters=json.dumps(job["parameters"]),
            interval=json.dumps(job["interval"]),
            retry_count=job["retry_count"] if "retry_count" in job else 0,
            trials=job["trials"] if "trials" in job else 5,
            priority=job["priority"] if "priority" in job else 1,
            last_run=job["last_run"] if "last_run" in job else None,
            run_at=job["run_at"] if "run_at" in job else self.get_run_at(job["interval"]),
            locked=job["locked"] if "locked" in job else False,
        )
        job.save()
        return False if job.pk is None else job


    def insert_many(self, jobs):
        """Insert Many Jobs"""
        status = True
        for job in jobs:
            status &= True if self.insert_one(job) != False else False
        return status


    def get_one_by_id(self, id):
        """Get Job By ID"""
        try:
            job = Job.objects.get(pk=id)
            return False if job.pk is None else job
        except:
            return False


    def get_one_to_run(self):
        """Get Job To Run"""
        try:
            job = Job.objects.filter(status__in=["pending","daemon"], run_at__lt=timezone.now(), locked=False).order_by("priority").first()
            # Lock the Job
            if not job.pk is None:
                job.locked = True
                job.save()
            return False if job.pk is None else job
        except:
            return False


    def update_one_by_id(self, id, new_data):
        """Update Job By ID"""
        job = self.get_one_by_id(id)
        if job != False:
            if "name" in new_data:
                job.name = new_data["name"]
            if "status" in new_data:
                job.status = new_data["status"]
            if "last_status" in new_data:
                job.last_status = new_data["last_status"]
            if "executor" in new_data:
                job.executor = new_data["executor"]
            if "parameters" in new_data:
                job.parameters = new_data["parameters"]
            if "interval" in new_data:
                job.interval = new_data["interval"]
            if "retry_count" in new_data:
                job.retry_count = new_data["retry_count"]
            if "trials" in new_data:
                job.trials = new_data["trials"]
            if "priority" in new_data:
                job.priority = new_data["priority"]
            if "last_run" in new_data:
                job.last_run = new_data["last_run"]
            if "run_at" in new_data:
                job.run_at = new_data["run_at"]
            if "locked" in new_data:
                job.locked = new_data["locked"]
            job.save()
            return True
        return False


    def update_after_run(self, job, status):
        """Update Job According To Status"""
        job_data = {"last_run": timezone.now(), "retry_count": (job.retry_count + 1), "last_status": status, "locked": False}

        if job.status == "pending":
            if status == self.PASSED:
                job_data["status"] = self.PASSED
            elif status == self.FAILED:
                if (job.retry_count + 1) >= job.trials:
                    job_data["status"] = self.FAILED
                else:
                    job_data["status"] = self.PENDING
            elif status == self.ERROR:
                job_data["status"] = self.ERROR
        elif job.status == "daemon":
            job_data["run_at"] = self.get_run_at(job.interval)

        return self.update_one_by_id(job.pk, job_data)


    def delete_one_by_id(self, id):
        """Delete Job By ID"""
        job = self.get_one_by_id(id)
        if job != False:
            count, deleted = job.delete()
            return True if count > 0 else False
        return False


    def get_run_at(self, interval):
        """Get Run at Datetime"""
        if interval["type"] == self.ONCE:
            return timezone.now()

        if interval["type"] == self.ONCE_AT:
            return interval["datetime"]

        if interval["type"] == self.AFTER:
            datetime = timezone.now()
            for key, value in interval.items():
                if key == "microseconds":
                    datetime += timedelta(microseconds=value)
                elif key == "milliseconds":
                    datetime += timedelta(milliseconds=value)
                elif key == "seconds":
                    datetime += timedelta(seconds=value)
                elif key == "minutes":
                    datetime += timedelta(minutes=value)
                elif key == "hours":
                    datetime += timedelta(hours=value)
                elif key == "days":
                    datetime += timedelta(days=value)
                elif key == "weeks":
                    datetime += timedelta(weeks=value)
                elif key == "months":
                    datetime += timedelta(days=value * 30)
                elif key == "years":
                    datetime += timedelta(days=value * 360)
            return datetime

        if interval["type"] == self.EVERY:
            datetime = timezone.now()
            for key, value in interval.items():
                if key == "microseconds":
                    datetime += timedelta(microseconds=value)
                elif key == "milliseconds":
                    datetime += timedelta(milliseconds=value)
                elif key == "seconds":
                    datetime += timedelta(seconds=value)
                elif key == "minutes":
                    datetime += timedelta(minutes=value)
                elif key == "hours":
                    datetime += timedelta(hours=value)
                elif key == "days":
                    datetime += timedelta(days=value)
                elif key == "weeks":
                    datetime += timedelta(weeks=value)
                elif key == "months":
                    datetime += timedelta(days=value * 30)
                elif key == "years":
                    datetime += timedelta(days=value * 360)
            return datetime

        return None