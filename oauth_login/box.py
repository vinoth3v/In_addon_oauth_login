class SocialLoginBoxLoginLinks(In.boxer.Box):
	'''SocialLoginBoxLoginLinks'''
	
	def __init__(self, data = None, items = None, **args):
		super().__init__(data, items, **args)
		
		self.add('Link', {
			'href' : '/social/login/!Facebook',
			'value' : '<i class="i-icon-facebook-square"></i> ' + s('Login with Facebook'),
			'weight' :  0,
			'css' : ['i-button i-button-primary']
		})
		
		self.add('Link', {
			'href' : '/social/login/!Google',
			'value' : '<i class="i-icon-google-plus-square"></i> ' + s('Login with Google'),
			'weight' :  1,
			'css' : ['i-button i-button-success']
		})
	
@IN.register('SocialLoginBoxLoginLinks', type = 'Themer')
class SocialLoginBoxLoginLinksThemer(In.boxer.BoxThemer):
	'''SocialLoginBoxLoginLinks'''
	
	