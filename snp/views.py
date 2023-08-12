from django.shortcuts import redirect
from django.http import HttpResponse
from django.template import loader
import csv
from .models import Species, Sample, SNP, Annotation
from django.core.paginator import Paginator, EmptyPage
from .forms import AnnotationForm
from datetime import date


def home(request):
    template = loader.get_template("snp/home.html")
    species_count = Species.objects.count()
    samples_count = Sample.objects.count()
    snps_count = SNP.objects.count()
    context = {
        'species_count': species_count,
        'samples_count': samples_count,
        'snps_count': snps_count,
    }
    return HttpResponse(template.render(context, request))

def index(request):
    template = loader.get_template("snp/index.html")

    if request.GET.get("region") != None:
        region = request.GET.get("region")
        chromosome = None
        start_position = None
        end_position = None

        if ":" in region and "-" in region:
            chromosome, position_range = region.split(":")
            start_position, end_position = position_range.split("-")
        elif ":" in region:
            chromosome, position = region.split(":")
            start_position = end_position = position
    else:
        chromosome = request.GET.get("region")
        start_position = None
        end_position = None

    query = SNP.objects.all()

    if chromosome:
        query = query.filter(chromosome=chromosome)

    if start_position and end_position:
        query = query.filter(coordinate__range=(start_position, end_position))

    if request.GET.get("max_maf"):
        query = query.filter(MAF__lte=float(request.GET.get("max_maf")))
    if request.GET.get("min_maf"):
        query = query.filter(MAF__gte=float(request.GET.get("min_maf")))


    snps_with_annotations = []
    for x in query:
        temp = x.__dict__
        if len(Annotation.objects.filter(snp_id=x.id)) != 0:
            temp["annotation"] = True
        else:
            temp["annotation"] = False
        snps_with_annotations.append(temp)
    
    paginator = Paginator(snps_with_annotations, per_page=4)

    page = request.GET.get("page")
    if page is not None:
        page_number = page.split(" %")[0]
    else:
        page_number = 1

    try:
        page_object = paginator.get_page(page_number)
    except EmptyPage:
        page_object = paginator.get_page(1)

    context = {
        'species_list': Species.objects.all(),
        'snps_with_annotations': snps_with_annotations,
        'page_obj': page_object
    }

    return HttpResponse(template.render(context, request))



def export_csv(request):
    items = SNP.objects.all()

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="export.csv"'

    writer = csv.writer(response)
    writer.writerow(['Chromosome', 'Position', 'REF Alelle', 'ALT Alelle', 'MAF'])  

    for item in items:
        writer.writerow([item.chromosome, item.coordinate, item.ref_allele, item.alter_allele, item.MAF])

    return response


def species_details(request, id):
    template = loader.get_template("snp/species_details.html")
    name = Species.objects.filter(id=id)[0].name

    context = {
        'name': name,
        'snps': SNP.objects.filter(species=id)
    }

    return HttpResponse(template.render(context, request))

from .forms import AnnotationForm

def annotation_details(request, id):
    snp = SNP.objects.get(id=id)

    if request.method == 'POST':
        form = AnnotationForm(request.POST)
        if form.is_valid():
            annotation = form.save(commit=False)
            annotation.snp = snp
            annotation.an_date = date.today()
            annotation.save()
            return redirect('annotation_details', id=id)
    else:
        form = AnnotationForm(initial={'snp': snp})

    template = loader.get_template("snp/annotation_details.html")

    context = {
        'snp_id': id,
        'snp': snp,
        'annotations': Annotation.objects.filter(snp=snp),
        'form': form
    }

    return HttpResponse(template.render(context, request))
