import scrapy


class PcsSpiderSpider(scrapy.Spider):
    name = "pcs_spider"
    allowed_domains = ["www.icd10data.com"]
    start_urls = ["https://www.icd10data.com/ICD10PCS/Codes"]

    all_codes = set()

    def start_requests(self):
        yield scrapy.Request(
            url = "https://www.icd10data.com/ICD10PCS/Codes",
            callback = self.parse
        )

    def parse(self, response):
        all_codes = response.css("a.identifier")
        for code in all_codes[:1]:
            relative_link = code.attrib['href']
            code_range = code.css("::text").get()
            url = "https://www.icd10data.com/" + relative_link
            yield scrapy.Request(
                url = url,
                meta = {"code range": code_range},
                callback = self.parse_catagory
            )

    def parse_catagory(self, response):
        catagory = response.css("h1.pageHeading::text").get()
        all_codes = response.css("a.identifier")
        for code in all_codes[:1]:
            relative_link = code.attrib['href']
            code_range = code.css("::text").get()
            url = "https://www.icd10data.com/" + relative_link
            yield scrapy.Request(
                url = url,
                callback = self.parse_subcatagory,
                meta = {"code range": code_range, "catagory": catagory}
            )
    
    def parse_subcatagory(self, response):
        subcatagory = response.css("h1.pageHeading ::text").get()
        all_codes = response.css("a.identifier")
        for code in all_codes:
            relative_link = code.attrib['href']
            code_range = code.css("::text").get()
            url = "https://www.icd10data.com/" + relative_link
            yield scrapy.Request(
                url = url,
                callback = self.parse_base_name,
                meta = {
                    "code range: ": code_range,
                    "catagory": response.meta['catagory'],
                    "subcatagory": subcatagory
                }
            )

    def parse_base_name(self, response):
        base_name = response.css("h1.pageHeading ::text").get()
        all_codes = response.css("a.identifier")
        for code in all_codes:
            relative_link = code.attrib['href']
            code_range = code.css("::text").get()
            url = "https://www.icd10data.com/" + relative_link
            yield scrapy.Request(
                url = url,
                callback = self.parse_name,
                meta = {
                    "code range": code_range,
                    "catagory": response.meta['catagory'],
                    "subcatagory": response.meta['subcatagory'],
                    "base name": base_name
                }
            )
    
    def parse_name(self, response):
        all_codes = response.css("a.identifierSpacing")
        for code in all_codes:
            relative_link = code.attrib['href']
            code_number = code.css("::text").get()
            url = "https://www.icd10data.com/" + relative_link
            yield scrapy.Request(
                url = url,
                callback = self.parse_final_code, 
                meta = {
                    "code": code_number,
                    "catagory": response.meta['catagory'],
                    "subcatagory": response.meta['subcatagory'],
                    "base name": response.meta['base name']
                }
            )

    def parse_final_code(self, response):
        code_description = response.css("h2.codeDescription::text").get()
        sel = response.css('div.body-content')
        description = "".join(str(sel.xpath('//ul/li//text()').extract()).strip())
        if response.meta['code'] not in self.all_codes:
            self.all_codes.add(response.meta['code'])
            yield {
                "url": response.url,
                "code": response.meta['code'],
                "catagory": response.meta['catagory'],
                "subcatagory": response.meta['subcatagory'],
                "base name": response.meta['base name'],
                "code description": code_description,
                "description": description
            }
