# Generated by Django 4.2.4 on 2023-08-22 17:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("my_app", "0003_alter_comment_post_alter_comment_user_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Book",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=300)),
                ("price", models.IntegerField(default=0)),
            ],
            options={
                "default_related_name": "books",
            },
        ),
        migrations.CreateModel(
            name="Publisher",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name="Store",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=300)),
                ("books", models.ManyToManyField(to="my_app.book")),
            ],
            options={
                "default_related_name": "stores",
            },
        ),
        migrations.AddField(
            model_name="book",
            name="publisher",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="my_app.publisher"
            ),
        ),
    ]