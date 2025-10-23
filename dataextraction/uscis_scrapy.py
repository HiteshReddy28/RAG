import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from urllib.parse import urlparse
import os

class UscisBodySpider(CrawlSpider):
    name = "uscis_body"
    allowed_domains = ["uscis.gov"]
    start_urls = ["https://www.uscis.gov/"]

    custom_settings = {
        'USER_AGENT': 'Crawler/1.0 (contact@email.com)',
        'ROBOTSTXT_OBEY': True,
        'DOWNLOAD_DELAY': 10, 
        'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
        'AUTOTHROTTLE_ENABLED': True,
        'AUTOTHROTTLE_START_DELAY': 10,
        'AUTOTHROTTLE_MAX_DELAY': 30,
        'FEED_EXPORT_ENCODING': 'utf-8'
    }

    # Deny list (from robots.txt)
    deny_paths = [
        '/admin/', '/comment/reply/', '/filter/tips', '/node/add/', '/search/',
        '/user/', '/media/oembed', '/sites/default/files/archive/',
        '/tools/reports-and-studies/h-1b-employer-data-hub',
        '/tools/reports-and-studies/h-2b-employer-data-hub',
        '/save/save-agency-search-tool', '/tools/civil-surgeons-by-region',
        '/tools/find-a-doctor/list/export'
    ]

    rules = (
        Rule(
            LinkExtractor(
                allow_domains=["uscis.gov"],
                deny=deny_paths,
                tags=('a', 'area'),
                attrs=('href',)
            ),
            callback='parse_page',
            follow=True
        ),
    )

    def parse_page(self, response):
        # Extract just the <body> HTML content
        body_html = response.xpath('//body').get(default='')

        parsed = urlparse(response.url)
        path = parsed.path
        if path.endswith('/') or path == '':
            path += 'index.html'

        local_path = os.path.join("uscis_body_html", parsed.netloc, path.lstrip("/"))
        os.makedirs(os.path.dirname(local_path), exist_ok=True)

        # Save only body HTML
        with open(local_path, 'w', encoding='utf-8') as f:
            f.write(body_html)

        self.logger.info(f"Saved body of {response.url}")
