# encoding: utf-8

import json
import requests

from .resource import AbstractResource
from .settings import BASE_URL


class Card(AbstractResource):
    BASE_URL = BASE_URL + 'cards'

    def __init__(
            self,
            api_key=None,
            _id=None,
            card_number=None,
            expiration_date=None,
            card_expiration_date=None,
            holder_name=None,
            card_hash=None):

        if card_hash is None:
            self.data = {
                'card_number': card_number,
                'expiration_date': expiration_date,
                'card_expiration_date': card_expiration_date,
                'holder_name': holder_name,
            }
        else:
            self.data = {'card_hash': card_hash}

        if id is not None:
            self.data['id'] = _id
        self.data['api_key'] = api_key

    def get_data(self):
        return self.data

    @property
    def id(self):
        return self.data.get('id', '')

    def find_by_id(self, _id=None):
        if _id is None and not self.data.get('id', False):
            raise ValueError('Cant find card id')
        card_id = _id if _id else self.data['id']
        url = self.BASE_URL + '/' + str(card_id)
        pagarme_response = requests.get(url, params={'api_key': self.data['api_key']})
        if pagarme_response.status_code == 200:
            try:
                self.handle_response(json.loads(pagarme_response.content))
            except:
                self.handle_response(json.loads(pagarme_response.content.decode(encoding='UTF-8')))
        else:
            try:
                self.error(pagarme_response.content)
            except:
                self.error(json.loads(pagarme_response.content.decode(encoding='UTF-8')))
