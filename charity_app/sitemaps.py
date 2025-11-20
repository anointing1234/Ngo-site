from django.contrib.sitemaps import Sitemap
from django.urls import reverse

class StaticViewSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return ["home", "about_us", "projects", "donate", "contact"]

    def location(self, item):
        return reverse(item)
