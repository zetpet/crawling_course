from typing import Iterator
import pandas as pd
import scrapy


class QuotesSpider(scrapy.Spider):
    name: str = "hw_1_rababkov"
    allowed_domains: list[str] = ["quotes.toscrape.com"]
    start_urls: list[str] = ["https://quotes.toscrape.com"]

    def __init__(self) -> None:
        """Initializes the spider with an empty list for storing quotes data."""
        self.quotes_data = []

    def parse(self, response) -> Iterator[dict[str, str]]:
        """Parse the response from the website and extract data.

        Args:
            response: The response object obtained from crawling the website.

        Returns:
            An iterator of dictionaries, where each dictionary contains the 'text', 'author', and 'tags' of a quote.
        """
        quotes = response.css("div.quote")

        for quote in quotes:
            text_quote = quote.css("span.text::text").get()
            author_quote = quote.css("span small::text").get()
            tags_quote = quote.css("div.tags a.tag::text").getall()
            self.quotes_data.append(
                {
                    "text": text_quote,
                    "author": author_quote,
                    "tags": ", ".join(tags_quote),
                }
            )
            yield {
                "text": text_quote,
                "author": author_quote,
                "tags": ", ".join(tags_quote),
            }

        next_page = response.css("li.next a::attr(href)").get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

    def closed(self, reason: str) -> None:
        """Called when the spider is closed."""
        self.save_quotes_to_excel()

    def save_quotes_to_excel(self) -> None:
        """Saves the collected quotes data to an Excel file."""
        df = pd.DataFrame(self.quotes_data)
        df.to_excel("quotes_rababkov.xlsx", index=False)
