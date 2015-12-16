from requests_oauthlib import OAuth2Session


def action_handler_page_social_callback(context, action, provider, **args):
	''''''
	
	# http://in.linux.local.in/social/callback/!Google?state=3J5aX4AM5wE8QEVayLWGUuQ2As3iMF&code=4/N61y8AnJXzBHHpKHf6CkQre6EHQdiro9XVtrtmcDkrY
	
	authorization_response = context.request.path_with_query
	
	key = context.request.args['query'].get('state', '')
	
	cls = IN.register.get_class(provider, 'OAuthLogin')
	if not cls:
		context.not_found()
	
	
	nabar_id = context.nabar.id
	
	try:
		
		
		#db = IN.db
		
		#cursor = db.select({
			#'table' : 'log.oauth_login_state',
			#'columns' : ['key'],
			#'where' : [
				#['id', id]
			#]
		#}).execute()

		
		#if cursor.rowcount == 0:
			#context.not_found()

		#key = cursor.fetchone()[0]
		
		o = cls(IN.APP.config.oauth_login[provider])
		
		token = o.fetch_token(key, authorization_response)
		
		if not token:
			
			if nabar_id:
				context.redirect('nabar/home')
			else:
				context.redirect('nabar/login')
			
			return
		
		if token:
			
			info = o.get_user_info()
			
			if not info:
				
				if nabar_id:
					context.redirect(''.join(('/nabar/', str(nabar_id), '/edit/login')))
				else:
					context.redirect('/nabar/login')
				
				return
			
			email = info['email']
			oauth_nabar_id = info['id']
			
			just_logged_in = False
			
			if not nabar_id:
				
				# no register if email is already active
				
				nabar_id = IN.nabar.get_active_nabar_id_by_email(email)

				if nabar_id:
					
					# login
					IN.nabar.login(nabar_id, True)
					
					IN.oauth_login.add_connection_if_not_exists(nabar_id, oauth_nabar_id, provider)
					
					context.redirect('/nabar/home')
					
					
			if not nabar_id:
				
				# register
				
				nabar_id = IN.oauth_login.register_nabar(info['name'], email)

				if not nabar_id:
					context.not_found()
				
				# login
				IN.nabar.login(nabar_id, True)
				just_logged_in = True
				
			
			IN.oauth_login.add_email_if_not_exists(nabar_id, email)
			
			IN.oauth_login.add_connection_if_not_exists(nabar_id, oauth_nabar_id, provider)
			
			if just_logged_in:
				context.redirect('/nabar/home')
			else:
				context.redirect(''.join(('/nabar/', str(nabar_id), '/edit/login')))
			
	except Exception as e:
		IN.logger.debug()
		