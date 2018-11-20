from lxml import html 
import requests
import pathlib

xrb_url = 'https://www.xrb.govt.nz'

# to decide which standard to download
print("""
        1) For profit standards
        2) Non-for-profit standards
        3) Public sector standards
        """)

result = input('Please choose: ')

if eval(result) == 1:
    suffix_url = '/accounting-standards/for-profit-entities/'
elif eval(result) ==2:
    suffix_url = ''
elif eval(result) ==3:
    suffix_url = ''
else:
    exit()

html_response = requests.get(xrb_url + suffix_url)

tree = html.fromstring(html_response.content) 

# get all the titles for the accounting standards
titles = tree.xpath('//li/div/a[@class="title"]/text()')

# build a dict to include all the links for corresponding accounting standard
standards = dict()
for title in titles:
    expr = '//a[text()="' + title + '"]/@href'
    link = xrb_url + tree.xpath(expr)[0]
    standards[title] = link
    
# create directories for each standard
xrb_path = pathlib.Path('./xrb/')
for title in titles:
    sub_path = xrb_path / title.replace(" ", "_")
#    sub_path.mkdir(parents=True, exist_ok=True)
    print(sub_path)

# download standard and save into the relevant directory
