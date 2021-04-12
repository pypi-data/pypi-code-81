#!/usr/bin/env python
# -*- coding: utf-8 -*-

###################
#    This file implement the SmtpClient.
#    Copyright (C) 2020  Maurice Lambert

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
###################

""" This file implement the SmtpClient. """

import smtplib
import logging

try:
    from .Email import Email, AdressError
except ImportError:
    from Email import Email, AdressError

__all__ = ["SmtpClient"]


class SmtpClient:

    """This class send email with SMTP protocol."""

    def __init__(
        self,
        smtp=None,
        port=25,
        username=None,
        password=None,
        use_tls=True,
        use_gpg=True,
        debug=False,
    ):
        self.smtp = smtp
        self.port = port
        self.username = username
        self.password = password
        self.use_tls = use_tls
        self.use_gpg = use_gpg
        self.debug = debug

    def send(
        self, email: Email, from_: str, to: list, name: str = "PyEmailTools"
    ) -> None:

        """ This method send an email. """

        logging.debug("Check email address.")
        to = self.get_valid_receivers(to, email)
        from_ = self.get_valid_receivers([from_], email)

        if len(from_) != 1:
            raise AdressError("Source address is invalid.")

        if len(to) == 0:
            raise AdressError("Destination addresses are not valid.")

        logging.info("Sending email...")

        self.mailserver = smtplib.SMTP(self.smtp, self.port)
        self.mailserver.ehlo(name)
        self.mailserver.helo(name)

        if self.debug:
            self.mailserver.set_debuglevel(1)
        if self.use_tls:
            logging.info("Starting TLS...")
            self.mailserver.starttls()
            self.mailserver.ehlo(name)
            self.mailserver.helo(name)
        if self.username and self.password:
            logging.debug("Authentication...")
            self.mailserver.login(self.username, self.password)

        self.mailserver.sendmail(from_, to, email.email.as_string())
        self.mailserver.quit()

        logging.debug("Email is sent.")

    def get_valid_receivers(self, addressS, email):

        """This method return valid addresses.
        If address isn't valid you get a error log in your
        logging file with the specific address."""

        receivers = []
        for address in addressS:
            email_ = email.check_email(address)
            if email_ and isinstance(email_, str):
                logging.debug(f"{email_} is valid.")
                receivers.append(email_)
        return receivers
