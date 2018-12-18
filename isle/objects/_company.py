import copy
from typing import List

import isle._urls as URL
import isle.objects._tmdb as _tmdb_obj
import isle.objects._others as other_objs

from .._config import tmdb_api_key


__all__ = ["Company"]


class Company(_tmdb_obj.TMDb):
    """Represents a company."""

    def _init(self):
        self.get_details()

    def _getdata(self, key):
        if key not in self.data:
            if key == "alternative_names":
                self.get_alternative_names()
            elif key == "images":
                self.get_images()
            else:
                self._init()
        return copy.deepcopy(self.data[key])

    @property
    def name(self):
        """Return the name of a company."""
        return self._getdata("name")

    @property
    def also_known_as(self):
        """Return alternative names of a company."""
        names = []
        for item in self._getdata("alternative_names")["results"]:
            names.append(item["name"])
        return names

    @property
    def description(self):
        """Return a company's description."""
        return self._getdata("description")

    @property
    def homepage(self):
        """Return a company's homepage."""
        return self._getdata("homepage")

    @property
    def country(self):
        """Return a company's origin country."""
        code = self._getdata("origin_country")
        if code:
            try:
                english_name = self._all_countries[code]
            except AttributeError:
                self._all_countries = self._get_all_countries()
                english_name = self._all_countries[code]
            return other_objs.Country(
                iso_3166_1=code, english_name=english_name
            )
        else:
            return code

    @property
    def parent_company(self):
        # TODO: definition
        return self._getdata("parent_company")

    @property
    def logos(self):
        """Return logo images that belong to a comapny. Each item
        is an instance of the `Image` class."""
        logos = []
        for item in self._getdata("images")["logos"]:
            logos.append(other_objs.Image(item, type_="logo"))
        return logos

    def _get_all_countries(self):
        data = self._request(
            URL.COUNTRIES_CONFIGURATION, **{"api_key": tmdb_api_key()}
        )
        countries = {}
        for item in data:
            countries[item["iso_3166_1"]] = item["english_name"]
        return countries

    def get_details(self, **params):
        """Get a companies details."""
        details = self._request(
            URL.COMPANY_DETAILS.format(company_id=self.tmdb_id), **params
        )
        self.data.update(details)
        return details

    def get_alternative_names(self, **params):
        """Get the alternative names of a company."""
        alternative_names = self._request(
            URL.COMPANY_ALTERNATIVE_NAMES.format(company_id=self.tmdb_id),
            **params
        )
        self.data.update({"alternative_names": alternative_names})
        return alternative_names

    def get_images(self, **params):
        """Get a companies logos."""
        images = self._request(
            URL.COMPANY_IMAGES.format(company_id=self.tmdb_id), **params
        )
        self.data.update({"images": images})
        return images
