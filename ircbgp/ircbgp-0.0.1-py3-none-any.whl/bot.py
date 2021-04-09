#! /usr/bin/env python3
#
# Florian Streibelt <florian.streibelt@streibelt.net>

import sys
import argparse
import time
import irc.client
import jaraco.logging
import logging

from ircbgp import __version__ as libversion
__version__ = libversion


class BGP:

    def __init__(self, channels, asn, prefixname):

        self.channels = channels
        self.asn = asn
        self.prefixname = prefixname

        self.peers = {}
        self.routes = {}

        if asn:
            self.routes[prefixname] = ( 'local' ,[])


    def reset(self, connection, channel):
        connection.privmsg(channel, f"notice: RESET done. Who are you?")

        self.peers[channel] = {}
        self.update_grt(connection)


    def sendto(self, connection, recipient, text):

        recipient=recipient.strip()

        if not recipient in self.routes:
            logging.info(f"No route to {recipient}")
            return False

        channel, aspath = self.routes.get(recipient)
        connection.privmsg(channel, f"msg:{recipient}:{text}")
        return True


    def announcement(self, connection, channel, prefix, the_aslist):

        as_path = ', '.join(map(lambda x:'AS%s'%str(x),the_aslist))

        if self.asn in the_aslist:
            logging.info(f"{channel} announcement rejected, found my ASN in announcement for {prefix}: {as_path}")
            return

        if self.prefixname == prefix:
            logging.info(f"{channel} announcement rejected, found myself in announcement for {prefix}: {as_path}")
            return

        logging.info(f"{channel} received ANNOUNCE {prefix} via {as_path}")

        # save the announcement for this channel/peer:
        routes = self.peers.get(channel, {})
        routes[prefix] = the_aslist
        self.peers[channel] = routes

        self.update_grt(connection)


    def dump_tables(self, changed_prefixes=None):

        logging.info("peer routing tables:")
        for channel, routes in self.peers.items():
            logging.info(f"in channel: {channel}:")
            for prefix, aslist in routes.items():
                as_path = ', '.join(map(lambda x:'AS%s'%str(x), aslist))
                logging.info(f"   {channel:20s} {prefix:20s} via {as_path}")

        logging.info("GRT:")
        for prefix, (source, as_list) in self.routes.items():
            u = ' '
            if changed_prefixes and prefix in changed_prefixes:
                u = '*'
            logging.info(f"{u}  {source:20s} {prefix:20s} via {str(as_list)}")


    def update_grt(self, connection):

        self.dump_tables()

        changed_prefixes = set()
        for channel, routes in self.peers.items():
            for prefix, as_list in routes.items():

                # get entry from current grt
                grt_entry = self.routes.get(prefix)
                if grt_entry:
                    source, current_aslist = grt_entry
                    if len(current_aslist) > len(as_list):
                        logging.info(f"prefix {prefix}: current aslist len={len(current_aslist)} > {len(as_list)}")
                        self.routes[prefix] = (channel, as_list)
                        changed_prefixes.add(prefix)
                else:
                    # no route yet, so add the new one
                    self.routes[prefix] = (channel, as_list)
                    changed_prefixes.add(prefix)

        self.dump_tables(changed_prefixes)

        for channel in self.channels:
            # only send changed prefixes:
            self.repeat(connection, channel, filter_prefixes=changed_prefixes)


    def repeat(self, connection, channel, filter_prefixes=None):

        for prefix, (source, as_list) in self.routes.items():
            if filter_prefixes is not None:
                # do not re-ennounce unchanged prefixes
                if prefix not in filter_prefixes:
                    continue

                # this would trigger reannouncements all the time
                if source=='local':
                    continue

            if source != channel:
                as_path = ', '.join(map(lambda x:'AS%s'%str(x), as_list + [self.asn,]))
                # if we want to later support differnet commands add the prefix:
                # connection.privmsg(channel, f"ANNOUNCE {prefix}: {as_path}")
                connection.privmsg(channel, f"{prefix}: {as_path}")
                logging.info(f"{channel} sending ANNOUNCE {prefix} via {as_path}")


    def send_hello(self, connection, channel):
        self.repeat(connection, channel)



class IRCCat(irc.client.SimpleIRCClient):

    def __init__(self, args):
        irc.client.SimpleIRCClient.__init__(self)
        self.args = args
        self.bgp = BGP(args.channels, args.asn, args.nickname)


    def on_welcome(self, connection, event):
        logging.info("joining...")
        for channel in self.args.channels:
            connection.join(channel)


    def on_pubmsg(self, connection, event):
        try:
            message = event.arguments[0]
        except:
            return

        for ign in ('error:', 'notice:'):
            if message.lower().startswith(ign):
                return

        source_nick = event.source.split('!',1)
        if source_nick[0] == self.args.nickname:
            logging.info("ignoring our own message")
            return

        channel = event.target.strip()

        # check if this is one of the valid channels,
        # check the syntax of the message,
        # send it to our "router" instance.

        if channel in self.args.channels:
            if message.strip().lower() == "help":
                connection.privmsg(channel, f"notice: Hi, I am {self.args.nickname}, a very simple bot.")
                time.sleep(.2)
                connection.privmsg(channel, "notice: I understand the public commands help, reset, and repeat.")
                time.sleep(.2)
                connection.privmsg(channel, "notice: The command reset will make me forget everything I learned from you.")
                time.sleep(.1)
                connection.privmsg(channel, "notice: The command repeat will repeat my announcements to you.")
            elif message.strip().lower() == "reset":
                self.bgp.reset(connection, channel)
            elif message.strip().lower() == "repeat":
                self.bgp.repeat(connection, channel)
            elif message.strip().lower().startswith('msg:'):
                cmd, recipient, text = message.strip().split(':')
                if recipient == self.args.nickname:
                    logging.notice(f"MESSAGE RECEIVED: {message}")
                else:
                    if self.bgp.sendto(connection, recipient,text):
                        connection.privmsg(channel, f"notice: message sent")
                    else:
                        connection.privmsg(channel, f"error: no route found")
                    return
            else:
                if not ':' in message:
                    logging.info(f"{channel} message '{message}' not understood, no colon")
                    connection.privmsg(channel, f"error: An announcement needs a ':' after the nickname, like:  'Fritz: AS123'")
                    return

                prefix, rest = message.split(':', 1)
                prefix=prefix.strip()
                rest=rest.strip()

                if ':' in rest:
                    logging.info(f"{channel} message '{message}' not understood, colon in aslist?")
                    connection.privmsg(channel, f"error: There is only one ':' allowed, like:  'Fritz: AS123 AS456'")
                    return

                aslist = rest.replace(',',' ').split()
                the_aslist =  []
                for asn in aslist:
                    asn = asn.strip().upper()
                    if asn == 'AS': #somebody typed AS 123 AS 456
                        continue
                    try:
                        asn=asn.replace('AS','')
                        asn = int(asn)
                        the_aslist.append(asn)
                    except ValueError:
                        logging.info(f"{channel} message '{message}' ASN '{asn}' is not numeric")
                        connection.privmsg(channel, f"error: AS-number in '{asn}' is not numeric, like:  'Fritz: AS123 AS456'")
                        return

                self.bgp.announcement(connection, channel, prefix, the_aslist)

        else:
            logging.info(f"reveived a message in channel {channel} that I am not configured for")


    def on_privmsg(self, connection, event):
        logging.info (event)
        try:
            msg = event.arguments[0]
            if msg.strip().lower()=="quit":
                self.connection.quit(f"bye, terminated by {event.source}")
        except:
            pass

        connection.privmsg(event.source, "Sorry, I am just a bot that does not understand private messages...")


    def on_join(self, connection, event):

        nickname, _rest = event.source.split('!',1)

        if nickname==self.args.nickname:
            logging.info(f"I successfully joined {event.target}!")
            self.connection.privmsg(event.target, f"notice: Hi! Your friendly BSG bot {self.args.nickname} just joined the channel!")
        else:
            logging.info(f"{nickname} successfully joined {event.target}!")
            self.connection.privmsg(event.target, f"notice: Hi, {nickname} I am {self.args.nickname}, your friendly BGP bot!")

        self.connection.privmsg(event.target, f"notice: Just type 'help' in this channel if you need help!")

        time.sleep(1) # risking a timeout but increase the chanceof the message beeing seen
        self.bgp.send_hello(connection, event.target) # this will also send our local ASN


    def on_disconnect(self, connection, event):
        sys.exit(0)

    def on_erroneusnickname(self, connection, event):
        sys.exit(event)

    def on_error(self, connection, event):
        sys.exit(event)
        sys.exit(0)



def get_args():

    def parse_channels(chans):

        chan_list = []

        if not isinstance(chans, str):
            raise ValueError("channels must be a string")

        try:
            for chan in chans.split(','):
                try:
                    chan=chan.strip()
                    if not chan.startswith('#'):
                        raise argparse.ArgumentTypeError(f"{chan} does not start with #!")
                    chan_list.append(chan)
                except ValueError:
                    raise argparse.ArgumentTypeError(f"{chan} is not a valid channel name!")
        except (KeyError, ValueError):
            raise argparse.ArgumentTypeError(f"error parsing {chans} as list of AS-numbers!")

        if len(chan_list)<1:
            raise argparse.ArgumentTypeError(f"unable to find channels in {chans}!")

        return chan_list

    parser = argparse.ArgumentParser()
    parser.add_argument('nickname', type=str, help="Name of the bot (or 'prefix')")
    parser.add_argument('asn', type=int, help="one integer with the own AS number")
    parser.add_argument('channels', type=parse_channels, help="comma separated list of channels to join")
    parser.add_argument('--version', action='version', version='%(prog)s ' + libversion)
    parser.add_argument('-s', '--server', default='127.0.0.1', type=str)
    parser.add_argument('-p', '--port', default=6667, type=int)
    jaraco.logging.add_arguments(parser)
    return parser.parse_args()


def main():

    args = get_args()
    jaraco.logging.setup(args)

    c = IRCCat(args)
    try:
        c.connect(args.server, args.port, args.nickname)
    except irc.client.ServerConnectionError as x:
        logging.info(x)
        sys.exit(1)
    c.start()


if __name__ == '__main__':
    main()
