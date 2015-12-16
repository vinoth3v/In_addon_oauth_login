
import datetime
from In.core.object_meta import ObjectMeta


class OAuthLoginMeta(ObjectMeta):

	__class_type_base_name__ = 'OAuthLoginBase'
	__class_type_name__ = 'OAuthLogin'


class OAuthLoginBase(Object, metaclass = OAuthLoginMeta):
	'''Base class of all IN OAuthLoginBase.

	'''
	__allowed_children__ = None
	__default_child__ = None


@IN.register('OAuthLogin', type = 'OAuthLogin')
class OAuthLogin(OAuthLoginBase):
	'''Base class of all IN OAuthLoginBase.

	'''
	
class OAuthLoginManager:
	''''''
	
	
	def add_connection_if_not_exists(self, nabar_id, oauth_nabar_id, provider):
		
		# add new oauth connection if not exists
		
		try:
			
			db = IN.db
			cursor = db.execute('''select o.id 
				FROM account.oauth_connection o
				where 
				o.nabar_id = %(nabar_id)s AND
				o.oauth_nabar_id = %(oauth_nabar_id)s AND
				o.provider = %(provider)s
				''', {
				'nabar_id' : nabar_id,
				'oauth_nabar_id' : oauth_nabar_id,
				'provider' : provider,				
			})

			if cursor.rowcount == 0:
				db.insert({
					'table' : 'account.oauth_connection',
					'columns' : ['nabar_id', 'oauth_nabar_id', 'provider'],
					'values' : [
						[nabar_id, oauth_nabar_id, provider]
					]
				}).execute()
				
				db.connection.commit()
				
		except Exception as e:
			IN.logger.debug()
			db.connection.rollback()
		
	
	def add_email_if_not_exists(self, nabar_id, email):
		
		try:
			
			db = IN.db
			
			# add new email if not exists
			
			cursor = db.execute('''select l.nabar_id
				FROM account.login l
				JOIN account.nabar a ON l.nabar_id = a.id
				where a.status = 1  AND
				l.type = %(type)s and l.status = 1 AND
				l.value = %(email)s
				LIMIT 1''', {
				'type' : 'email',
				'email' : email,
			})

			if cursor.rowcount == 0:
			
				login_id = In.nabar.NabarLogin({
					'id' : None,				# new login
					'nabar_id' : nabar_id,
					'value' : email,
					'type' : 'email',
					'created' : datetime.datetime.now(),
					'status' : IN.nabar.NABAR_STATUS_ACTIVE, # active
				}).insert()
			
				db.connection.commit()
			
		except Exception as e:
			IN.logger.debug()
			db.connection.rollback()
		
	def register_nabar(self, name, email, gender = 1):
		
		if type(gender) is str:
			gender = gender.lower()
			try:
				gender = {'female' : 0,  'male' : 1, 'shemale' : 2}[gender] # throw error
			except Exception as e1:
				gender = 1 # default
			
		nabar_id = In.nabar.Nabar({
			'id' : None,		# new nabar
			'name' : name,		# display name
			'gender' : gender,
			'created' : datetime.datetime.now(),
			'status' : IN.nabar.NABAR_STATUS_ACTIVE, 		# disabled by default
			'roles' : [IN.nabar.confirmed_role_id],
			'data' : {
				'primary_email' : email
			},
		}).insert(False)


		if not nabar_id:
			return
		
		nabar = IN.entitier.load_single('Nabar', nabar_id)
		
		# update the nabar_id and nabar cache
		nabar.nabar_id = nabar_id
		nabar.save()
		
		return nabar_id
		
	
@IN.hook
def In_app_init(app):
	# set the messenger

	IN.oauth_login = OAuthLoginManager()

