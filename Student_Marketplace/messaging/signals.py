from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Conversation, Notification
from orders.models import Order


@receiver(post_save, sender=Order)
def create_order_conversation(sender, instance, created, **kwargs):
	"""Automatically create a conversation when an order is created"""
	if created and instance.user:
		# Get the service owner (freelancer) from the first order item
		# In a real app, you'd get this from the service's owner
		# For now, we'll create a conversation with a placeholder user
		from django.contrib.auth.models import User
		
		# Find a freelancer user (in real app, get from service.owner)
		freelancer = User.objects.filter(
			profile__role='freelancer'
		).first()
		
		if freelancer and freelancer != instance.user:
			# Create conversation
			conversation = Conversation.objects.create(
				title=f"Order #{instance.id} - {instance.items.first().service_title if instance.items.exists() else 'Service'}",
				order=instance
			)
			conversation.participants.add(instance.user, freelancer)
			
			# Create notifications
			Notification.objects.create(
				user=instance.user,
				notification_type=Notification.NOTIFICATION_TYPE_ORDER,
				title="Order Created",
				message=f"Your order #{instance.id} has been created. You can now communicate with the service provider.",
				related_order=instance,
				related_conversation=conversation
			)
			
			Notification.objects.create(
				user=freelancer,
				notification_type=Notification.NOTIFICATION_TYPE_ORDER,
				title="New Order Received",
				message=f"You have received a new order #{instance.id}. Please check your dashboard.",
				related_order=instance,
				related_conversation=conversation
			)
