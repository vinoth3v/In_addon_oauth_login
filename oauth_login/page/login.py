
def action_handler_page_social_login(context, action, provider, **args):
	''''''
	
	cls = IN.register.get_class(provider, 'OAuthLogin')
	if not cls:
		context.not_found()
	
	try:
		o = cls(IN.APP.config.oauth_login[provider])
		
		authorization_url = o.authorization_url()
		
		# TODO: STATE
		
		context.redirect(authorization_url)
		
	except Exception as e:
		IN.logger.debug()
	