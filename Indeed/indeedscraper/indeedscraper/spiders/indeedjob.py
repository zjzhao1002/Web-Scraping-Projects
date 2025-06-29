import scrapy
import re
import json
import pandas as pd


class IndeedjobSpider(scrapy.Spider):
    name = "indeedjob"

    def get_indeed_job_url(self, jobkey):
        return "https://de.indeed.com/viewjob?jk=" + jobkey

    def start_requests(self):
        df = pd.read_csv("<Path-to-search_result.csv>/search_result.csv")
        for i, row in df.iterrows():
            jobkey = row['jobkey']
            job_url = self.get_indeed_job_url(jobkey)
            print(job_url)
            yield scrapy.Request(
                url=job_url,
                callback=self.parse_job,
                meta={
                    'keyword': row['keyword'],
                    'location': row['location'],
                    'page': row['page'],
                    'position': row['position'],
                    'jobkey': row['jobkey']
                }
            )

    def parse_job(self, response):
        keyword = response.meta['keyword']
        location = response.meta['location']
        page = response.meta['page']
        position = response.meta['position']
        script_tag = re.findall(r"_initialData=(\{.+?\});", response.text)
        if script_tag is not None:
            json_blob = json.loads(script_tag[0])
            # with open(f'initialdata-{response.meta['jobkey']}.json', 'w', encoding='utf-8') as f:
            #     json.dump(json_blob, f, ensure_ascii=False, indent=4)

            job = json_blob['jobInfoWrapperModel']['jobInfoModel']
            yield {
                'keyword': keyword,
                'location': location,
                'page': page,
                'position': position,
                'jobkey': response.meta['jobkey'],
                'company': job['jobInfoHeaderModel'].get('companyName'), 
                'jobTitle': job['jobInfoHeaderModel'].get('jobTitle'),
                'jobDescription': job.get('sanitizedJobDescription') if job.get('sanitizedJobDescription') is not None else '',
            }
