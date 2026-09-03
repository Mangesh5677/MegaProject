from datetime import date

from modules.database.models import Internship, InternshipApplication


def apply_for_internship(db, user_id, internship_id, notes=""):
	internship = (
		db.query(Internship)
		.filter(Internship.id == internship_id, Internship.user_id == user_id)
		.first()
	)
	if internship is None:
		return None, False

	application = (
		db.query(InternshipApplication)
		.filter(
			InternshipApplication.user_id == user_id,
			InternshipApplication.internship_id == internship_id,
		)
		.first()
	)
	if application:
		return application, False

	application = InternshipApplication(
		user_id=user_id,
		internship_id=internship_id,
		applied_date=date.today(),
		status="Applied",
		notes=notes.strip(),
	)
	db.add(application)
	db.commit()
	db.refresh(application)
	return application, True


def get_applications(db, user_id):
	return (
		db.query(InternshipApplication)
		.filter(InternshipApplication.user_id == user_id)
		.order_by(InternshipApplication.applied_date.desc(), InternshipApplication.id.desc())
		.all()
	)


def update_application(db, user_id, application_id, status, interview_date, notes):
	application = (
		db.query(InternshipApplication)
		.filter(
			InternshipApplication.id == application_id,
			InternshipApplication.user_id == user_id,
		)
		.first()
	)
	if application:
		application.status = status
		application.interview_date = interview_date
		application.notes = notes.strip()
		db.commit()
		db.refresh(application)
	return application
