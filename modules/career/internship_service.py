from modules.database.models import Internship


def create_internship(db, user_id, company_name, role, description, location, work_mode, skills, application_deadline, application_url):
	internship = Internship(
		user_id=user_id,
		company_name=company_name.strip(),
		role=role.strip(),
		description=description.strip(),
		location=location.strip(),
		work_mode=work_mode,
		skills=skills.strip(),
		application_deadline=application_deadline,
		application_url=application_url.strip(),
		status="Saved",
	)
	db.add(internship)
	db.commit()
	db.refresh(internship)
	return internship


def get_internships(db, user_id, search="", status="All"):
	query = db.query(Internship).filter(Internship.user_id == user_id)
	if search.strip():
		term = f"%{search.strip()}%"
		query = query.filter(
			(Internship.company_name.ilike(term))
			| (Internship.role.ilike(term))
			| (Internship.skills.ilike(term))
		)
	if status != "All":
		query = query.filter(Internship.status == status)
	return query.order_by(Internship.application_deadline.asc(), Internship.id.desc()).all()


def get_internship(db, user_id, internship_id):
	return (
		db.query(Internship)
		.filter(Internship.id == internship_id, Internship.user_id == user_id)
		.first()
	)


def update_internship_status(db, user_id, internship_id, status):
	internship = get_internship(db, user_id, internship_id)
	if internship:
		internship.status = status
		db.commit()
		db.refresh(internship)
	return internship
