# Import necessary modules
from django.core.management.base import BaseCommand
from faker import Faker
from emr.models import Patient
from django.utils import timezone

class Command(BaseCommand):
    help = 'Seed data into the database'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Seeding data...'))

        fake = Faker()

        num_records_to_generate = 100

        for _ in range(num_records_to_generate):
            Patient.objects.create(
                first_name = fake.first_name(),
                last_name = fake.last_name(),
                dob = fake.date_of_birth(),
                next_of_kin = fake.name(),
                phone_number = fake.numerify(text='##########'),
                address_of_kin = fake.address(),
                place_of_origin = fake.city(),
                mswd = fake.word(),
                xray_number = fake.random_number(digits=5),
                ethnic_group = fake.random_element(elements=("Asian", "Black", "Hispanic", "White")),
                occupation = fake.job(),
                religion = fake.random_element(elements=("Christianity", "Islam", "Hinduism", "Buddhism", "Other")),
                created_at = timezone.now(),
                updated_at = timezone.now(),
            )

        self.stdout.write(self.style.SUCCESS('Data seeding completed successfully.'))
