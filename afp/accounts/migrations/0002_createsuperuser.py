from django.contrib.auth import get_user_model
from django.db import migrations

import google.auth
from google.cloud import secretmanager as sm

# This data migration allows you to programatically create a django admin user
# This will run in Cloud Build, which requires Cloud Build to have access to the secret.


def createsuperuser(apps, schema_editor):

    # Retrieve secret from Secret Manager
    _, project = google.auth.default()
    client = sm.SecretManagerServiceClient()
    name = f"projects/{project}/secrets/superuser_password/versions/latest"
    superuser_password = client.access_secret_version(
        name=name
    ).payload.data.decode("UTF-8")

    # Create a new user using acquired password
    User = get_user_model()
    User.objects.create_superuser(
        username="admin",
        email="info@afp-fmc-camh.ca",
        password=superuser_password,
    )


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [migrations.RunPython(createsuperuser)]
