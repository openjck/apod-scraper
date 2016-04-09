# Installation

Follow these steps to install the scraper on ScraperWiki.

1. Create a ScraperWiki account
2. Create a new scraper (sometimes called a dataset) for this project
3. SSH into the account of the new scraper
4. `cd code`
5. Clone the repository into a directory called *repo*
6. `rm scraper`
7. `ln -s repo/scraper.py scraper`
8. `cd repo`
9. `pip install --user -r requirements-scraperwiki.txt`

**NB:** If the scraper is edited using the web-based *Code in your browser*
tool, the symlink will be overwritten with the scraper file contents.
