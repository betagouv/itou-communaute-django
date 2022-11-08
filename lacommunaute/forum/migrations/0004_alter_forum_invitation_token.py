# Generated by Django 4.1.3 on 2022-11-03 13:50

import uuid

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("forum", "0003_forum_invitation_token_forum_members_group"),
    ]

    operations = [
        migrations.AlterField(
            model_name="forum",
            name="invitation_token",
            field=models.UUIDField(default=uuid.uuid4, unique=True),
        ),
    ]