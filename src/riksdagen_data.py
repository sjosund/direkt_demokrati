from datetime import date, timedelta

import requests

from db_func import add_proposition
from utils import str_to_timestamp


def fetch_propositions(start, end):
    url = 'http://data.riksdagen.se/dokumentlista/?' \
          'doktyp=prop&from={start}&tom={end}&utformat=json'.format(start=start, end=end)
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception('Error while fetching')
    documents = response.json()['dokumentlista']['dokument']
    if isinstance(documents, dict):
        documents = [documents]

    return documents


def fetch_propositions_and_write_to_db(start, end):
    documents = fetch_propositions(start=start, end=end)
    for document in documents:
        add_proposition(
            {
                'title': document['titel'],
                'url': document['dokument_url_html'],
                'date': str_to_timestamp(document['datum'])
            }
        )


def main():
    fetch_propositions_and_write_to_db(
        start=date.today() - timedelta(days=30*6),
        end=date.today()
    )


if __name__ == '__main__':
    main()
