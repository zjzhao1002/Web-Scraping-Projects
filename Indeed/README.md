# Indeed
Indeed, Inc. is an American worldwide employment website for job listings launched in November 2004. 
It is an independent subsidiary of multinational company Recruit Holdings. 
Indeed is currently available in over 60 countries and 28 languages.

# Method
**Scrapy** is used in this case, since they have a [tutorial to scrape Indeed](https://thepythonscrapyplaybook.com/python-scrapy-indeed-scraper/).
However, this tutorial is written in 2023. Something has been changed. 

The scraping process has two steps: 
## Step 1: scrape the search page
The url of Indeed search page always includes the query and the location. 
For example, if we search for Data Scientist in Hamburg, we will go to the page with following url:
```
https://de.indeed.com/jobs?q=Data+Scientist&l=Hamburg
```
`q` stands for the search query and `l` is the location.

With Indeed the job data is available as hidden JSON data on the page. 
They are contained in the `<script id="mosaic-data" type="text/javascript">` tag, 
under `window.mosaic.providerData["mosaic-provider-jobcards"]`. 
We can use a regex command to find the json. 
```
script_tag = re.findall(r'window.mosaic.providerData\["mosaic-provider-jobcards"\]=(\{.+?\});', response.text)
```
Now we can extract data from this json. The most important one is the `jobkey`, which is actually a ID for each job.

## Step 2: scrape the job page
In 2025, the job url has this structure:
```
"https://de.indeed.com/viewjob?jk=" + jobkey
```
As Indeed returns the data inside a `window._initialData={}` inside a `<script>` tag in the HTML response,
it is pretty easy to extract the data. 
As we have done in the search page, we can use the following code:
```
script_tag = re.findall(r"_initialData=(\{.+?\});", response.text)
```
And then we can scrape data.

# Bypassing Indeed's Anti-Bot Protection
In this case, the **ScrapeOps Proxy Aggregator** has been used to bypass the anti-bot protection. 
We can integrate the proxy easily into our scrapy project by installing the ScrapeOps Scrapy proxy SDK a Downloader Middleware:
```
pip install scrapeops-scrapy-proxy-sdk
```
Finally, we need to edit the **setting.py**:
```
SCRAPEOPS_API_KEY = '<ScrapeOps-API-KEY>'
SCRAPEOPS_PROXY_ENABLED = True
SCRAPEOPS_PROXY_SETTINGS = {'mobile': True}

DOWNLOADER_MIDDLEWARES = {
    'scrapeops_scrapy_proxy_sdk.scrapeops_scrapy_proxy_sdk.ScrapeOpsScrapyProxySdk': 725,
}
```
