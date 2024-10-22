# app/repositories/job_application_repository.py
from app import db
from app.models.job_application import JobApplication

class JobApplicationRepository:
    @staticmethod
    def create_application(data):
        application = JobApplication(
            resume=data['resume'],
            cover_letter=data.get('cover_letter', ''),
            member_id=data['member_id'],
            job_id=data['job_id']
        )
        db.session.add(application)
        db.session.commit()
        return application

    @staticmethod
    def get_application_by_id(application_id):
        return JobApplication.query.get(application_id)
