"""This file is part of Pyxgram.

   Pyxgram is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.

   Pyxgram is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with Pyxgram.  If not, see <http://www.gnu.org/licenses/>. """

from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from functools import partial
import time
import os
import telegram

class Logger:
    def __init__(self,logfile,separator=True):
        self.logfile=logfile
        if separator:
            self.log_separator()
        if os.path.exists(self.logfile)==False:
            with open(self.logfile,'w') as self.main_file:
                self.main_file.write('Log created at '+time.strftime("%H:%M:%S")+'\n')
        with open(self.logfile,'a') as self.main_file:
            self.main_file.write('Log started at '+time.strftime("%H:%M:%S")+'\n')
        print('Log started at '+time.strftime("%H:%M:%S"))
    def log_separator(self):
        with open(self.logfile,'a') as self.main_file:
            self.main_file.write('\n\nSeparator\n\n')
    def error(self,error):
        with open(self.logfile,'a') as self.main_file: 
            self.main_file.write('Error at '+time.strftime("%H:%M:%S")+': '+error+'\n')
        print('Error at '+time.strftime("%H:%M:%S")+': '+error)
    def info(self,info):
        with open(self.logfile,'a') as self.main_file:
            self.main_file.write('Info at '+time.strftime("%H:%M:%S")+': '+info+'\n')
        print('Info at '+time.strftime("%H:%M:%S")+': '+info)
    def clear(self):
        with open(self.logfile,'a') as self.main_file:
            self.main_file.write('')
        with open(self.logfile,'a') as self.main_file:
            self.main_file.write('Log cleared at '+time.strftime("%H:%M:%S")+'\n')
        print('Log cleared at '+time.strftime("%H:%M:%S"))

class BaseBot:
    def __init__(self,token,include=True):
        """BaseBot its the main class of pyxtgram module."""
        self.updater=Updater(token=token)
        self._help=''
        self.dispatcher=self.updater.dispatcher
        self.log=Logger('bot.log')
        self.log.info('Bot created')
        if include:
            from include import separator,admin_id
            self.admin_id=admin_id
            self.separator=separator
        else:
            self.admin_id=None
            self.separator='-'
    def error_handler(self,update: Update,context: CallbackContext,function):
        try:
            function(update,context)
        except ValueError as err:
            self.log.error('Value Error')
            self.log.error(str(err))
        except ZeroDivisionError as err:
            self.log.error('ZeroDivisionError')
            self.log.error(str(err))
        except Exception as err:
            self.log.error('A unknow error as ocurred')
            self.log.error(err)
    def normal_command(self,function):
        """Adds a command. Its a shorcut for dispatcher.add_handler(CommandHandler)"""
        self.dispatcher.add_handler(CommandHandler(function.__name__,partial(self.error_handler,function=function)))
        self._help+='/'+function.__name__+self.separator+str(function.__doc__)+'\n\n'
        self.log.info('Added a new command')
    def admin_pass(self,update:Update,context:CallbackContext,function):
        """This is a minimal subfunction of admin_command decorator"""
        if update.message.chat_id==self.admin_id:
            function(update,context)
        else:
            self.log.info('A person trying to access to a admin function')
    def admin_command(self,function):
        """The admin_command function uses the admin_id from the include.py file
        you can set this with <class>.admin_id=id replacing id with our id."""
        self.log.info('Added a Admin Command')
        self.dispatcher.add_handler(CommandHandler(function.__name__,partial(self.admin_pass,function=function)))
    def package_add(self,packagename):
        exec('from '+packagename+' import initial',globals())
        initial(self)
        self.log.info('Added the package '+packagename)
    def typing(self,update,context):
        """Send's the typing chat action"""
        context.bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
    def start(self):
        """Start's the bot and all the systems"""
        try:
            self.updater.start_polling()
            self.updater.idle()
            self.log.info('Bot started')
        except telegram.error.NetworkError as error:
            self.log.error('Network Error')
            self.log.error(str(error))
    def reply(self,text,update):
        """Reply a message with a text.
        This is a shorcut for the
        update.message..reply_text
        function"""
        update.message.reply_text(text)
    def send_text(self,text,update,context,chat_id=None):
        """Send a message with a text
        This i a shorcut for the
        bot.send_message or
        context.bot.send_message"""
        if chat_id==None:
            chat_id=update.message.chat_id
        context.bot.send_message(chat_id,text)

bot=BaseBot('1654011024:AAEajJrasZ4GiKJr1LjzN-zFbaDmIhlkwnc',include=False)

bot.start()