from plyer import notification


def show_notification(title, message):

    notification.notify(
        title=title,
        message=message,
        app_name="AI Productivity Manager",
        timeout=10
    )