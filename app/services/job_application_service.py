# app/services/job_application_service.py
from app.repositories.job_application_repository import JobApplicationRepository
from app.models.member import Member
from app.models.job import Job
from werkzeug.exceptions import BadRequest

class JobApplicationService:
    @staticmethod
    def apply_for_job(member_id, job_id, resume, cover_letter=None):
        # Check if the member and job exist
        member = Member.query.get(member_id)
        if not member:
            raise BadRequest('Invalid member.')

        job = Job.query.get(job_id)
        if not job:
            raise BadRequest('Invalid job.')

        # Validate the resume (it should be non-empty)
        if not resume:
            raise BadRequest('Resume is required.')

        # Create the job application
        application_data = {
            'resume': resume,
            'cover_letter': cover_letter,
            'member_id': member_id,
            'job_id': job_id
        }
        return JobApplicationRepository.create_application(application_data)
