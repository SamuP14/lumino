import weasyprint
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django_rq import job


@job
def deliver_certificate(base_url, student):
    pdf_filename = f'{student.username}_grade_certificate.pdf'

    html_content = render_to_string(
        'subjects/marks/certificate_template.html',
        {
            'student': student,
        },
    )

    pdf = weasyprint.HTML(string=html_content).write_pdf()

    file_path = settings.CERTIFICATE_DIR / pdf_filename
    with open(file_path, 'wb') as f:
        f.write(pdf)

    subject = 'Your Grade Certificate'
    message = 'Please find attached your grade certificate.'
    email = EmailMessage(subject, message, settings.DEFAULT_FROM_EMAIL, [student.email])
    email.attach(pdf_filename, pdf, 'application/pdf')

    email.send()
