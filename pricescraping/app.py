import crochet
crochet.setup()  # initialize crochet before further imports

from flask import Flask, jsonify, render_template, request
from prices.prices.spiders import emag
from scrapy import signals
from scrapy.crawler import CrawlerRunner
from scrapy.signalmanager import dispatcher

app = Flask(__name__)
output_data = []
crawl_runner = CrawlerRunner()

ecommerce_shops = {'emag': emag.EmagSpider,
                   'cell': 'something'}


# @app.route('/')
# def hello_world():
#     return render_template("index.html")


# @app.route('/scrape/', methods=["POST"])
# def scrape():
#     # run crawler in twisted reactor synchronously
#     url = request.form.get('url')
#     scrape_with_crochet(url)
#     return jsonify(output_data)

@app.route('/price', methods=['POST'])
def scrape():
    if request.method == 'POST':
        s = request.form['url']
        # run crawler in twisted reactor synchronously
        scrape_with_crochet(s)
        return jsonify(output_data)


@crochet.wait_for(timeout=60.0)
def scrape_with_crochet(url):
    shop_spider = emag.EmagSpider
    for key in ecommerce_shops.keys():
        if key in url:
            shop_spider = ecommerce_shops.get(key)
            break
    # signal fires when single item is processed
    # and calls _crawler_result to append that item
    dispatcher.connect(_crawler_result, signal=signals.item_scraped)
    eventual = crawl_runner.crawl(shop_spider, url)
    return eventual  # returns a twisted.internet.defer.Deferred


def _crawler_result(item, response, spider):
    """
    We're using dict() to decode the items.
    Ideally this should be done using a proper export pipeline.
    """
    output_data.clear()
    output_data.append(dict(item))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
