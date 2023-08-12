# Generated by Django 4.2 on 2023-05-10 12:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Species',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('ref_genome', models.CharField(max_length=200, unique=True)),
                ('img_src', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='SNP',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('snp_name', models.CharField(max_length=50, unique=True)),
                ('chromosome', models.IntegerField(blank=True, null=True)),
                ('coordinate', models.IntegerField(blank=True, null=True)),
                ('ref_allele', models.CharField(blank=True, max_length=1, null=True)),
                ('alter_allele', models.CharField(blank=True, max_length=1, null=True)),
                ('MAF', models.FloatField(max_length=200)),
                ('species_name', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='snp.species')),
            ],
            options={
                'unique_together': {('chromosome', 'coordinate', 'alter_allele')},
            },
        ),
        migrations.CreateModel(
            name='Sample',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sample_name', models.CharField(max_length=200)),
                ('collection_date', models.DateField()),
                ('sequencing_date', models.DateField()),
                ('tissue_name', models.CharField(max_length=50)),
                ('species', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='snp.species')),
            ],
        ),
        migrations.CreateModel(
            name='Annotation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=50)),
                ('value', models.CharField(max_length=200)),
                ('author', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('an_date', models.DateField(blank=True, null=True)),
                ('snp', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='snp.snp')),
            ],
            options={
                'unique_together': {('type', 'snp')},
            },
        ),
    ]