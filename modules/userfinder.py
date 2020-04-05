
import requests, re, urllib3

# Disabling insecure request warnings for HTTPS sites
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def check_username(mssg, telegramClient, chat_id, bot):
	"""
	Module forked from https://github.com/tr4cefl0w/userfinder

	This function finds the user name from the mssg argument and loops through each site in the 'sites'
	variable to verify is the user account is valid. This is done by first checking for a 200 status
	code. Then, because some sites can't fucking respect RFC standards by returning 200s on invalid
	requests, we have to exclude some responses by checking if a string from the not_found_msg list
	is present in the response. This removes the possibility of false-positives for the sites
	present in the default list.
	"""

	user = re.search(r'([\"])(?:(?=(\\?))\2.)*?\1', mssg.text)

	not_found_msg = [
		"doesn&#8217;t&nbsp;exist",
		"doesn't exist",
		"no such user",
		"page not found",
		"could not be found",
		"https://pastebin.com/index",
		"user not found",
		"usererror-404",
		"he user id you entered was not found"
	]

	headers = {
		'User-Agent':
		'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0'
	}

	sites = [
		'https://www.instagram.com/{}',
		'https://www.facebook.com/{}',
		'https://www.twitter.com/{}',
		'https://www.youtube.com/{}',
		'https://{}.blogspot.com',
		'https://www.reddit.com/user/{}',
		'https://{}.wordpress.com',
		'https://www.pinterest.com/{}',
		'https://www.github.com/{}',
		'https://{}.tumblr.com',
		'https://www.flickr.com/people/{}',
		'https://steamcommunity.com/id/{}',
		'https://vimeo.com/{}',
		'https://soundcloud.com/{}',
		'https://disqus.com/{}',
		'https://medium.com/@{}',
		'https://{}.deviantart.com',
		'https://vk.com/{}',
		'https://about.me/{}',
		'https://imgur.com/user/{}',
		'https://flipboard.com/@{}',
		'https://slideshare.net/{}',
		'https://open.spotify.com/user/{}',
		'https://www.mixcloud.com/{}',
		'https://www.scribd.com/{}',
		'https://www.badoo.com/en/{}',
		'https://www.patreon.com/{}',
		'https://bitbucket.org/{}',
		'https://www.dailymotion.com/{}',
		'https://www.etsy.com/shop/{}',
		'https://cash.me/{}',
		'https://www.behance.net/{}',
		'https://www.goodreads.com/{}',
		'https://www.instructables.com/member/{}',
		'https://keybase.io/{}',
		'https://kongregate.com/accounts/{}',
		'https://{}.livejournal.com',
		'https://angel.co/{}',
		'https://last.fm/user/{}',
		'https://dribbble.com/{}',
		'https://www.codecademy.com/{}',
		'https://en.gravatar.com/{}',
		'https://pastebin.com/u/{}',
		'https://foursquare.com/{}',
		'https://www.roblox.com/user.aspx?username={}',
		'https://www.gumroad.com/{}',
		'https://{}.newgrounds.com',
		'https://www.wattpad.com/user/{}',
		'https://www.canva.com/{}',
		'https://creativemarket.com/{}',
		'https://www.trakt.tv/users/{}',
		'https://500px.com/{}',
		'https://buzzfeed.com/{}',
		'https://tripadvisor.com/members/{}',
		'https://{}.hubpages.com',
		'https://{}.contently.com',
		'https://houzz.com/user/{}',
		'https://blip.fm/{}',
		'https://www.wikipedia.org/wiki/User:{}',
		'https://news.ycombinator.com/user?id={}',
		'https://www.codementor.io/{}',
		'https://www.reverbnation.com/{}',
		'https://www.designspiration.net/{}',
		'https://www.bandcamp.com/{}',
		'https://www.colourlovers.com/love/{}',
		'https://www.ifttt.com/p/{}',
		'https://www.ebay.com/usr/{}',
		'https://{}.slack.com',
		'https://www.okcupid.com/profile/{}',
		'https://www.trip.skyscanner.com/user/{}',
		'https://ello.co/{}',
		'https://{}.basecamphq.com/login'
	]

	for site in sites:
		if (user):
			try:
				r = requests.get(site.format(
					user.group().replace('"',"")).rstrip(), headers=headers, timeout=10)
				if r.status_code == 200:
					found = [p in r.text.lower() for p in not_found_msg]
					if True not in found:
						telegramClient.send_message(chat_id, r.url, disable_web_page_preview=True)
			except requests.exceptions.RequestException as e:
				print(e)
				continue
