from search_dictionary_for_certain_keys import search_dictionary_for_certain_keys
import json
from error import BovadaException


class BovadaMatch(object):
	def __init__(self, *args, **kwargs):
		self.sport = kwargs.pop("sport")
		self.description = kwargs.pop("description")
		self.startTime = kwargs.pop("startTime")
		self.home_team_short_name = kwargs.pop("home_team_short_name")
		self.home_team_full_name = kwargs.pop("home_team_full_name")
		self.home_team_abbreviation = kwargs.pop("home_team_abbreviation")
		self.away_team_short_name = kwargs.pop("away_team_shortname")
		self.away_team_full_name = kwargs.pop("away_team_full_name")
		self.away_team_abbreviation= kwargs.pop("away_team_abbreviation")
		self.game_link = kwargs.pop("game_link")
		self.type = kwargs.pop("type")
		self.game_id = kwargs.pop("game_id")
		self.outcomes = kwargs.pop("outcomes")
		return super(BovadaMatch, self).__init__()

	@property
	def match_details(self):
		return "%s, %s, %s, %s, %s, %s, %s, %s" %(self.sport, self.game_link, 
			self.description, self.startTime, self.home_team_full_name,
			self.game_link, self.type, self.game_id)

	@classmethod
	def create_from_center_content(cls, content_center):
		match = search_dictionary_for_certain_keys("items", content_center)[0]
		outcome_objects_for_match = []
		game_sport = match['sport']
		game_id = int(match['id'])
		description = match['description']
		startTime = match['startTime']
		competitors = match['competitors']
		home_team_abbreviation = search_dictionary_for_certain_keys("abbreviation", competitors[0])
		home_team_short_name = search_dictionary_for_certain_keys("shortName", competitors[0])
		home_team_full_name = search_dictionary_for_certain_keys("description", competitors[0])
		away_team_short_name = search_dictionary_for_certain_keys("shortName", competitors[1])
		away_team_abbreviation=  search_dictionary_for_certain_keys("abbreviation", competitors[1])
		away_team_full_name = search_dictionary_for_certain_keys("description", competitors[1])
		game_link = "https://sports.bovada.lv{}".format(match['link'])
		type_ = match['type']
		displayGroups= match['displayGroups']
		for group in displayGroups:
			#if the group is not a gameline we'll skip over it.
			if group['description'] != "Game Lines":
				pass
			else:
				betting_lines = [x for x in group["itemList"]]
				for line in betting_lines:
					outcomes = OutCome.create_from_betting_line(line)
					for outcome in outcomes:
						outcome_objects_for_match.append(outcome)


					

		bmatch = BovadaMatch(
				sport=game_sport,
				description=description,
				startTime=startTime,
				home_team_short_name=home_team_short_name,
				home_team_full_name = home_team_full_name,
				home_team_abbreviation = home_team_abbreviation,
				away_team_shortname = away_team_short_name,
				away_team_abbreviation = away_team_abbreviation,
				away_team_full_name = away_team_full_name,
				game_link=game_link,
				type=type_,
				game_id=game_id, 
				outcomes=outcome_objects_for_match)
		return bmatch
	@classmethod
	def bulk_create_from_center_content(cls, center_content):
		bmatches = []
		try:
			gamelines = search_dictionary_for_certain_keys("items", center_content)[0] #index 0 is gamelines index 1 is futures
		except (IndexError, TypeError):
			return []

		try:
			matches = gamelines["itemList"]['items']
		except (KeyError):
			return []
		else:
			for match in matches:
				game_sport = ""
				game_id = None
				description = ""
				startTime = None
				competitors = []
				home_team_abbreviation = ""
				home_team_short_name = ""
				home_team_full_name = ""
				away_team_full_name = ""
				away_team_short_name = ""
				away_team_abbreviation = ""
				game_link = ""
				outcome_objects_for_match = []
				try:
					game_sport = match['sport']
				except KeyError, e:
					pass
				try:
					game_id = int(match['id'])
				except KeyError, e:
					pass
				try:
					description = match['description']
				except KeyError, e:
					pass
				try:
					startTime = match['startTime']
				except KeyError, e:
					pass
				try:
					competitors = match['competitors']
				except KeyError, e:
					pass
				try:
					home_team_abbreviation = search_dictionary_for_certain_keys("abbreviation", competitors[0])
				except (KeyError, IndexError):
					pass
				try:
					home_team_short_name = search_dictionary_for_certain_keys("shortName", competitors[0])
				except (KeyError, IndexError):
					pass
				try:
					home_team_full_name = search_dictionary_for_certain_keys("description", competitors[0])
				except (KeyError, IndexError):
					pass
				try:
					away_team_short_name = search_dictionary_for_certain_keys("shortName", competitors[1])
				except (KeyError, IndexError):
					pass
				try:
					away_team_abbreviation=  search_dictionary_for_certain_keys("abbreviation", competitors[1])
				except (KeyError, IndexError):
					pass
				try:
					away_team_full_name = search_dictionary_for_certain_keys("description", competitors[1])
				except (KeyError, IndexError):
					pass
				try:
					game_link = "https://sports.bovada.lv{}".format(match['link'])
				except (KeyError, TypeError):
					pass
				try:
					type_ = match['type']
				except (KeyError):
					pass
				try:
					displayGroups= match['displayGroups']
				except (KeyError):
					return []
				else:
					for group in displayGroups:
						group_description = None
						try:
							group_description = group["description"]
						except KeyError:
							pass
						if (group_description is None or
							group_description != "Game Lines"
							):
							break

						else:
							try:
								bet_lines = group["itemList"]
							except KeyError, e:
								break
							else:
								betting_lines = [x for x in bet_lines]
							for line in betting_lines:
								outcomes = OutCome.create_from_betting_line(line)
								for outcome in outcomes:
									outcome_objects_for_match.append(outcome)


							

				bmatch = BovadaMatch(
						sport=game_sport,
						description=description,
						startTime=startTime,
						home_team_short_name=home_team_short_name,
						home_team_full_name = home_team_full_name,
						home_team_abbreviation = home_team_abbreviation,
						away_team_shortname = away_team_short_name,
						away_team_abbreviation = away_team_abbreviation,
						away_team_full_name = away_team_full_name,
						game_link=game_link,
						type=type_,
						game_id=game_id, 
						outcomes=outcome_objects_for_match)
				
				bmatches.append(bmatch)
			
			return bmatches


class OutCome(object):
	def __init__(self, *args, **kwargs):
		#3-Way MoneyLine
		self.odds_type = kwargs.pop("odds_type")
		#H = Home, A = Away, O = Over, U = Under
		self.outcome_type = kwargs.pop("outcome_type")
		try:
			self.name = kwargs.pop("name")
		except KeyError:
			pass
		try:
			self.odds = kwargs.pop("odds")
		except KeyError:
			pass
		try:
			self.handicap = kwargs.pop("handicap")
		except KeyError:
			pass
		try:
			self.price_id = kwargs.pop("price_id")
		except KeyError, e:
			pass
		try:
			self.outcome_id = kwargs.pop("outcome_id")
		except KeyError, e:
			pass
		return super(OutCome, self).__init__()


	@classmethod
	def create_from_betting_line(cls, betting_line, *args, **kwargs):
		outcome_objs = []
		odds_type = betting_line["description"]
		outcomes = betting_line["outcomes"]
		for outcome in outcomes:
			outcome_type = None
			
			try:
				handicap = float(outcome["price"]["handicap"])
			except Exception, e:
				handicap = None

			try:
				outcome_type = outcome["type"]
			except KeyError, e:
				pass

			try:
				name = outcome["description"]
			except KeyError, e:
				name = None

			try:
				outcome_type = outcome["type"]
			except KeyError, e:
				outcome_type = None
			try:
				odds = float(outcome["price"]['decimal'])
			except KeyError, e:
				odds = None

			try:
				status = outcome['status']
			except KeyError, e:
				status = None
			try:
				price_id = int(outcome['price']['id'])
			except KeyError, e:
				price_id = None
			try:
				outcome_id = int(outcome['price']['outcomeId'])
			except KeyError, e:
				outcome_id = None

			if status == "OPEN":
				outcome_objs.append(
					cls(
						odds_type=odds_type,
						name=name,
						outcome_type=outcome_type,
						odds=odds,
						handicap = handicap,
						price_id=price_id,
						outcome_id=outcome_id
					)
				)
		
		return outcome_objs




def parse_special_response(response, action):
	if action == "balance":
		return int(search_dictionary_for_certain_keys("availableBalance", response.json())["amount"])
	elif action == "summary":
		return response.json()

	elif action == "wallets":
		return response.json()



	elif action == "open_bets":
		outstanding_bet_amount = 0
		total_odds = 0
		try:
			items = response.json()["items"]
		except KeyError, e:
			items = None

		if items:
			for item in items:
				print item
				try:
					riskAmount = item["riskAmount"]
				except KeyError, e:
					riskAmount = None
				try:
					toWinAmount = item["toWinAmount"]
				except KeyError, e:
					toWinAmount = 0
				
				if riskAmount:
					try:
						riskAmount = float(riskAmount)
					except Exception, e:
						print e
						riskAmount = riskAmount

					outstanding_bet_amount += riskAmount
				
				if riskAmount and toWinAmount:
					odds = (toWinAmount/riskAmount) + 1
					total_odds += odds

		return (
			"number of outstanding bets: {}".format(len(items)), 
			"outstanding_bet_amount: {}".format(outstanding_bet_amount),
			"avg_odds: {}".format(total_odds/len(items)),
		)

	elif action == "open_bet_outcome_ids":
		outcome_ids = []
		try:
			items = response.json()["items"]
		except KeyError, e:
			items = None

		for item in items:
			try:
				outcome_ids.append(item["reference"])
			except KeyError, e:
				print e

	elif action == "bet_history" or action=="bet_history_24_hours" or action=="bet_history_3_days":
		total_profit = 0
		number_of_bets_won = 0
		number_of_bets_lost = 0
		try:
			items = response.json()["items"]
		except KeyError, e:
			items = None

		if items:
			for item in items:
				try:
					outcomeCode = item["outcomeCode"]
				except KeyError, e:
					outcomeCode = None

				if (outcomeCode and 
					outcomeCode == "W"
					):
					number_of_bets_won += 1
					total_profit += float(item["toWinAmount"]) + float(item["riskAmount"]) - float(item["riskAmount"])


				elif (outcomeCode and 
					outcomeCode == "L"
					):
					number_of_bets_lost +=1
					total_profit -= float(item["riskAmount"])
			return "total_profit: ${}, num_bets_won: {}:), number_of_bets_lost: {}:(".format(total_profit, number_of_bets_won, number_of_bets_lost)




	return response

def parse_response(response):
	center_content = response['data']['regions']['content_center'] #useful
	bmatches = BovadaMatch.bulk_create_from_center_content(center_content)
	return bmatches

	
			
