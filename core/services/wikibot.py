import random
import time

import pywikibot
import mwparserfromhell

from django.conf import settings
from pywikibot.exceptions import IsRedirectPageError

from core.models import WikiPage


class WikiWanderBot(object):
    def __init__(self, lang="en", wiki="wikipedia"):
        self.site = pywikibot.Site(lang, wiki)  # The site we want to run our bot on

    def is_valid_link(self, link):
        # Filter out images, categories, and non-internal links
        return not str(link.title).startswith(
            (
                "File:",
                "Category:",
                "Talk:",
                "User:",
                "Template:",
                "Help:",
                "Portal:",
                "Draft:",
                "TimedText:",
                "MediaWiki:",
                "Module:",
                "Special:",
            )
        )

    def find_related_pages(self, base: str):
        page = pywikibot.Page(self.site, base)

        text = page.get()

        parsed = mwparserfromhell.parse(text)

        links = []

        for node in parsed.filter_wikilinks():
            if self.is_valid_link(node):
                links.append(node)

        return list({str(link.title) for link in links})


def wander():
    current_page = settings.WIKI_STARTING_PAGE
    max_pages = settings.WIKI_MAX_PAGES

    bot = WikiWanderBot()

    while True:
        try:
            related_pages = bot.find_related_pages(current_page)
        except (
            pywikibot.exceptions.IsRedirectPageError,
            pywikibot.exceptions.NoPageError,
        ):
            # revisit a random page
            current_page = WikiPage.objects.order_by("?").first().title
        else:
            if len(related_pages) == 0:
                # revisit a random page
                current_page = WikiPage.objects.order_by("?").first().title
            else:
                WikiPage.objects.create(title=current_page)

                current_page = random.choice(related_pages)

        # prevent the database from growing too large
        if WikiPage.objects.count() >= max_pages:
            cutoff = WikiPage.objects.order_by("-created_at")[max_pages - 1].created_at
            WikiPage.objects.filter(created_at__lte=cutoff).delete()

        time.sleep(3)
