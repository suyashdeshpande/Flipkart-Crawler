import scrapy


class FlipkartSpider(scrapy.Spider):
    name = "flipkart_spider"

    def start_requests(self):
        url = "https://www.flipkart.com/search?q=laptop&sid=6bo%2Cb5g&as=on&as-show=on&otracker=AS_QueryStore_OrganicAutoSuggest_1_6&otracker1=AS_QueryStore_OrganicAutoSuggest_1_6&as-pos=1&as-type=RECENT&as-searchtext=laptop"
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        items = response.css("a._31qSD5")
        for item in items:
            itemName = item.css("div._3wU53n::text").get()
            rating = item.css("div.hGSR34::text").get()
            price = item.css("div._1vC4OE._2rQ-NK::text").get()

            yield {
                "name": itemName,
                "rating": rating,
                "price": price
            }

        nextPageId = response.css("a.fyt9Eu + a::attr(href)").get()
        i = 1
        while i < 6:
            nextPage = response.joinurl(nextPageId)
            yield scrapy.Request(nextPage, callable=self.parse)
            i += 1
