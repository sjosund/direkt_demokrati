from datetime import date, timedelta

import requests


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


def fetch_until_today(start):
    return fetch_propositions(
        start=start,
        end=date.today()
    )


def main():
    print(fetch_propositions(
        start=date.today() - timedelta(days=10),
        end=date.today()
    ))


if __name__ == '__main__':
    main()
