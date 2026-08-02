from modules.notifications.email_service import send_email

send_email(
    receiver="mangeshshinde61499@gmail.com",
    subject="🎉 AI Productivity Manager Test",
    body="""
Hello!

This is a test email from your AI Productivity Manager.

If you received this email, Gmail integration is working successfully.

Regards,
AI Productivity Manager
"""
)

print("Email function executed.")