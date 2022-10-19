# Generated by Django 4.1.2 on 2022-10-18 09:05

import django.db.models.deletion
import mptt.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("forum", "0001_initial"),
        ("forum_conversation", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="forum",
            name="last_post",
            field=models.ForeignKey(
                blank=True,
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="forum_conversation.post",
                verbose_name="Last post",
            ),
        ),
        migrations.AddField(
            model_name="forum",
            name="parent",
            field=mptt.fields.TreeForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="children",
                to="forum.forum",
                verbose_name="Parent",
            ),
        ),
    ]
