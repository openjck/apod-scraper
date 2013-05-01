import scraperwiki, re, dateutil.parser as parser
from bs4 import BeautifulSoup

# Reformat markup to get rid of arbitrary linebreaks.
def oneline(html):
    return re.sub('\s+', ' ', html)

base = 'http://apod.nasa.gov/apod/'

archive = base + 'archivepix.html'
archive_soup = BeautifulSoup(scraperwiki.scrape(archive))

apod_links = archive_soup.find_all(href=re.compile('ap.*[0-9]+\.html'))
for apod_link in apod_links:
    apod_html = scraperwiki.scrape(base + apod_link['href'])
    apod_soup = BeautifulSoup(apod_html)

    regex_flags = re.DOTALL | re.IGNORECASE

    # URL
    url = base + apod_link['href']

    # Date
    date_raw = apod_link.previous_sibling[:-3]
    date = parser.parse(date_raw).isoformat()

    # Title
    title_enc = apod_link.text
    title = title_enc.decode('latin-1')

    # Explanation
    explanation_enc = re.search('<(b|(h3))>.*?Explanation.*?</(b|(h3))>\s*(.*?)\s*(</p>)?<p>', apod_html, regex_flags).group(5)
    explanation_dec = explanation_enc.decode('latin-1')
    explanation = '<p>' + oneline(explanation_dec) + '</p>'

    # Picture. Note that this ignores videos (at least for now).
    picture_link = apod_soup.find(href=re.compile('image/'))
    if picture_link:
        picture_url = base + picture_link['href']

    # Save!
    if 'picture_url' in locals():
        record = {'url': url, 'date': date, 'title': title, 'explanation': explanation, 'picture_url': picture_url}
        scraperwiki.sqlite.save(['url'], record)
