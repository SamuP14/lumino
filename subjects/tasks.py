import datetime
import os

from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django_rq import job
from weasyprint import HTML


@job
def deliver_certificate(base_url, request):
    context = {
        'student': request.user,
        'today': datetime.date.today(),
        'request': request,
    }

    certificate_html = render_to_string('subjects/marks/certificate_template.html', context)

    output_directory = settings.CERTIFICATE_DIR
    output_filename = f'{request.user.username}_grade_certificate.pdf'
    output_path = os.path.join(output_directory, output_filename)

    os.makedirs(output_directory, exist_ok=True)

    HTML(string=certificate_html, base_url=base_url).write_pdf(output_path)

    email_body = render_to_string('subjects/marks/email.html', {'student': request.user})

    email = EmailMessage(
        subject='Marks Certificate',
        body=email_body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[request.user.email],
    )
    email.content_subtype = 'html'
    email.attach_file(output_path)
    email.send()
