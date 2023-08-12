from django.db import models
from django.core.exceptions import ValidationError

class Species(models.Model):
    name = models.CharField(max_length=100, unique=True, null=False, blank=False)
    ref_genome = models.CharField(max_length=200, unique=True, null=False, blank=False)
    img_src = models.ImageField(upload_to="media")
    
    class Meta:
        db_table = "gallery"


class Sample(models.Model):
    sample_name = models.CharField(max_length=200)
    collection_date = models.DateField()
    sequencing_date = models.DateField()
    species = models.ForeignKey(Species, on_delete=models.CASCADE, default='')
    tissue_name = models.CharField(max_length=50)
    def clean(self):
            if self.collection_date >= self.sequencing_date:
                raise ValidationError("Collection date must be earlier than sequencing date.")

class SNP(models.Model):
    snp_name = models.CharField(max_length=50, unique=True, null=False, blank=False)
    chromosome = models.IntegerField(null=True, blank=True)
    coordinate = models.IntegerField(null=True, blank=True)

    class Nucleotides(models.TextChoices):
        A = 'A'
        C = 'C'
        G = 'G'
        T = 'T'

    ref_allele = models.CharField(max_length=1, null=True, blank=True, choices=Nucleotides.choices)
    alter_allele = models.CharField(max_length=1, null=True, blank=True, choices=Nucleotides.choices)
    MAF = models.FloatField(default=0.0)
    species = models.ForeignKey(Species, on_delete=models.CASCADE, default='')
    class Meta:
        unique_together = [["chromosome", "coordinate", "alter_allele"]]

class Annotation(models.Model):
    sort = models.CharField(max_length=50)
    value = models.CharField(max_length=200)
    author = models.CharField(max_length=200, null=True, blank=True, default='')
    an_date = models.DateField(null=True, blank=True)
    snp = models.ForeignKey(SNP, on_delete=models.CASCADE, default='')
    class Meta:
        unique_together = [["sort", "snp"]]
       