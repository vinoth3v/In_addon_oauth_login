
from requests_oauthlib import OAuth2Session

from .oauth_login import OAuthLogin

class Google(OAuthLogin):
	'''OAuthLogin Google.

	'''
	def __init__(self, config):
		self.config = config
	
	def authorization_url(self):
		
		try:
			
			redirect_uri = ''.join(('http://', IN.APP.config.app_domain, '/', 'social/callback/!', self.__type__))
			
			google = OAuth2Session(self.config['client_id'], scope = self.config['scope'], redirect_uri = redirect_uri)

			authorization_url, state = google.authorization_url(self.config['authorization_url'], access_type = "offline", approval_prompt = "force")

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
			
			self.session = OAuth2Session(client_id, state = key, redirect_uri=redirect_uri)
			
			token = self.session.fetch_token(token_url, client_secret = client_secret, authorization_response = authorization_response)
			
			return token
			
		except Exception as e:
			IN.logger.debug()
	
	def get_user_info(self):
		
		''' {\n "id": "107422018847720368553",\n 
				"email": "vinoth.3v@gmail.com",\n 
				"verified_email": true,\n 
				"name": "Vinoth Kanyakumari",\n 
				"given_name": "Vinoth",\n 
				"family_name": "Kanyakumari",\n 
				"link": "https://plus.google.com/+VinothKanyakumari",\n 
				"picture": "https://lh5.googleusercontent.com/-IlUWdWKhMZ8/AAAAAAAAAAI/AAAAAAAAE9E/oGncCYSq-MQ/photo.jpg",\n 
				"gender": "male",\n 
				"locale": "en"\n}
			'''
			
		response = self.session.get('https://www.googleapis.com/oauth2/v1/userinfo')
		
		info = json.loads(response.content.decode("utf-8"))
		
		if not info['verified_email']:
			return None
		
		return info
		