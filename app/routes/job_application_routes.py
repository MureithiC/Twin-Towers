# app/routes/job_application_routes.py
from flask import Blueprint
from flask_restful import Api
from app.controllers.job_application_controller import JobApplicationResource

# Define a Blueprint for job applications
job_application_bp = Blueprint('job_application_bp', __name__)
job_application_api = Api(job_application_bp)

# Register the job application resource
job_application_api.add_resource(JobApplicationResource, '/jobs/<int:job_id>/apply')
