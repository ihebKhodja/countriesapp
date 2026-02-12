from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Count, Sum
from .models import Country


def country_list(request):
    """List all countries with pagination, region filter, and name search."""
    queryset = Country.objects.all().order_by('common_name')

    # Region filter
    region = request.GET.get('region', '')
    if region:
        queryset = queryset.filter(region=region)

    # Search by name
    search = request.GET.get('search', '')
    if search:
        queryset = queryset.filter(common_name__icontains=search)

    # All distinct regions for the filter dropdown
    regions = Country.objects.values_list('region', flat=True).distinct().order_by('region')
    regions = [r for r in regions if r]

    # Pagination (15 per page)
    paginator = Paginator(queryset, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'regions': regions,
        'current_region': region,
        'search': search,
    }
    return render(request, 'country_list.html', context)


def country_detail(request, cca3):
    """Detail view for a single country."""
    country = get_object_or_404(Country, cca3=cca3.upper())
    return render(request, 'country_detail.html', {'country': country})


def stats(request):
    """Statistics page."""
    total_countries = Country.objects.count()
    total_population = Country.objects.aggregate(total=Sum('population'))['total'] or 0
    total_area = Country.objects.aggregate(total=Sum('area'))['total'] or 0

    top_population = Country.objects.filter(population__isnull=False).order_by('-population')[:10]
    top_area = Country.objects.filter(area__isnull=False).order_by('-area')[:10]

    region_stats = (
        Country.objects.filter(region__isnull=False)
        .exclude(region='')
        .values('region')
        .annotate(
            count=Count('id'),
            total_population=Sum('population'),
            total_area=Sum('area'),
        )
        .order_by('-count')
    )

    context = {
        'total_countries': total_countries,
        'total_population': total_population,
        'total_area': total_area,
        'top_population': top_population,
        'top_area': top_area,
        'region_stats': region_stats,
    }
    return render(request, 'stats.html', context)
