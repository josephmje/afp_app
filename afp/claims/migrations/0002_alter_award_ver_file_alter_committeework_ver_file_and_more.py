# Generated by Django 4.1 on 2022-12-02 21:08

import afp.claims.mixins
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("claims", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="award",
            name="ver_file",
            field=afp.claims.mixins.ContentTypeRestrictedFileField(
                blank=True,
                null=True,
                upload_to=afp.claims.mixins.user_directory_path,
                verbose_name="Verification File",
            ),
        ),
        migrations.AlterField(
            model_name="committeework",
            name="ver_file",
            field=afp.claims.mixins.ContentTypeRestrictedFileField(
                blank=True,
                null=True,
                upload_to=afp.claims.mixins.user_directory_path,
                verbose_name="Verification File",
            ),
        ),
        migrations.AlterField(
            model_name="cpa",
            name="cpa_file",
            field=afp.claims.mixins.ContentTypeRestrictedFileField(
                blank=True,
                null=True,
                upload_to=afp.claims.mixins.user_directory_path,
                verbose_name="CPA File",
            ),
        ),
        migrations.AlterField(
            model_name="cpa",
            name="ver_file",
            field=afp.claims.mixins.ContentTypeRestrictedFileField(
                blank=True,
                null=True,
                upload_to=afp.claims.mixins.user_directory_path,
                verbose_name="Verification File",
            ),
        ),
        migrations.AlterField(
            model_name="editorialboard",
            name="ver_file",
            field=afp.claims.mixins.ContentTypeRestrictedFileField(
                blank=True,
                null=True,
                upload_to=afp.claims.mixins.user_directory_path,
                verbose_name="Verification File",
            ),
        ),
        migrations.AlterField(
            model_name="exam",
            name="ver_file",
            field=afp.claims.mixins.ContentTypeRestrictedFileField(
                blank=True,
                null=True,
                upload_to=afp.claims.mixins.user_directory_path,
                verbose_name="Verification File",
            ),
        ),
        migrations.AlterField(
            model_name="grant",
            name="ver_file",
            field=afp.claims.mixins.ContentTypeRestrictedFileField(
                blank=True,
                null=True,
                upload_to=afp.claims.mixins.user_directory_path,
                verbose_name="Verification File",
            ),
        ),
        migrations.AlterField(
            model_name="grantreview",
            name="ver_file",
            field=afp.claims.mixins.ContentTypeRestrictedFileField(
                blank=True,
                null=True,
                upload_to=afp.claims.mixins.user_directory_path,
                verbose_name="Verification File",
            ),
        ),
        migrations.AlterField(
            model_name="lecture",
            name="ver_file",
            field=afp.claims.mixins.ContentTypeRestrictedFileField(
                blank=True,
                null=True,
                upload_to=afp.claims.mixins.user_directory_path,
                verbose_name="Verification File",
            ),
        ),
        migrations.AlterField(
            model_name="promotion",
            name="ver_file",
            field=afp.claims.mixins.ContentTypeRestrictedFileField(
                blank=True,
                null=True,
                upload_to=afp.claims.mixins.user_directory_path,
                verbose_name="Verification File",
            ),
        ),
        migrations.AlterField(
            model_name="publication",
            name="ver_file",
            field=afp.claims.mixins.ContentTypeRestrictedFileField(
                blank=True,
                null=True,
                upload_to=afp.claims.mixins.user_directory_path,
                verbose_name="Verification File",
            ),
        ),
        migrations.AlterField(
            model_name="supervision",
            name="ver_file",
            field=afp.claims.mixins.ContentTypeRestrictedFileField(
                blank=True,
                null=True,
                upload_to=afp.claims.mixins.user_directory_path,
                verbose_name="Verification File",
            ),
        ),
    ]
