# -*- coding: utf-8 -*-
import os
import abc
import time
import pdfkit
import random
import pickle
import logging
import requests
import pandas as pd
import multiprocessing as mp
import snscrape.modules.vkontakte as sns_vk
import snscrape.modules.telegram as sns_tg
import snscrape.modules.twitter as sns_tw
from math import ceil
from xh1scr import TikTok as tik_tok
from tumblpy import Tumblpy
from itertools import islice
from bs4 import BeautifulSoup
from urllib.parse import quote
from prettytable import PrettyTable
from facebook_scraper import get_posts
from instaloader import Instaloader, Profile
from concurrent.futures import ThreadPoolExecutor, TimeoutError
from concurrent.futures import thread as cf_thread


logger = logging.getLogger("SEARCH ME")
stream = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s ### %(name)s ### %(message)s')
stream.setFormatter(formatter)
logger.addHandler(stream)
logger.addHandler(logging.NullHandler())
__base__ = os.getcwd()
# config = pdfkit.configuration(wkhtmltopdf='wkhtmltopdf.exe')
S_VK, S_IG, S_TG, S_TW, S_YT, S_FB, S_TB, S_SC, S_TK = "vk", "instagram", "telegram", "twitter", "youtube", "facebook", "tumblr", "snapchat", "tiktok"


class Search(metaclass=abc.ABCMeta):
	def __init__(self, results=10, retry=10, pdf_report=False, pdf_timeout=30, cache=True, sleep_min=0.0, sleep_max=1.5, socials=(S_VK, S_IG, S_TG, S_TW, S_YT, S_FB, S_TB, S_SC, S_TK), languages=['af', 'ach', 'ak', 'am', 'ar', 'az', 'be', 'bem', 'bg', 'bh', 'bn', 'br', 'bs', 'ca', 'chr', 'ckb', 'co', 'crs', 'cs', 'cy', 'da', 'de', 'ee', 'el', 'en', 'eo', 'es', 'es-419', 'et', 'eu', 'fa', 'fi', 'fo', 'fr', 'fy', 'ga', 'gaa', 'gd', 'gl', 'gn', 'gu', 'ha', 'haw', 'hi', 'hr', 'ht', 'hu', 'hy', 'ia', 'id', 'ig', 'is', 'it', 'iw', 'ja', 'jw', 'ka', 'kg', 'kk', 'km', 'kn', 'ko', 'kri', 'ku', 'ky', 'la', 'lg', 'ln', 'lo', 'loz', 'lt', 'lua', 'lv', 'mfe', 'mg', 'mi', 'mk', 'ml', 'mn', 'mo', 'mr', 'ms', 'mt', 'ne', 'nl', 'nn', 'no', 'nso', 'ny', 'nyn', 'oc', 'om', 'or', 'pa', 'pcm', 'pl', 'ps', 'pt-BR', 'pt-PT', 'qu', 'rm', 'rn', 'ro', 'ru', 'rw', 'sd', 'sh', 'si', 'sk', 'sl', 'sn', 'so', 'sq', 'sr', 'sr-ME', 'st', 'su', 'sv', 'sw', 'ta', 'te', 'tg', 'th', 'ti', 'tk', 'tl', 'tn', 'to', 'tr', 'tt', 'tum', 'tw', 'ug', 'uk', 'ur', 'uz', 'vi', 'wo', 'xh', 'xx-bork', 'xx-elmer', 'xx-hacker', 'xx-klingon', 'xx-pirate', 'yi', 'yo', 'zh-CN', 'zh-TW', 'zu'], domains=['com', 'al', 'dz', 'as', 'ad', 'am', 'ac', 'at', 'az', 'bs', 'by', 'be', 'bj', 'ba', 'vg', 'bg', 'bf', 'cm', 'ca', 'cv', 'cat', 'cf', 'td', 'cl', 'cn', 'cd', 'cg', 'ci', 'hr', 'cz', 'dk', 'dj', 'dm', 'tl', 'ec', 'ee', 'fm', 'fi', 'fr', 'ga', 'gm', 'ps', 'ge', 'de', 'gr', 'gl', 'gp', 'gg', 'gy', 'ht', 'hn', 'hu', 'is', 'iq', 'ie', 'im', 'it', 'jp', 'je', 'jo', 'kz', 'ki', 'kg', 'la', 'lv', 'li', 'lt', 'lu', 'mk', 'mg', 'mw', 'mv', 'ml', 'mu', 'md', 'mn', 'me', 'ms', 'nr', 'nl', 'ne', 'ng', 'nu', 'no', 'ps', 'pn', 'pl', 'pt', 'ro', 'ru', 'rw', 'sh', 'ws', 'sm', 'st', 'sn', 'rs', 'sc', 'sk', 'si', 'so', 'es', 'lk', 'sr', 'ch', 'tg', 'tk', 'to', 'tt', 'tn', 'tm', 'ae', 'vu']):
		self.results = results
		self.retry = retry
		self.socials = socials
		self.languages = languages
		self.domains = domains
		self.pdf_report = pdf_report
		self.pdf_timeout = pdf_timeout
		self.cache = cache
		self.sleep_min = sleep_min
		self.sleep_max = sleep_max
		logger.debug(f"\nRESULTS → {self.results} \nNUMBER RETRIES → {self.retry} \nSOCIALS → {self.socials} \nPDF REPORT → {self.pdf_report} \nPDF TIMEOUT → {self.pdf_timeout} \nCACHE → {self.cache} \nSLEEP RANGE → {self.sleep_min} - {self.sleep_max} s \nLANGUAGES → {len(self.languages)} \nDOMAINS → {len(self.domains)}")

	@abc.abstractmethod
	def search(self):
		pass

	def show(self, results):
		table = PrettyTable()
		for result in results:
			table.field_names = ["RATING", "RESULT"]
			table.align["RESULT"] = "l"
			table.add_row(["🔎", result["item"]])
			for rating, link in enumerate(result["links"]):
				table.add_row([rating + 1, link])
		print(table)

	@staticmethod
	def export(item, link, k):
		try:
			pdfkit.from_url(link, os.path.join(__base__, item, f"{str(k)} — {link.split('/')[2]}.pdf"))
		except Exception as e:
			logger.debug(f"EXPORT PDF EXCEPTION {k} {link} → {str(e)}")

	def pdf_reports(self, results):
		workers = mp.cpu_count() // 2 if mp.cpu_count() > 1 else mp.cpu_count()
		for result in results:
				with ThreadPoolExecutor(max_workers=workers) as executor:
					for count, link in enumerate(result["links"]):
						try:
							executor.submit(self.export, link=link, item=result["item"], k=count).result(timeout=self.pdf_timeout)
						except TimeoutError as e:
							logger.debug(f"EXPORT PDF TIMEOUT EXCEPTION {count} {link} → {str(e)}")
					executor.shutdown(wait=False)
					executor._threads.clear()
					cf_thread._threads_queues.clear()
	
	def cache_pkl(self, results):
		with open("tmp.pkl", "wb") as pkl:
			pickle.dump(results, pkl)

	@staticmethod
	def makedirs(items):
		for item in items:
			os.makedirs(os.path.join(__base__, item), exist_ok=True, mode=0o777)

	def use_social(self, searched, **kw):
		DOMAIN_BASE = ".com"
		ref = {S_VK: f"{S_VK}{DOMAIN_BASE}", S_IG: f"{S_IG}{DOMAIN_BASE}", S_TG: "t.me", S_TW: f"{S_TW}{DOMAIN_BASE}", S_YT: f"{S_YT}{DOMAIN_BASE}", S_FB: f"{S_FB}{DOMAIN_BASE}", S_TB: f"{S_TB}{DOMAIN_BASE}", S_SC: f"{S_SC}{DOMAIN_BASE}", S_TK: f"{S_TK}{DOMAIN_BASE}"}
		vk = Vk(**kw) if S_VK in self.socials else None
		instagram = Instagram(**kw) if S_IG in self.socials else None
		telegram = Telegram(**kw) if S_TG in self.socials else None
		youtube = Youtube(**kw) if S_YT in self.socials else None
		twitter = Twitter(**kw) if S_TW in self.socials else None
		facebook = Facebook(**kw) if S_FB in self.socials else None
		tumblr = Tumblr(**kw) if S_TB in self.socials else None
		snapchat = Snapchat(**kw) if S_SC in self.socials else None
		tiktok = Tiktok(**kw) if S_TK in self.socials else None
		results = {}
		workers = mp.cpu_count() // 2 if mp.cpu_count() > 1 else mp.cpu_count()
		for searched_item in searched:
			searched_item["socials"] = {}
			os.makedirs(os.path.join(__base__, searched_item["item"], S_IG), exist_ok=True, mode=0o777)
			os.makedirs(os.path.join(__base__, searched_item["item"], S_YT), exist_ok=True, mode=0o777)
			os.makedirs(os.path.join(__base__, searched_item["item"], S_TB), exist_ok=True, mode=0o777)
			os.makedirs(os.path.join(__base__, searched_item["item"], S_SC), exist_ok=True, mode=0o777)
			with ThreadPoolExecutor(max_workers=workers) as executor:
				for link in searched_item["links"]:
					if str(link).startswith("http"):
						if (ref[S_VK] in link.split("/")[2]) and not(vk is None):
							searched_item["socials"][S_VK] = executor.submit(vk.search, link=link, searched_item=searched_item["item"]).result()
						elif (ref[S_IG] in link.split("/")[2]) and not(instagram is None):
							searched_item["socials"][S_IG] = executor.submit(instagram.search, link=link, searched_item=searched_item["item"]).result()
						elif (ref[S_TG] in link.split("/")[2]) and not(telegram is None):
							searched_item["socials"][S_TG] = executor.submit(telegram.search, link=link, searched_item=searched_item["item"]).result()
						elif (ref[S_YT] in link.split("/")[2]) and not(youtube is None):
							searched_item["socials"][S_YT] = executor.submit(youtube.search, link=link, searched_item=searched_item["item"]).result()
						elif (ref[S_TW] in link.split("/")[2]) and not(twitter is None):
							searched_item["socials"][S_TW] = executor.submit(twitter.search, link=link, searched_item=searched_item["item"]).result()
						elif (ref[S_FB] in link.split("/")[2]) and not(facebook is None):
							searched_item["socials"][S_FB] = executor.submit(facebook.search, link=link, searched_item=searched_item["item"]).result()
						elif (ref[S_TB] in link.split("/")[2]) and not(tumblr is None):
							searched_item["socials"][S_TB] = executor.submit(tumblr.search, link=link, searched_item=searched_item["item"]).result()
						elif (ref[S_SC] in link.split("/")[2]) and not(snapchat is None):
							searched_item["socials"][S_SC] = executor.submit(snapchat.search, link=link, searched_item=searched_item["item"]).result()
						elif (ref[S_TK] in link.split("/")[2]) and not(tiktok is None):
							searched_item["socials"][S_TK] = executor.submit(tiktok.search, link=link, searched_item=searched_item["item"]).result()
						else:
							continue
					else:
						continue						
		return searched


class Google(Search):

	def search(self, items):

		def search_item(item, retry=0):
			url_search = f"https://www.google.{random.choice(self.domains)}/search?q={item.replace(' ', '+')}&num={self.results}&hl={random.choice(self.languages)}"
			try:
				response = requests.get(url_search, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'})
			except Exception as e:
				if retry < self.retry:
					retry = retry + 1
					search_item(item=item, retry=retry)
			else:
				soup = BeautifulSoup(response.text, 'html.parser')
				result_block = soup.find_all('div', attrs={'class': 'g'})
				for result in result_block:
					link = result.find('a', href=True)
					title = result.find('h3')
					if link and title:
						if str(link['href']).startswith("http"):
							yield link['href']
			finally:
				logger.debug(f"{response.status_code} SEARCHED URL → {url_search} RETRIES → {retry}")
				response.raise_for_status()
		assert len(items) > 0
		logger.debug(f"ITEMS 4 SEARCH → {items}")
		self.makedirs(items=items)
		results = []
		for item in items:
			results.append({"item": item, "links": list(search_item(item=str(item)))})
			time.sleep(random.uniform(self.sleep_min, self.sleep_max))
			if self.cache:
				self.cache_pkl(results=results)
		if self.pdf_report:
			self.pdf_reports(results=results)
		return results


class Rambler(Search):

	def search(self, items):

		def search_item(item, retry=0):
			url_search = f"https://nova.rambler.ru/search?query={quote(item.replace(' ', '+'))}&utm_source=head&utm_campaign=self_promo&utm_medium=form&utm_content=search"
			try:
				response = requests.get(url_search)
			except Exception as e:
				if retry < self.retry:
					retry = retry + 1
					search_item(item=item, retry=retry)
			else:
				soup = BeautifulSoup(response.text, 'html.parser')
				results = soup.find_all('article')
				for result in results:
					link = result.find_all('a')[0]['href']
					if "yabs.yandex.ru" in link:
						continue
					else:
						if str(link).startswith("http"):
							yield link
			finally:
				logger.debug(f"{response.status_code} SEARCHED URL → {url_search} RETRIES → {retry}")
				response.raise_for_status()
		assert len(items) > 0
		logger.debug(f"ITEMS 4 SEARCH → {items}")
		self.makedirs(items=items)
		results = []
		for item in items:
			results.append({"item": item, "links": list(search_item(item=str(item)))})
			time.sleep(random.uniform(self.sleep_min, self.sleep_max))
			if self.cache:
				self.cache_pkl(results=results)
		if self.pdf_report:
			self.pdf_reports(results=results)
		return results


class Social(metaclass=abc.ABCMeta):
	def __init__(self, posts_limit=10, export_data=True, export_format="csv", download_media=True):
		self.posts_limit = posts_limit
		self.export_data = export_data
		self.export_format = export_format
		self.download_media = download_media
		self.export_formats = ['csv', 'xls', 'html', 'json']
		self.stop_words = ["explore", "tags", "wall", "music"]

	@abc.abstractmethod
	def search(self):
		pass

	def export(self, social_net, array, username):
		data = pd.DataFrame(array)
		if self.export_format in self.export_formats[:3]:
			f = {self.export_formats[0]: data.to_csv, self.export_formats[1]: data.to_excel, self.export_formats[2]: data.to_html}
			f[self.export_format](f'{os.path.join(__base__, username, social_net)}.{self.export_format}', index=False)
		if self.export_format == self.export_formats[3]:
			with open(f'{os.path.join(__base__, username, social_net)}.{self.export_format}', "w") as f:
				json.dump({social_net: array}, f)
		logger.debug(f'{social_net} → {os.path.join(__base__, username, social_net)}.{self.export_format}')

	def get_user_from_link(self, link):
		return link.split('/')[3] if not (link.split('/')[3] in self.stop_words) else None        


class Instagram(Social):

	def search(self, link, searched_item):
		logger.debug(f"{S_IG} {link}")
		user = self.get_user_from_link(link)
		if self.download_media and not(user is None):
			os.chdir(os.path.join(__base__, searched_item, S_IG))
			'''ig = Instaloader()
			profile = Profile.from_username(ig.context, user)
			posts_sorted_by_likes = sorted(profile.get_posts(), key=lambda p: p.likes + p.comments, reverse=True)
			for post in islice(posts_sorted_by_likes, ceil(self.posts_limit)):
				ig.download_post(post, user)'''
			try:
				os.system(f"instaloader {user} --count {self.posts_limit}")
			except Exception as e:
				logger.debug(f"{S_IG} {user} {str(e)}")
			os.chdir(__base__) 
		return user


class Vk(Social):
	def search(self, link, searched_item):
		logger.debug(f"{S_VK} → {link}")
		user = self.get_user_from_link(link)
		if user is None:
			return user
		else:
			vks = []
			for l, vk in enumerate(sns_vk.VKontakteUserScraper(user).get_items()):
				if l == self.posts_limit:
					break
				vks.append({'url': vk.url, 'content': vk.content})
			if self.export_data:
				self.export(social_net=S_VK,array=vks, username=searched_item)
			return vks


class Telegram(Social):
	def search(self, link, searched_item):
		logger.debug(f"{S_TG} → {link}")
		user = self.get_user_from_link(link)
		if user is None:
			return user
		else:
			tgs = []
			for l, tg in enumerate(sns_tg.TelegramChannelScraper(name=user).get_items()):
				if l == self.posts_limit:
					break
				tgs.append({'date': tg.date, 'url': tg.url, 'content': tg.content})
			if self.export_data:
				self.export(social_net=S_TG,array=tgs, username=searched_item)
			return tgs


class Facebook(Social):
	def search(self, link, searched_item):
		logger.debug(f"{S_FB} → {link}")
		user = self.get_user_from_link(link)
		if user is None:
			return user
		else:
			fbs = []
			for l, fb in enumerate(get_posts(user, pages=self.posts_limit)):
				if l == self.posts_limit:
					break
				fbs.append(fb)
			if self.export_data:
				self.export(social_net=S_FB,array=fbs, username=searched_item)
			return fbs


class Twitter(Social):
	def search(self, link, searched_item):
		logger.debug(f"{S_TW} → {link}")
		user = self.get_user_from_link(link)
		if user is None:
			return user
		else:
			tws = []
			for l, tw in enumerate(sns_tw.TwitterSearchScraper(query=user).get_items()):
				if l == self.posts_limit:
					break
				tws.append({'username': tw.username, 'url': tw.url, 'content': tw.content})
			if self.export_data:
				self.export(social_net=S_TW,array=tws, username=searched_item)
			return tws


class Youtube(Social):

	@staticmethod
	def get_user_from_link(link):
		return link.split('/')[4] if (link.split('/')[3] == "channel") or (link.split('/')[3] == "c") else None

	def search(self, link, searched_item):
		logger.debug(f"{S_YT} → {link}")
		user = self.get_user_from_link(link)
		if self.download_media:
			os.chdir(os.path.join(__base__, searched_item, S_YT))
			try:
				os.system(f"youtube-dl {link} --playlist-end {self.posts_limit}")
			except Exception as e:
				logger.debug(f"{S_YT} {link} {str(e)}")
			os.chdir(__base__)
		return user


class Tumblr(Social):

	@staticmethod
	def get_user_from_link(link):
		return link.split("/")[2].split(".")[0]

	def search(self, link, searched_item):
		logger.debug(f"{S_TB} → {link}")
		user = self.get_user_from_link(link)
		if self.download_media:
			os.chdir(os.path.join(__base__, searched_item, S_TB))
			client = Tumblpy(app_key='zLgPh6LeV7DyczfPALkTEfr8rOgzcYAY8TzAlabVIYrgpATPON', app_secret='mGP5mVle2ZUNKHzK4ayjAGpfUCkLTmQm91ic9YtWTTcDkdFLPE', oauth_token='hRwAn1CoZJ5Q96T8o51aQL2YcKnh1k66RlnCRLQtqjtWf0WZ4W', oauth_token_secret='oqlple5FP9MVRTxbUQHjrEVSs4DDLFP7h4zBE5D4g952qeqRo3')
			photo4download, video4download, youtube4download = [], [], []
			try:
				for x in client.posts(user)['posts']:
					if x["type"] == "photo":
						for ph in x["photos"]:
							photo4download.append(ph["original_size"]["url"])
					if x["type"] == "video":
						if x["video_type"] == S_TB:
							video4download.append(x["video_url"])
						if x["video_type"] == S_YT:
							youtube4download.append(x['permalink_url'])
				for media in photo4download + video4download:
					with open(media.split("/")[-1], "wb") as f:
						f.write(requests.get(media, allow_redirects=True).content)
				if len(youtube4download) > 0:
					youtube = Youtube(posts_limit=self.posts_limit, export_data=self.export_data, export_format=self.export_format, download_media=self.download_media)
					for link in youtube4download:
						youtube.search(link=link, searched_item=searched_item["item"])
			except Exception as e:
				logger.debug(f"{S_TB} {link} {str(e)}")
			os.chdir(__base__)
		return user


class Tiktok(Social):

	@staticmethod
	def get_user_from_link(link):
		if "?" in link.split("/")[3]:
			return link.split("/")[3][1:link.split("/")[3].index("?")] if link.split("/")[3].startswith("@") else None
		else:
			return link.split("/")[3][1:] if link.split("/")[3].startswith("@") else None

	def search(self, link, searched_item):
		logger.debug(f"{S_TK} → {link}")
		user = self.get_user_from_link(link)
		if user is None:
			return user
		else:
			tks = []
			try:
				tik_tok.run(user) 
				tks.append({"nickname": tik_tok.nickname(), "followers": tik_tok.followers(), "following": tik_tok.following(), "likes": tik_tok.likes(), "status": tik_tok.status(), "avatar_link": tik_tok.getavatar()})
			except Exception as e:
				logger.debug(f"{S_TK} {link} {str(e)}")
			else:
				if self.export_data:
					self.export(social_net=S_TK,array=tks, username=searched_item)
			return tks


class Snapchat(Social):

	@staticmethod
	def get_user_from_link(link):
		return link.split("/")[4] if (link.split('/')[3] == "u") or (link.split('/')[3] == "add") else None

	def search(self, link, searched_item):
		logger.debug(f"{S_SC} → {link}")
		user = self.get_user_from_link(link)
		if self.download_media and not(user is None):
			os.chdir(os.path.join(__base__, searched_item, S_SC))
			try:
				os.system(f"snapchat-dl {user} -l {self.posts_limit}")
			except Exception as e:
				logger.debug(f"{S_SC} {link} {str(e)}")
			os.chdir(__base__)
		return user


__all__ = ["Google", "Rambler"]
