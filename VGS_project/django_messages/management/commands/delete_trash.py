from django.core.management.base import BaseCommand
from django_messages.models import Message

class Command(BaseCommand):
    help = "Deletes messages in trash"

    def handle(self, *args, **options):
        Message.objects.del_trash().delete()