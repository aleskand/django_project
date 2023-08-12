from django.contrib import admin
from .models import Species, Sample, SNP, Annotation

admin.site.register(Species)
admin.site.register(Sample)
admin.site.register(SNP)
admin.site.register(Annotation)

