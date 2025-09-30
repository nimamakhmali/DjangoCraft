from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Service


@receiver(post_save, sender=Service)
def notify_service_moderation(sender, instance: Service, created: bool, **kwargs):
	if created:
		return
	# Only notify on status changes to approved/rejected
	if instance.status == Service.STATUS_APPROVED and instance.approved_at:
		_subject = "Your service has been approved"
		_message = f"Your service '{instance.title}' has been approved."
		_recipients = [getattr(getattr(instance, 'owner', None), 'email', None)]
		_recipients = [e for e in _recipients if e]
		if _recipients:
			send_mail(
				subject=_subject,
				message=_message,
				from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'no-reply@example.com'),
				recipient_list=_recipients,
				fail_silently=True,
			)
	elif instance.status == Service.STATUS_REJECTED:
		_subject = "Your service has been rejected"
		_reason = instance.rejection_reason or "No reason provided"
		_message = f"Your service '{instance.title}' was rejected. Reason: {_reason}"
		_recipients = [getattr(getattr(instance, 'owner', None), 'email', None)]
		_recipients = [e for e in _recipients if e]
		if _recipients:
			send_mail(
				subject=_subject,
				message=_message,
				from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'no-reply@example.com'),
				recipient_list=_recipients,
				fail_silently=True,
			)
