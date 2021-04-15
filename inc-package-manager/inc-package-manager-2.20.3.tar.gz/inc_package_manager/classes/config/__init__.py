#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# inc imports.
from dev0s.shortcuts import *
import w3bsite 

# alias.
ALIAS = "inc-package-manager"

# source.
SOURCE = Directory(dev0s.defaults.source_path(__file__, back=3))
OS = dev0s.defaults.operating_system(supported=["linux", "macos"])

# checks.
dev0s.defaults.alias(alias=ALIAS, executable=f"{SOURCE}", venv=f"{SOURCE}/venv/")

# production settings.
# do not deploy with production disabled.
PRODUCTION = dev0s.env.get("PRODUCTION", format=bool, default=True)

# database.
DATABASE = Database(f"/etc/{ALIAS}/")
if not Files.exists(str(DATABASE)[:-1]):
	print(f"{color.orange}Root permissions{color.end} required to create database {DATABASE}.")
	os.system(f"sudo mkdir {DATABASE} && sudo chown -R {dev0s.defaults.vars.user}:{dev0s.defaults.vars.group} {DATABASE} && sudo chmod -R 770 {DATABASE}")


# limit website init.
if dev0s.system.env.get("INC_PACKAGE_MANAGER_CLI", format=bool, default=True):
	
	# website.
	website = w3bsite.Website(
		# main.
		root=str(SOURCE),
		database=str(DATABASE),
		library=f"/usr/local/lib/{ALIAS}",
		domain="127.0.0.1:52940",
		name="IncPackageManager",
		remote=None,
		# the template data (only required when running the website) (overwrites the w3bsite template data keys).
		template_data={
			"COLORS":{
				"white":"#FAFAFA",
				"light_white":"#E9F0FD",
				"grey":"#E5E5E5",
				"light_grey":"#D6D6D6",
				"dark_grey":"#424242",
				"blue":"#5A8FE6",
				"purple":"#323B83",#"#B32FCA",
				#"purple":"#9B00AA",
				"red":"#FD304E",
				"pink":"#F62B7D",
				"orange":"#FF8800",
				"green":"#006633",
				"darkest":"#1F2227",
				"darker": "#20242A",
				"dark": "#262B30",
				# background color.
				"topbar":"#323B83",#1F2227", #"#FAFAFA",
				"background":"#323B83",#"#E7E9EF", #"#FAFAFA",
				"topbar_darkmode":"#1F2227",#1F2227", #"#FAFAFA",
				"background_darkmode":"#1F2227",#"#E7E9EF", #"#FAFAFA",
				# elements.
				"widgets":"#FAFAFA",
				"widgets_reversed":"#323B83",#"#1F2227",
				"widgets_darkmode":"#323B83",
				"widgets_reversed_darkmode":"#20242A",#"#1F2227",
				# text.
				"text":"#1F2227",
				"text_reversed":"#FAFAFA",
				"text_darkmode":"#FAFAFA",
				"text_reversed_darkmode":"#FAFAFA",
				# input & textareas.
				"input_txt":"#1F2227",
				"input_txt_reversed":"#FAFAFA",
				"input_bg":"#FAFAFA",
				"input_bg_reversed":"#323B83",
				# buttons.
				"button_txt":"#FAFAFA",
				"button_txt_reversed":"#1F2227",
				"button_bg":"#323B83",
				"button_bg_reversed":"#FAFAFA",
				# custom colors.
				# ...
			},
		},
		# custom styling.
		styling={
			"LEFTBAR_WIDTH":"280px", # px
			"RIGHTBAR_WIDTH":"280px", # px
			"TOPBAR_HEIGHT":"50px", #px
		},
		# 	the organization name.
		organization="VanDenBerghInc",
		# aes.
		#aes_passphrase=CONFIG["aes"]["master"],
		# options.
		namecheap_enabled=False,
		firebase_enabled=False,
		stripe_enabled=False,
		email_enabled=False,
		interactive=False,
		_2fa=False,
		production=PRODUCTION,
	)
