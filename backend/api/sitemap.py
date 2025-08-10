from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class StaticSitemap(Sitemap):
    protocol = "https"

    def items(self):
        return ["home-page-content", "technologies-list", "services-list"]

    def location(self, item):
        return reverse(item)
