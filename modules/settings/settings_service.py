from modules.database.models import Settings


def get_settings(db, user_id):

    settings = (
        db.query(Settings)
        .filter(Settings.user_id == user_id)
        .first()
    )

    if settings is None:

        settings = Settings(user_id=user_id)

        db.add(settings)
        db.commit()
        db.refresh(settings)

    return settings


def save_settings(db, settings):

    db.add(settings)
    db.commit()
    db.refresh(settings)