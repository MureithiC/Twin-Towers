from app import db

class Job(db.Model):
    __tablename__ = 'jobs'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(100), nullable=True)
    salary = db.Column(db.Float, nullable=True)
    posted_date = db.Column(db.DateTime, nullable=False)
    
    def __repr__(self):
        return f'<Job {self.title}>'
