# app/models/job_application.py
from app import db
from datetime import datetime

class JobApplication(db.Model):
    __tablename__ = 'job_application'

    id = db.Column(db.Integer, primary_key=True)
    resume = db.Column(db.String(255), nullable=False)
    cover_letter = db.Column(db.Text, nullable=True)
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    member = db.relationship('Member', backref='applications')
    job = db.relationship('Job', backref='applications')

    def to_dict(self):
        return {
            'id': self.id,
            'resume': self.resume,
            'cover_letter': self.cover_letter,
            'member_id': self.member_id,
            'job_id': self.job_id,
            'created_at': self.created_at
        }
