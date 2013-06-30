from bs4 import BeautifulSoup
import scraperwiki
import re
import dateutil.parser as parser

# Reformat markup to remove arbitrary linebreaks.
def oneline(html):
    return re.sub('\s+', ' ', html)

base = 'http://apod.nasa.gov/apod/'
archive = base + 'archivepix.html'
encoding = 'latin-1'

archive_soup = BeautifulSoup(scraperwiki.scrape(archive), from_encoding=encoding)
archive_links = archive_soup.find_all(href=re.compile('ap.*[0-9]+\.html'))
for archive_link in archive_links:
    apod_html = scraperwiki.scrape(base + archive_link['href'])
    apod_soup = BeautifulSoup(apod_html, from_encoding=encoding)

    # URL
    url = base + archive_link['href']

    # Date
    date_raw = archive_link.previous_sibling[:-3]
    date = parser.parse(date_raw).strftime('%Y-%m-%d')

    # Title
    title = archive_link.text

    # Explanation
    explanation_raw = re.search('<(b|(h3))>.*?Explanation.*?</(b|(h3))>\s*(.*?)\s*(</p>)?<p>', apod_html, re.DOTALL | re.IGNORECASE).group(5)
    explanation_utf = explanation_raw.decode(encoding) # Remember, we are working directly with apod_html, which was not passed through / decoded by BeautifulSoup.
    explanation = oneline(explanation_utf)

    # Picture URL. Check that there actually is a picture, as NASA sometimes
    # publishes videos instead.
    picture_link = apod_soup.find(href=re.compile('image/'))
    if picture_link:
        picture_url = base + picture_link['href']
        picture_found = True
    else:
        picture_found = False

    # Save!
    if picture_found:
        record = {'url': url, 'date': date, 'title': title, 'explanation': explanation, 'picture_url': picture_url}
        scraperwiki.sqlite.save(['url'], record)
