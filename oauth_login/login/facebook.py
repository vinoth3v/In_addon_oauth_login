
from requests_oauthlib import OAuth2Session
from requests_oauthlib.compliance_fixes import facebook_compliance_fix

from .oauth_login import OAuthLogin

class Facebook(OAuthLogin):
	'''OAuthLogin Facebook.

	'''
	def __init__(self, config):
		self.config = config

		#super().__init__()

	def authorization_url(self):

		try:

			redirect_uri = ''.join(('http://', IN.APP.config.app_domain, '/', 'social/callback/!', self.__type__))

			fb = OAuth2Session(self.config['client_id'], scope = self.config['scope'], redirect_uri = redirect_uri)
			fb = facebook_compliance_fix(fb)

			authorization_url, state = fb.authorization_url(self.config['authorization_url'])

			return authorization_url

		except Exception as e:
			IN.logger.debug()
			#db.connection.rollback()

	def fetch_token(self, key, authorization_response):

		try:

			client_id = self.config['client_id']
			token_url = self.config['token_url']
			client_secret = self.config['client_secret']

			redirect_uri = ''.join(('http://', IN.APP.config.app_domain, '/', 'social/callback/!', self.__type__))

			self.session = OAuth2Session(client_id, state = key, redirect_uri = redirect_uri)
			self.session = facebook_compliance_fix(self.session)

			token = self.session.fetch_token(token_url, client_secret = client_secret, authorization_response = authorization_response)

			return token

		except Exception as e:
			IN.logger.debug()

	def get_user_info(self):

		'''
		{'first_name': 'Siva',
		 'gender': 'male',
		 'id': '966397646735187',
		 'last_name': 'Jk',
		 'link': 'https://www.facebook.com/app_scoped_user_id/966397646735187/',
		 'locale': 'en_US',
		 'name': 'Siva Jk',
		 'timezone': 5.5,
		 'updated_time': '2013-06-17T17:02:00+0000',
		 'verified': True}
		'''

		response = self.session.get('https://graph.facebook.com/me')

		info = json.loads(response.content.decode("utf-8"))

		if not info['verified']:
			return None

		return info


