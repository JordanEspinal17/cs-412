import os
import csv
from datetime import datetime
from django.conf import settings
from django.db import models


class Voter(models.Model):  # Correct inheritance
    last_name = models.TextField()
    first_name = models.TextField()
    street_number = models.CharField(max_length=10)
    street_name = models.TextField()
    apartment_number = models.CharField(max_length=10, blank=True, null=True)
    zip_code = models.CharField(max_length=10)
    date_of_birth = models.DateField()
    date_of_registration = models.DateField()
    party_affiliation = models.TextField()
    precinct_number = models.TextField()
    v20state = models.BooleanField(default=False)
    v21town = models.BooleanField(default=False)
    v21primary = models.BooleanField(default=False)
    v22general = models.BooleanField(default=False)
    v23town = models.BooleanField(default=False)
    voter_score = models.IntegerField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}, Precinct {self.precinct_number}"


def load_data():
    """Function to load data records from the CSV file into Django model instances."""
    # Remove existing records to prevent duplicates
    Voter.objects.all().delete()

    # File path to the data
    file_path = os.path.join(settings.BASE_DIR, 'voter_analytics', 'data', 'newton_voters.csv')

    # Open the CSV file and process its contents
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)

        for row in reader:
            try:
                # Create Voter instances
                voter = Voter(
                    last_name=row['Last Name'],
                    first_name=row['First Name'],
                    street_number=row['Residential Address - Street Number'],
                    street_name=row['Residential Address - Street Name'],
                    apartment_number=row.get('Residential Address - Apartment Number', None),
                    zip_code=row['Residential Address - Zip Code'],
                    date_of_birth=datetime.strptime(row['Date of Birth'], '%Y-%m-%d').date(),
                    date_of_registration=datetime.strptime(row['Date of Registration'], '%Y-%m-%d').date(),
                    party_affiliation=row['Party Affiliation'],
                    precinct_number=row['Precinct Number'],
                    v20state=row['v20state'].strip().upper() == 'TRUE',
                    v21town=row['v21town'].strip().upper() == 'TRUE',
                    v21primary=row['v21primary'].strip().upper() == 'TRUE',
                    v22general=row['v22general'].strip().upper() == 'TRUE',
                    v23town=row['v23town'].strip().upper() == 'TRUE',
                    voter_score=int(row['voter_score']),
                )
                voter.save()  # Save instance to the database

            except Exception as e:
                print(f"Error processing row: {row}")
                print(f"Exception: {e}")

    print(f"Done. Loaded {Voter.objects.count()} voter records.")
