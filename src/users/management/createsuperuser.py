from django.contrib.auth.management.commands.createsuperuser import Command as BaseCreateSuperuserCommand
from django.core.management import CommandError

class Command(BaseCreateSuperuserCommand):
    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument('--email', type=str, required=True, help='Email of the superuser')
        parser.add_argument('--first_name', type=str, required=True, help='First name of the superuser')
        parser.add_argument('--last_name', type=str, required=True, help='Last name of the superuser')

    def handle(self, *args, **options):
        email = options.get('email')
        first_name = options.get('first_name')
        last_name = options.get('last_name')
        password = options.get('password')
        
        if not email:
            raise CommandError("Email is required")
        if not first_name:
            raise CommandError("First name is required")
        if not last_name:
            raise CommandError("Last name is required")

        # Avoid duplicate email issues
        User = self.UserModel
        if User.objects.filter(email=email).exists():
            raise CommandError("This email is already used")

        superuser = User(email=email, first_name=first_name, last_name=last_name)
        if password:
            superuser.set_password(password)
        superuser.is_staff = True
        superuser.is_superuser = True
        superuser.save()

        self.stdout.write(self.style.SUCCESS(f"Superuser created successfully: {email}"))