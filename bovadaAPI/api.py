from auth import login_to_bovada
from selenium.webdriver import Firefox
from .error import BovadaException
from .decorators import authentication_required, authentication_recommended




class BovadaApi(object):

	def __init__(self, authentication=None,driver=None, *args, **kwargs):
		self.authentication = authentication
		self.driver = Firefox()
		self.current_url = "https://bovada.lv"
		self.driver.get(self.current_url)
		return super(BovadaApi, self).__init__(*args, **kwargs)


	def authenticate(self, username=None, password=None):
		try:
			logged_in = login_to_bovada(self)
		except Exception, e:
			print e

		


	
	@authentication_required
	@property
	def balance(self):
		return bind_api(action="balance")


	@authentication_required
	@property
	def bet_history(self):
		self.current_url = "http://bovada.lv/https://www.bovada.lv/?pushdown=bet-history"
		return bind_api(action="bet_history")

	@authentication_required
	@property
	def open_bets(self):
		self.current_url = "http://bovada.lv/https://www.bovada.lv/?pushdown=bet-history"
		return bind_api(action="open_bets")

	@authentication_recommended
	@property
	def soccer_matches(self):
		self.current_url = "http://sports.bovada.lv/soccer"
		return bind_api(action="soccer_matches")

	@property
	def basketball_matches(self):
		return bind_api(action="basketball_matches")

	@property
	def tennis_matches(self):
		return bind_api(action="tennis_matches")

	@property
	def rugby_matches(self):
		return bind_api(action="rugby_matches")




