import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from flask import render_template
from website import BREVO_API_KEY, GMAIL_USER

def send_email(app, to_email, subject, template_name, **context):

    try:
        # give thread the Flask app
        with app.app_context():
            html_content = render_template(template_name, **context)

        configuration = sib_api_v3_sdk.Configuration()
        configuration.api_key['api-key'] = BREVO_API_KEY

        api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
            sib_api_v3_sdk.ApiClient(configuration)
        )

        email_data = sib_api_v3_sdk.SendSmtpEmail(
            to=[{"email": to_email}],
            sender={"email": GMAIL_USER, "name": "Jabir2233"},
            subject=subject,
            html_content=html_content
        )

        response = api_instance.send_transac_email(email_data)

        print(f"[MAIL OK] → {to_email}")

    except Exception as e:
        print(f"[MAIL ERROR] → {e}")