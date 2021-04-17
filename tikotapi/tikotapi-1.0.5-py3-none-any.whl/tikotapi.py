import time
import os

logins = ["api", "tikot", "developer", "dev", "tikotshop"] #For add login write: , "login"
passwords = ["pass", "p", "api", "tikotshop", "developer", "dev", "tikot"] #For add password write: , "password"
raitings = ["3+", "6+", "7+", "12+", "16+", "18+"] #Don't edit!
notesaccounts = ["i001"] #For add account write: , (Examples) "i001, i002, i003, i004"
secretkeys = ["Kzk1WKyRepTxsfjfP6K37ibeM3EJ20ZIL6ioFPxJflGZgebbQW"]

def test(): # Testing creating files by library
	print("Testing tiny create files")
	os.mkdir("test files")
	os.chdir("test files")
	print("Test file 1 created!")
	test1 = open("test1.test", "w")
	test1.write("Hello")
	print("Test file 2 created!")
	test2 = open("test2.test", "w")
	test2.write("Hello user!")
	print("Test file 3 created!")
	test3 = open("test3.test", "w")
	test3.write("Hello user! The")
	print("Test file 4 created!")
	test4 = open("test4.test", "w")
	test4.write("Hello user! The test!")
	test5 = open("test5.test", "w")
	test5.write("Hello user! The test!\nTikOt API")
	panelts = open("panel_tikotshop.py", "w")
	panelts.write("import tikotapi\ntikotapi.panel_tikotshop(\"login\", \"password\")")
	paneltw = open("panel_tikotworks.py", "w")
	paneltw.write("import tikotapi\ntikotapi.panel_tikotworks(\"login\", \"password\")")
	print("Test completed! Creating log file...")
	time.sleep(2)
	print("Adding file")
	logtest = open("logtest.log", "w")
	time.sleep(4)
	print("Creating text")
	time.sleep(20)
	logtest.write("[Message] Test file 1 created!\n[Message] Test file 2 created!\n[Message] Test file 3 created!\n[Secret warning] Preparing to create a log file\n[Message] Test file 4 created!\n[Messsage] Test completed! Creating log file...")

def panel_tikotshop(login2, password2):
	if login2 not in logins:
		print("Invalid login in args!")
	elif password2 not in passwords:
		print("Invalid password in args!")
	else:
		print("Welcome " + login2 + "! Press enter secret key")
		secretkey = input("")
		if secretkey not in secretkeys:
			print("Invalid key! Get key in developer panel")
			print("List keys:\n1. *****KyRepTxsfjfP6K37ibeM3EJ20ZIL6ioFPx***********")
			print("If your key not is this list send message in mail: tikotstudio@yandex.ru")
		elif secretkey == secretkeys[0]:
			print("8DirectLabirint - 8ДириктоЛабиринт")
			print("Raiting: " + raitings[0])
			print("Loaded on downloader: ProdaFile.ru")

			yn1 = input("Yes/No? ")
			if yn1 == "Yes":
				print("Statistic game: CRT: 1% Downloads: 1004")
				print("Name: 8DirectLabirint\nRaiting: 3+\nDate publish: 22.02.2021.19:50 Vladivastok")
				print("Price: 1$")
				print("Type games/status: public")
				print("Others types (not your game): draft, not checked")
			elif yn1 == "No":
				print("View your secret key in developer panel!")
			else:
				print("Aborted!")


def tutorial():
	print("Welcome to tutorial in TIKOT API 1.0.5! I'm learn your using this API!")
	print("Write \"next\" for start learn")
	tutorialnext1 = input("")

	nexts = ["next", "Next"]

	if tutorialnext1 == nexts[0] or tutorialnext1 == nexts[1]:
		print("Testing module. 1.")
		print("For testing module you need to enter tikotapi.connect()\nbut there is an easier method! tikotapi.test(\"login\", \"password\")")
		print("---")
		print("For next learning api write: next")
		tutorialnext2 = input("")

		if tutorialnext2 == nexts[0] or tutorialnext2 == nexts[1]:
			print("Connecting game. 2.")
			print("Connecting to analitic your game write:\npanel_tikotshop(\"login\", \"password\")")
			print("Will write to you: Hello USERNAME! Plase enter secret key")
			print("Your write secret key")
			print("Show: name game and rait game. If this game your then we write Yes and if not then we write No")
			print("If your write Yes then show this info:\nCRT, DOWNLOADS, NAME GAME, RAIT GAME and DATE PUBLISH")

			print("---")
			print("To dashboard in site your game:")
			print("Raiting, name game, first name creator game, last name creator game,\nDate publication game, SECRET KEY GAME, name main script")
			print("what is written in the caps then it will come in handy for us")

	elif tutorialnext1 not in nexts:
		print("Error! Write: next or Next")


def panel_noteinfile(login5, password5):
	print("Your write note = your note save in file")
	noteacc = input("Write id (EXAMPLES: i001, i002, i003) ")

	if login5 not in logins:
		print("Invalid login!")
	elif password5 not in passwords:
		print("Invalid password!")
	else:
		if noteacc not in notesaccounts:
			print("Invalid user!")
			print("Open the script and add in list notesaccounts your id (1. 001 2. 002 3. 003)")
		else:
			print("Login completed! Loading...")
			time.sleep(2)
			print("Hello " + noteacc + "!")
			note = input("Your note: ")

			os.mkdir("Notes")
			os.chdir("Notes")
			yournote = open("note.txt", "w")
			yournote.write("Your note: " + note + "\nTIKOT API 1.0.4:).")
			print("If you want to make 1 more note,\n then you must move the note.txt file to another location and delete the \"Notes\" folder.")
			print("---")
			print("Tutorial in tikotapi.tk")