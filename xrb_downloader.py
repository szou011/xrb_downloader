from lxml import html
import requests
import pathlib
import logging
import pprint

logging.basicConfig(level=logging.DEBUG)

xrb_url = 'https://www.xrb.govt.nz'

standards_list = {
        1:"for-profit-entities",
        2:"not-for-profit",
        3:"public-sector"
        }

# to decide which standard to download
print("Please select the accounting standards to be downloaded:")
pprint.pprint(standards_list)

try:
    selected_standards = standards_list[eval(input('Please input (1, 2 or 3): '))]
except:
    exit()

html_response = requests.get(xrb_url + "/" + selected_standards)

tree = html.fromstring(html_response.content)

# get all the titles for the accounting standards
titles = tree.xpath('//li/div/a[@class="title"]/text()')

# build a dict to include all the links for corresponding accounting standard
standards = dict()
for title in titles:
    expr = '//a[text()="' + title + '"]/@href'
    link = xrb_url + tree.xpath(expr)[0]
    standards[title] = link

logging.debug(pprint.pformat(standards))

# create directories for each standard
dl_path = pathlib.Path('./xrb/')
for title in titles:
    sub_path = dl_path / selected_standards / title.replace(" ", "_")
#    sub_path.mkdir(parents=True, exist_ok=True)
    print(sub_path)

# download standard and save into the relevant directory
