import io
from unittest.mock import patch
import pytest
from django.core.management import call_command
from django.urls import reverse
from django.test import Client
from .models import Country
from django.core.exceptions import ValidationError
import pytest
from django.urls import reverse
from django.test import Client
from .models import Country
from django.core.exceptions import ValidationError

pytestmark = pytest.mark.django_db

  
@pytest.fixture
def client():
	return Client()

@pytest.fixture
def countries():
	Country.objects.create(cca3='FRA', cca2='FR', common_name='France', region='Europe', population=67000000, area=640000)
	Country.objects.create(cca3='USA', cca2='US', common_name='United States', region='Americas', population=331000000, area=9834000)
	Country.objects.create(cca3='JPN', cca2='JP', common_name='Japan', region='Asia', population=125000000, area=377975)
	Country.objects.create(cca3='ESP', cca2='ES', common_name='Spain', region='Europe', population=47000000, area=505990)
	Country.objects.create(cca3='BRA', cca2='BR', common_name='Brazil', region='Americas', population=212000000, area=8515767)

	for i in range(20):
		cca3 = f'T{i:02}' if i < 10 else f'T{i:02}'[:3]  # always 3 chars max
		# Generate unique cca2: e.g. T0, T1, ..., T9, U0, U1, ...
		first = chr(65 + (i // 10))  # A, B, C, ...
		second = str(i % 10)
		cca2 = f'{first}{second}'
		Country.objects.create(cca3=cca3, cca2=cca2, common_name=f'Test{i}', region='TestRegion', population=1000+i, area=100+i)

def test_import_countries_command(db):
	mock_response = [
		{
			"name": {"common": "Testland", "official": "Republic of Testland"},
			"cca2": "TL",
			"cca3": "TST",
			"capital": ["Test City"],
			"region": "TestRegion",
			"subregion": "TestSubregion",
			"population": 123456,
			"area": 654321.0,
			"flags": {"png": "http://example.com/flag.png"},
			"currencies": {"TST": {"name": "Test Dollar", "symbol": "$"}},
		}
	]
	class MockResponse:
		def __init__(self, json_data):
			self._json = json_data
			self.status_code = 200
		def json(self):
			return self._json
		def raise_for_status(self):
			pass

	with patch("requests.get", return_value=MockResponse(mock_response)):
		out = io.StringIO()
		call_command("import_countries", stdout=out)
		assert Country.objects.filter(cca3="TST").exists()
		country = Country.objects.get(cca3="TST")
		assert country.common_name == "Testland"
		assert country.official_name == "Republic of Testland"
		assert country.cca2 == "TL"
		assert country.capital == "Test City"
		assert country.region == "TestRegion"
		assert country.population == 123456
		assert country.area == 654321.0

def test_country_list_pagination(client, countries):
	url = reverse('country_list')
	response = client.get(url)
	assert response.status_code == 200
	assert 'page_obj' in response.context
	assert response.context['page_obj'].paginator.num_pages >= 2

def test_country_list_region_filter(client, countries):
	url = reverse('country_list')
	response = client.get(url, {'region': 'Europe'})
	assert response.status_code == 200
	assert all(c.region == 'Europe' for c in response.context['page_obj'])

def test_country_list_search(client, countries):
	url = reverse('country_list')
	response = client.get(url, {'search': 'France'})
	assert response.status_code == 200
	assert any('France' in c.common_name for c in response.context['page_obj'])

def test_country_list_regions(client, countries):
	url = reverse('country_list')
	response = client.get(url)
	regions = response.context['regions']
	assert 'Europe' in regions
	assert 'Americas' in regions
	assert 'Asia' in regions

def test_country_detail_existing(client, countries):
	url = reverse('country_detail', args=['FRA'])
	response = client.get(url)
	assert response.status_code == 200
	assert 'country' in response.context
	assert response.context['country'].cca3 == 'FRA'

def test_country_detail_404(client):
	url = reverse('country_detail', args=['XXX'])
	response = client.get(url)
	assert response.status_code == 404

def test_stats_view(client, countries):
	url = reverse('stats')
	response = client.get(url)
	assert response.status_code == 200
	assert response.context['total_countries'] == Country.objects.count()
	expected_population = sum(c.population for c in Country.objects.all())
	expected_area = sum(c.area for c in Country.objects.all())
	assert response.context['total_population'] == pytest.approx(expected_population)
	assert response.context['total_area'] == pytest.approx(expected_area)
	assert len(response.context['top_population']) <= 10
	assert len(response.context['top_area']) <= 10
	assert response.context['region_stats']

def test_country_model_creation():
	country = Country.objects.create(cca3='DEU', cca2='DE', common_name='Germany', region='Europe', population=83000000, area=357022)
	assert country.pk is not None
	assert country.cca3 == 'DEU'
	assert country.cca2 == 'DE'
	assert country.common_name == 'Germany'
	assert country.region == 'Europe'
	assert country.population == 83000000
	assert country.area == 357022

def test_country_model_required_fields():
	country = Country(cca3='NOR', cca2='NO')  
	with pytest.raises(ValidationError):
		country.full_clean()

def test_urls(client):
	urls = [
		reverse('country_list'),
		reverse('country_detail', args=['FRA']),
		reverse('stats'),
		reverse('home'),
	]
	for url in urls:
		response = client.get(url)
		assert response.status_code in [200, 404] 
