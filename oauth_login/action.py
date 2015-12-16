from .page import *

@IN.hook
def actions():
	actns = {}
	
	actns['social/login/{provider}'] = {
		'handler' : action_handler_page_social_login,
	}
	
	actns['social/callback/{provider}'] = {
		'handler' : action_handler_page_social_callback,
	}
	
	return actns
	
