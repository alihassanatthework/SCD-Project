from django.core.management.base import BaseCommand
from accounts.models import User

class Command(BaseCommand):
    help = 'Creates the initial admin user with fixed credentials'

    def handle(self, *args, **options):
        if User.objects.filter(user_type='admin').exists():
            self.stdout.write(self.style.WARNING('Admin user already exists.'))
            return

        try:
            admin = User.objects.create_user(
                username='admin',
                email='admin@jobportal.com',
                password='admin123',
                user_type='admin',
                is_staff=True,
                is_superuser=True
            )
            self.stdout.write(self.style.SUCCESS('Successfully created admin user'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error creating admin user: {str(e)}')) 