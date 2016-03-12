import scrapy
import urlparse
import os
import errno
import shutil
import re

website = 'summit2014.reversim.com'


class MySpider(scrapy.Spider):
    name = 'rs'
    start_urls = ['http://summit2014.reversim.com/?_escaped_fragment_=']
    allowed_domains = [website]

    def parse(self, response):
        self.save(response)
        for url in response.css('a::attr("href")').re('.*'):
            url = response.urljoin(url)
            url = urlparse.urlparse(url)
            url = url._replace(query='_escaped_fragment_=')
            url = url.geturl()
            yield scrapy.Request(url)

    def save(self, response):
        url = urlparse.urlparse(response.url)
        path = url.path
        if path == '/':
            path = '/index'
        filename = '{0}{1}.html'.format(website, path)
        mkdir(filename)
        print '>>>>>>>>>>>> ' + filename
        body = response.body
        body = re.sub(r'href="/(.*)"', r'href="/\1.html"', body)
        with open(filename, 'wb') as f:
            f.write(body)


def mkdir(filename):
    '''
    Makes the dir for the file, recursively if you have to
    '''
    path = os.path.dirname(filename)
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def rm(path):
    shutil.rmtree(path, ignore_errors=True)


rm(website)
