# app/controllers/job_application_controller.py
from flask import request, Blueprint
from flask_restful import Resource, Api
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.job_application_service import JobApplicationService
from werkzeug.exceptions import BadRequest

job_application_bp = Blueprint('job_application_bp', __name__)
job_application_api = Api(job_application_bp)

class JobApplicationResource(Resource):
    @jwt_required()
    def post(self, job_id):
        """ Apply for a job """
        current_user = get_jwt_identity()

        # Get application data from the request
        data = request.get_json()
        resume = data.get('resume')
        cover_letter = data.get('cover_letter', '')

        try:
            application = JobApplicationService.apply_for_job(
                member_id=current_user['id'],
                job_id=job_id,
                resume=resume,
                cover_letter=cover_letter
            )
        except BadRequest as e:
            return {"error": str(e)}, 400

        # TODO: Add logic to send email notifications to both member and employer
        
        return application.to_dict(), 201

# Add the resource to the API
job_application_api.add_resource(JobApplicationResource, '/jobs/<int:job_id>/apply')
