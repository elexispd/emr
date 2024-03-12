# Import necessary modules
from django.core.management.base import BaseCommand
from faker import Faker
from emr.models import Staff, Department
from django.utils import timezone

class Command(BaseCommand):
    help = 'Seed data into the database'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Seeding data...'))

        fake = Faker()

        num_records_to_generate = 20
        
        department_id = fake.random_element(elements=(6, 7, 8))
        department = Department.objects.get(pk=department_id)
        

        for _ in range(num_records_to_generate):
            Staff.objects.create(
                first_name = fake.first_name(),
                last_name = fake.last_name(),
                email = fake.email(),
                # doctor_type = fake.random_element(elements=("Contract", "Permanent")),
                # doctor_specialization = fake.random_element(elements=("Surgeon", "General")),
                phone_number = fake.numerify(text='##########'),
                is_chief_consultant = fake.boolean(),
                is_store_keeper = fake.boolean(),              
                department=  department,
                date_joined = timezone.now(),
                updated_at = timezone.now(),
            )

        self.stdout.write(self.style.SUCCESS('Data seeding completed successfully.'))
