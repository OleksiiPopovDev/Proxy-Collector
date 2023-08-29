from database.model.country_model import Country
from dto.country_dto import CountryDto


class CountryRepository:
    @staticmethod
    def save(country: CountryDto) -> None:
        Country.create(
            name=country.name,
            code=country.code,
            code_3=country.code_3,
            latitude=country.latitude,
            longitude=country.longitude
        )
