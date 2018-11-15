from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from email.mime.image import MIMEImage
from django.conf import settings
import os


def forge_corporate_email(subject, html_body, text_body, to, extra_images={}, **kwargs):
    # related = MIMEMultipart("related")
    html_content = render_to_string('email/email.html', {'body': html_body, 'subject': subject, 'corp_color': '#642e99', 'BASE_URL': settings.BASE_URL})
    text_content = strip_tags(render_to_string('email/email_text.html', {'body': text_body, 'subject': subject, 'corp_color': '#642e99', 'BASE_URL': settings.BASE_URL}))

    if 'from_email' in kwargs:
        from_email = kwargs.pop('from_email')
    else:
        from_email = settings.DEFAULT_FROM_EMAIL

    email = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=from_email,
        to=to,
        **kwargs
    )

    email.attach_alternative(html_content, 'text/html')

    img = open(os.path.join(os.path.dirname(__file__), '..', '..', 'static', 'images', 'email-logo.png'), 'rb').read()
    logo_image = MIMEImage(img)
    logo_image.add_header('Content-ID', '<email-logo.png>')
    logo_image.add_header('Content-Disposition', 'inline', filename='email-logo.png')
    logo_image.add_header('Content-Type', 'image/png', name='email-logo.png')
    email.attach(logo_image)

    for img_id, img_path in extra_images.items():
        try:
            img = open(img_path, 'r').read()
            logo_image = MIMEImage(img)
            logo_image.add_header('Content-ID', '<{}>'.format(img_id))
            logo_image.add_header('Content-Disposition', 'inline', filename=img_id)
            subtype = 'jpeg'
            if img_path.lower().endswith('png'):
                subtype = 'png'
            logo_image.add_header('Content-Type', 'image/{}'.format(subtype), name=img_id)
            email.attach(logo_image)
        except:
            pass

    email.mixed_subtype = "related"
    return email


def send_email(subject, html_body, text_body, to, extra_images={}, skip_bcc=False, **kwargs):
    bcc = kwargs.pop('bcc', [])
    if not skip_bcc:
        bcc += settings.EMAILS_BCC_EMAILS
    email = forge_corporate_email(subject, html_body, text_body, to, bcc=bcc, extra_images={}, **kwargs)
    return email.send()
