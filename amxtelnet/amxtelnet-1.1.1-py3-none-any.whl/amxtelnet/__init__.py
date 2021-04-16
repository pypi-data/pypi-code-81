import asyncio
from logging import debug, info, warning, error
import asyncio
import re
import sys
import socket
import selectors
from time import monotonic as _time


# Telnet constants (do not modify)
TELNET_PORT = 23

IAC  = bytes([255]) # "Interpret As Command"
DONT = bytes([254])
DO   = bytes([253])
WONT = bytes([252])
WILL = bytes([251])
theNULL = bytes([0])
SE  = bytes([240])  # Subnegotiation End
NOP = bytes([241])  # No Operation
DM  = bytes([242])  # Data Mark
BRK = bytes([243])  # Break
IP  = bytes([244])  # Interrupt process
AO  = bytes([245])  # Abort output
AYT = bytes([246])  # Are You There
EC  = bytes([247])  # Erase Character
EL  = bytes([248])  # Erase Line
GA  = bytes([249])  # Go Ahead
SB =  bytes([250])  # Subnegotiation Begin
BINARY = bytes([0]) # 8-bit data path
ECHO = bytes([1]) # echo
RCP = bytes([2]) # prepare to reconnect
SGA = bytes([3]) # suppress go ahead
NAMS = bytes([4]) # approximate message size
STATUS = bytes([5]) # give status
TM = bytes([6]) # timing mark
RCTE = bytes([7]) # remote controlled transmission and echo
NAOL = bytes([8]) # negotiate about output line width
NAOP = bytes([9]) # negotiate about output page size
NAOCRD = bytes([10]) # negotiate about CR disposition
NAOHTS = bytes([11]) # negotiate about horizontal tabstops
NAOHTD = bytes([12]) # negotiate about horizontal tab disposition
NAOFFD = bytes([13]) # negotiate about formfeed disposition
NAOVTS = bytes([14]) # negotiate about vertical tab stops
NAOVTD = bytes([15]) # negotiate about vertical tab disposition
NAOLFD = bytes([16]) # negotiate about output LF disposition
XASCII = bytes([17]) # extended ascii character set
LOGOUT = bytes([18]) # force logout
BM = bytes([19]) # byte macro
DET = bytes([20]) # data entry terminal
SUPDUP = bytes([21]) # supdup protocol
SUPDUPOUTPUT = bytes([22]) # supdup output
SNDLOC = bytes([23]) # send location
TTYPE = bytes([24]) # terminal type
EOR = bytes([25]) # end or record
TUID = bytes([26]) # TACACS user identification
OUTMRK = bytes([27]) # output marking
TTYLOC = bytes([28]) # terminal location number
VT3270REGIME = bytes([29]) # 3270 regime
X3PAD = bytes([30]) # X.3 PAD
NAWS = bytes([31]) # window size
TSPEED = bytes([32]) # terminal speed
LFLOW = bytes([33]) # remote flow control
LINEMODE = bytes([34]) # Linemode option
XDISPLOC = bytes([35]) # X Display Location
OLD_ENVIRON = bytes([36]) # Old - Environment variables
AUTHENTICATION = bytes([37]) # Authenticate
ENCRYPT = bytes([38]) # Encryption option
NEW_ENVIRON = bytes([39]) # New - Environment variables
TN3270E = bytes([40]) # TN3270E
XAUTH = bytes([41]) # XAUTH
CHARSET = bytes([42]) # CHARSET
RSP = bytes([43]) # Telnet Remote Serial Port
COM_PORT_OPTION = bytes([44]) # Com Port Control Option
SUPPRESS_LOCAL_ECHO = bytes([45]) # Telnet Suppress Local Echo
TLS = bytes([46]) # Telnet Start TLS
KERMIT = bytes([47]) # KERMIT
SEND_URL = bytes([48]) # SEND-URL
FORWARD_X = bytes([49]) # FORWARD_X
PRAGMA_LOGON = bytes([138]) # TELOPT PRAGMA LOGON
SSPI_LOGON = bytes([139]) # TELOPT SSPI LOGON
PRAGMA_HEARTBEAT = bytes([140]) # TELOPT PRAGMA HEARTBEAT
EXOPL = bytes([255]) # Extended-Options-List
NOOPT = bytes([0])

if hasattr(selectors, 'PollSelector'):
    _TelnetSelector = selectors.PollSelector
else:
    _TelnetSelector = selectors.SelectSelector


class Telnet:

    """Telnet interface class.

    An instance of this class represents a connection to a telnet
    server.  The instance is initially not connected; the open()
    method must be used to establish a connection.  Alternatively, the
    host name and optional port number can be passed to the
    constructor, too.

    Don't try to reopen an already connected instance.

    This class has many read_*() methods.  Note that some of them
    raise EOFError when the end of the connection is read, because
    they can return an empty string for other reasons.  See the
    individual doc strings.

    read_until(expected, [timeout])
        Read until the expected string has been seen, or a timeout is
        hit (default is no timeout); may block.

    read_all()
        Read all data until EOF; may block.

    read_some()
        Read at least one byte or EOF; may block.

    read_very_eager()
        Read all data available already queued or on the socket,
        without blocking.

    read_eager()
        Read either data already queued or some data available on the
        socket, without blocking.

    read_lazy()
        Read all data in the raw queue (processing it first), without
        doing any socket I/O.

    read_very_lazy()
        Reads all data in the cooked queue, without doing any socket
        I/O.

    read_sb_data()
        Reads available data between SB ... SE sequence. Don't block.

    set_option_negotiation_callback(callback)
        Each time a telnet option is read on the input flow, this callback
        (if set) is called with the following parameters :
        callback(telnet socket, command, option)
            option will be chr(0) when there is no option.

    """

    def __init__(self, host=None, port=0,
                 timeout=socket._GLOBAL_DEFAULT_TIMEOUT):
        """Constructor.

        When called without arguments, create an unconnected instance.
        With a hostname argument, it connects the instance; port number
        and timeout are optional.
        """
        self.host = host
        self.port = port
        self.timeout = timeout
        self.sock = None
        self.rawq = b''
        self.irawq = 0
        self.cookedq = b''
        self.eof = 0
        self.iacseq = b'' # Buffer for IAC sequence.
        self.sb = 0 # flag for SB and SE sequence.
        self.sbdataq = b''
        self.option_callback = None
        if host is not None:
            self.open(host, port, timeout)

    def open(self, host, port=0, timeout=socket._GLOBAL_DEFAULT_TIMEOUT):
        """Connect to a host.

        The optional second argument is the port number, which
        defaults to the standard telnet port (23).

        Don't try to reopen an already connected instance.
        """
        self.eof = 0
        if not port:
            port = TELNET_PORT
        self.host = host
        self.port = port
        self.timeout = timeout
        sys.audit("amxtelnet.Telnet.open", self, host, port)
        self.sock = socket.create_connection((host, port), timeout)

    def __del__(self):
        """Destructor -- close the connection."""
        self.close()

    def msg(self, msg, *args):
        debug(f"Telnet:{self.host}:{self.port} {msg} {args}")

    def close(self):
        """Close the connection."""
        sock = self.sock
        self.sock = None
        self.eof = True
        self.iacseq = b''
        self.sb = 0
        if sock:
            sock.close()

    def get_socket(self):
        """Return the socket object used internally."""
        return self.sock

    def fileno(self):
        """Return the fileno() of the socket object used internally."""
        return self.sock.fileno()

    def write(self, buffer):
        """Write a string to the socket, doubling any IAC characters.
        Logan: IAC doubling disabled

        Can block if the connection is blocked.  May raise
        OSError if the connection is closed.

        """
        # if IAC in buffer:     # logan revert = uncomment
        #     buffer = buffer.replace(IAC, IAC+IAC)     # logan revert = uncomment
        sys.audit("amxtelnet.Telnet.write", self, buffer)
        self.msg("send %r", buffer)
        self.sock.sendall(buffer)

    def read_until(self, match, timeout=None):
        """Read until a given string is encountered or until timeout.

        When no match is found, return whatever is available instead,
        possibly the empty string.  Raise EOFError if the connection
        is closed and no cooked data is available.

        """
        n = len(match)
        self.process_rawq()
        i = self.cookedq.find(match)
        if i >= 0:
            i = i+n
            buf = self.cookedq[:i]
            self.cookedq = self.cookedq[i:]
            return buf
        if timeout is not None:
            deadline = _time() + timeout
        with _TelnetSelector() as selector:
            selector.register(self, selectors.EVENT_READ)
            while not self.eof:
                if selector.select(timeout):
                    i = max(0, len(self.cookedq)-n)
                    self.fill_rawq()
                    self.process_rawq()
                    i = self.cookedq.find(match, i)
                    if i >= 0:
                        i = i+n
                        buf = self.cookedq[:i]
                        self.cookedq = self.cookedq[i:]
                        return buf
                if timeout is not None:
                    timeout = deadline - _time()
                    if timeout < 0:
                        break
        return self.read_very_lazy()

    def read_all(self):
        """Read all data until EOF; block until connection closed."""
        self.process_rawq()
        while not self.eof:
            self.fill_rawq()
            self.process_rawq()
        buf = self.cookedq
        self.cookedq = b''
        return buf

    def read_some(self):
        """Read at least one byte of cooked data unless EOF is hit.

        Return b'' if EOF is hit.  Block if no data is immediately
        available.

        """
        self.process_rawq()
        while not self.cookedq and not self.eof:
            self.fill_rawq()
            self.process_rawq()
        buf = self.cookedq
        self.cookedq = b''
        return buf

    def read_very_eager(self):
        """Read everything that's possible without blocking in I/O (eager).

        Raise EOFError if connection closed and no cooked data
        available.  Return b'' if no cooked data available otherwise.
        Don't block unless in the midst of an IAC sequence.

        """
        self.process_rawq()
        while not self.eof and self.sock_avail():
            self.fill_rawq()
            self.process_rawq()
        return self.read_very_lazy()

    def read_eager(self):
        """Read readily available data.

        Raise EOFError if connection closed and no cooked data
        available.  Return b'' if no cooked data available otherwise.
        Don't block unless in the midst of an IAC sequence.

        """
        self.process_rawq()
        while not self.cookedq and not self.eof and self.sock_avail():
            self.fill_rawq()
            self.process_rawq()
        return self.read_very_lazy()

    def read_lazy(self):
        """Process and return data that's already in the queues (lazy).

        Raise EOFError if connection closed and no data available.
        Return b'' if no cooked data available otherwise.  Don't block
        unless in the midst of an IAC sequence.

        """
        self.process_rawq()
        return self.read_very_lazy()

    def read_very_lazy(self):
        """Return any data available in the cooked queue (very lazy).

        Raise EOFError if connection closed and no data available.
        Return b'' if no cooked data available otherwise.  Don't block.

        """
        buf = self.cookedq
        self.cookedq = b''
        if not buf and self.eof and not self.rawq:
            raise EOFError('telnet connection closed')
        return buf

    def read_sb_data(self):
        """Return any data available in the SB ... SE queue.

        Return b'' if no SB ... SE available. Should only be called
        after seeing a SB or SE command. When a new SB command is
        found, old unread SB data will be discarded. Don't block.

        """
        buf = self.sbdataq
        self.sbdataq = b''
        return buf

    def set_option_negotiation_callback(self, callback):
        """Provide a callback function called after each receipt of a telnet option."""
        self.option_callback = callback

    def process_rawq(self):
        """Transfer from raw queue to cooked queue.

        Set self.eof when connection is closed.  Don't block unless in
        the midst of an IAC sequence.

        """
        buf = [b'', b'']
        try:
            while self.rawq:
                c = self.rawq_getchar()
                if not self.iacseq:
                    if c == theNULL:
                        continue
                    if c == b"\021":
                        continue
                    # if c != IAC:  # logan revert = uncomment
                    if c:   # logan revert = delete line
                        buf[self.sb] = buf[self.sb] + c
                        continue
                    else:
                        self.iacseq += c
                elif len(self.iacseq) == 1:
                    # 'IAC: IAC CMD [OPTION only for WILL/WONT/DO/DONT]'
                    if c in (DO, DONT, WILL, WONT):
                        self.iacseq += c
                        continue

                    self.iacseq = b''
                    if c == IAC:
                        buf[self.sb] = buf[self.sb] + c
                    else:
                        if c == SB: # SB ... SE start.
                            self.sb = 1
                            self.sbdataq = b''
                        elif c == SE:
                            self.sb = 0
                            self.sbdataq = self.sbdataq + buf[1]
                            buf[1] = b''
                        if self.option_callback:
                            # Callback is supposed to look into
                            # the sbdataq
                            self.option_callback(self.sock, c, NOOPT)
                        else:
                            # We can't offer automatic processing of
                            # suboptions. Alas, we should not get any
                            # unless we did a WILL/DO before.
                            self.msg('IAC %d not recognized' % ord(c))
                elif len(self.iacseq) == 2:
                    cmd = self.iacseq[1:2]
                    self.iacseq = b''
                    opt = c
                    if cmd in (DO, DONT):
                        self.msg('IAC %s %d',
                            cmd == DO and 'DO' or 'DONT', ord(opt))
                        if self.option_callback:
                            self.option_callback(self.sock, cmd, opt)
                        else:
                            self.sock.sendall(IAC + WONT + opt)
                    elif cmd in (WILL, WONT):
                        self.msg('IAC %s %d',
                            cmd == WILL and 'WILL' or 'WONT', ord(opt))
                        if self.option_callback:
                            self.option_callback(self.sock, cmd, opt)
                        else:
                            self.sock.sendall(IAC + DONT + opt)
        except EOFError: # raised by self.rawq_getchar()
            self.iacseq = b'' # Reset on EOF
            self.sb = 0
            pass
        self.cookedq = self.cookedq + buf[0]
        self.sbdataq = self.sbdataq + buf[1]

    def rawq_getchar(self):
        """Get next char from raw queue.

        Block if no data is immediately available.  Raise EOFError
        when connection is closed.

        """
        if not self.rawq:
            self.fill_rawq()
            if self.eof:
                raise EOFError
        c = self.rawq[self.irawq:self.irawq+1]
        self.irawq = self.irawq + 1
        if self.irawq >= len(self.rawq):
            self.rawq = b''
            self.irawq = 0
        return c

    def fill_rawq(self):
        """Fill raw queue from exactly one recv() system call.

        Block if no data is immediately available.  Set self.eof when
        connection is closed.

        """
        if self.irawq >= len(self.rawq):
            self.rawq = b''
            self.irawq = 0
        # The buffer size should be fairly small so as to avoid quadratic
        # behavior in process_rawq() above
        buf = self.sock.recv(50)
        self.msg("recv %r", buf)
        self.eof = (not buf)
        self.rawq = self.rawq + buf

    def sock_avail(self):
        """Test whether data is available on the socket."""
        with _TelnetSelector() as selector:
            selector.register(self, selectors.EVENT_READ)
            return bool(selector.select(0))

    def interact(self):
        """Interaction function, emulates a very dumb telnet client."""
        if sys.platform == "win32":
            self.mt_interact()
            return
        with _TelnetSelector() as selector:
            selector.register(self, selectors.EVENT_READ)
            selector.register(sys.stdin, selectors.EVENT_READ)

            while True:
                for key, events in selector.select():
                    if key.fileobj is self:
                        try:
                            text = self.read_eager()
                        except EOFError:
                            warning('*** Connection closed by remote host ***')
                            return
                        if text:
                            sys.stdout.write(text.decode('ascii'))
                            sys.stdout.flush()
                    elif key.fileobj is sys.stdin:
                        line = sys.stdin.readline().encode('ascii')
                        if not line:
                            return
                        self.write(line)

    def mt_interact(self):
        """Multithreaded version of interact()."""
        import _thread
        _thread.start_new_thread(self.listener, ())
        while 1:
            line = sys.stdin.readline()
            if not line:
                break
            self.write(line.encode('ascii'))

    def listener(self):
        """Helper for mt_interact() -- this executes in the other thread."""
        while 1:
            try:
                data = self.read_eager()
            except EOFError:
                warning('*** Connection closed by remote host ***')
                return
            if data:
                sys.stdout.write(data.decode('ascii'))
            else:
                sys.stdout.flush()

    def expect(self, list, timeout=None):
        """Read until one from a list of a regular expressions matches.

        The first argument is a list of regular expressions, either
        compiled (re.Pattern instances) or uncompiled (strings).
        The optional second argument is a timeout, in seconds; default
        is no timeout.

        Return a tuple of three items: the index in the list of the
        first regular expression that matches; the re.Match object
        returned; and the text read up till and including the match.

        If EOF is read and no text was read, raise EOFError.
        Otherwise, when nothing matches, return (-1, None, text) where
        text is the text received so far (may be the empty string if a
        timeout happened).

        If a regular expression ends with a greedy match (e.g. '.*')
        or if more than one expression can match the same input, the
        results are undeterministic, and may depend on the I/O timing.

        """
        re = None
        list = list[:]
        indices = range(len(list))
        for i in indices:
            if not hasattr(list[i], "search"):
                if not re: import re
                list[i] = re.compile(list[i])
        if timeout is not None:
            deadline = _time() + timeout
        with _TelnetSelector() as selector:
            selector.register(self, selectors.EVENT_READ)
            while not self.eof:
                self.process_rawq()
                for i in indices:
                    m = list[i].search(self.cookedq)
                    if m:
                        e = m.end()
                        text = self.cookedq[:e]
                        self.cookedq = self.cookedq[e:]
                        return (i, m, text)
                if timeout is not None:
                    ready = selector.select(timeout)
                    timeout = deadline - _time()
                    if not ready:
                        if timeout < 0:
                            break
                        else:
                            continue
                self.fill_rawq()
        text = self.read_very_lazy()
        if not text and self.eof:
            raise EOFError
        return (-1, None, text)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()


class AMXTelnet:
	def __init__(self) -> None:
		self.scanned_systems = []


	def set_systems(self, systems):
		self.systems = systems
		info(f"added {len(self.systems)} systems")


	def config(self, user_name, password, alt_username='administrator', alt_password='password', write_results=True, path='systems/hard coded/'):
		self.user_name = user_name
		self.password = password
		self.alt_username = alt_username
		self.alt_password = alt_password
		self.write_results = write_results
		self.path = path
		return


	def set_requests(self, *requests):
		self.requests = [request for request in requests]
		info(f"requests = {requests}")
		return


	def _write_to_file(self, master, telnet_text):
		from os import mkdir, path
		# write each telnet rx to individual .txt file
		if not path.exists(self.path):
			mkdir(self.path)
			info(f'amxtelnet.py created {self.path}')

		header = f"full_name={master['full_name']}\nmaster_ip={master['master_ip']}\nfailed_attemps={master['master_failed_attempts']}\nlogin_failure={master['master_login_failure']}\n"

		file_path = f"{self.path}{master['full_name']} telnet.txt"
		with open(file_path, 'w+') as f:
			info(f'amxtelnet.py created {file_path}')
			f.write(header + telnet_text)


	async def _telnet_master_login(self, tn, master):
		if not self.user_name: error('user_name was not provided')
		if not self.password: error('password was not provided')
		master['master_user'] = self.user_name
		master['master_password'] = self.password
		# create ['master_failed_attempts'] if it doesn't exist
		try:
			master['master_failed_attempts']
		except KeyError:
			master['master_failed_attempts'] = 0

		# attempt to login
		tn.write(f"{self.user_name}\r\n".encode())
		tn.read_until(b'\r\nPassword : ')
		tn.write(f"{self.password}\r\n".encode())
		login_result = tn.read_until(b'Welcome to ', timeout=2)

		# login successful, throw back to _telnet_scan_master() to send commands
		if 'Welcome to' in login_result.decode():
			master['master_login_failure'] = None
			info(f"{master['full_name']} login success")
			return master

		# login failed, throw back to _telnet_scan_master() to try the default login
		elif 'Invalid' in login_result.decode():
			master['master_failed_credentials'] = f"{master['master_user']} {master['master_password']}"
			master['master_login_failure'] = 'invalid login'
			master['master_failed_attempts'] += 1
			return master


	async def _telnet_scan_master(self, master):
		info(f"connecting to {master['full_name']}")

		# avoid key errors later on
		master['master_telnet_failure'] = None
		master['master_login_failure'] = None

		try:
			with Telnet(master['master_ip'], timeout=10) as tn:
				telnet_text = ""

				# keep attempting login until success, unknown login, or timeout
				tn.read_until(b'\r\nLogin : ')
				master = await self._telnet_master_login(tn, master)

				# check login results
				while True:
					# success
					if master['master_login_failure'] is None:
						tn = await self._poll_master(tn)
						if 'NX' in master['master_model']:
							# close on echo of last command sent
							telnet_text = tn.read_until(
								f'{self.requests[-1]}\r\n'.encode()).decode()
							tn.close()
						else:
							tn.write(b"exit\r\n")
							telnet_text = tn.read_all().decode('ascii')
						break

					# failure, try amx default
					elif master['master_user'] != self.alt_username:
						self.user_name = self.alt_username
						self.password = self.alt_password
						warning(f" trying {self.user_name} {master['full_name']}")
						master = await self._telnet_master_login(tn, master)
						# default login attempted, loop through again to see if it worked
						continue

					# default didn't work either, move on to the next system
					else:
						error(f"""Unable to login to {master['full_name']} {master['master_ip']}
								after {master['master_failed_attempts']} failed attempts""")
						tn.close()
						break
				
				if self.write_results: self._write_to_file(master, telnet_text)

		# NX masters throw this error when using 'exit'
		# instead of .close(), but NI needs 'exit'
		except ConnectionResetError:
			warning(f'amxtelnet.py: _telnet_scan_master() NX false connection error')

		except Exception as e:
			if master is not None:
				warning(f"{master['full_name']} {master['master_ip']} {e}")
			else: error(f"amxtelnet.py: _telnet_scan_master() no master: {master} {e}")

		self.scanned_systems.append(master)
		return


	async def _poll_master(self, tn):
		for request in self.requests:
			tn.write(f"{request}\r\n".encode())
			await asyncio.sleep(0)
		return tn


	async def _gather_connections(self, systems, simultaneous=65535):
		tasks = []
		skip_remainder = True
		master_count = len(systems)
		if master_count <= simultaneous: simultaneous = master_count
		else: skip_remainder = False
		master_chunks = int(master_count / simultaneous)
		master_remainder = master_count % simultaneous

		for i in range(master_chunks):
			tasks = []
			scan_start = (i * simultaneous)
			scan_end = (scan_start + simultaneous)
			for x in range(scan_start, scan_start + simultaneous):
				tasks.append(self._telnet_scan_master(systems[x]))
			await asyncio.gather(*tasks)

		# remainder
		if not skip_remainder:
			tasks = []
			scan_start = master_chunks * simultaneous
			scan_end = master_chunks * simultaneous + master_remainder
			for i in range(scan_start, scan_end):
				tasks.append(self._telnet_scan_master(systems[i]))
			await asyncio.gather(*tasks)
		return


	async def run(self):
		import time
		# scan time begins to increase when simultaneous is set to 50 or lower
		start = time.perf_counter()
		await(self._gather_connections(self.systems))
		elapsed = time.perf_counter() - start
		info(f"amxtelnet.py AMXTelnet() complete in {elapsed:0.2f} seconds")
		# 'RoomName telnet.txt' was created for every room
		return


class ParseAMXResponse:
	def __init__(self, input_path):
		if input_path:
			self.input_path = input_path
		else: self.input_path = 'telnet responses/'


	async def _parse_master_telnet(self, data_in, telnet_master):
		full_text = data_in.split('\n')

		master_line = '00000  ('
		device_line = '05001 '
		massio_line = '08001 '
		tp_line = '10001 '
		version_match = r' v(\d.\S+)'
		serial_match = r"Serial='?(\w+)"

		telnet_master['tp_generation'] = 'None'
		telnet_master['tp_model'] = 'None'
		telnet_master['tp_firmware'] = 'None'
		telnet_master['tp_serial'] = 'None'
		telnet_master['tp_ip'] = 'None'

		for i, line in enumerate(full_text):
			if master_line in line:
				telnet_master['master_firmware'] = re.search(
					version_match, line).group(1)
				telnet_master['master_serial'] = re.search(
					serial_match, full_text[i+1]).group(1)

			elif device_line in line:
				model_match = r'\)N([\w.-]+)'
				telnet_master['master_model'] = f"N{re.search(model_match, line).group(1)}"
				telnet_master['device_firmware'] = re.search(
					version_match, line).group(1)

			elif (massio_line in line) or (tp_line in line):
				tp_match = r'((08001|10001)  \(\d+\))([\w-]+)'
				tp_match_obj = re.search(tp_match, data_in)
				if tp_match_obj: telnet_master['tp_model'] = tp_match_obj.group(3)

				try:
					telnet_master['tp_firmware'] = re.search(
						version_match, line).group(1)
					telnet_master['tp_serial'] = re.search(
						serial_match, full_text[i+1]).group(1)
					tp_ip_match = r'Physical Address=IP (\d.+)'
					telnet_master['tp_ip'] = re.search(
						tp_ip_match, full_text[i+2]).group(1)
				except Exception as e:
					error(f"amxtelnet.py _parse_master_telnet({telnet_master['full_name']}) tp_firmware {e}")
					pass

		re_list = [
			r'(?<=#)(?P<system_number>\d+)',
			# r'(?<=\)N)(?P<master_model>[\w.-]+)',
			r'(?<=HostName    )(?P<master_hostname>[\w.-_]+)',
			r'(?<=IP Address  )(?P<master_ip>[\d.]+)',
			r'(?<=Subnet Mask )(?P<master_subnet>[\d.]+)',
			r'(?<=Gateway IP  )(?P<master_gateway>[\d.]+)',
			r'(?<=IPv4 Address  )(?P<master_ip>[\d.]+)',
			r'(?<=IPv4 Subnet Mask )(?P<master_subnet>[\d.]+)',
			r'(?<=IPv4 Gateway IP  )(?P<master_gateway>[\d.]+)',
			r'(?<=MAC Address )(?P<master_mac>[\w:]+)',
			r'(?<=1  Name is )(?P<program_name>[\w, .]+)',
			r'(?<=Rev )(?P<program_version>[\w, .]+)',
		]

		for item in re_list:
			telnet_master = await self._re_search(item, data_in, telnet_master)

		# Not reading logs, just seeing if they exist
		telnet_master['error_log'] = '.log' in data_in.lower()  # true/false
		telnet_master['camera_log'] = 'camera_log.txt' in data_in.lower()  # true/false

		return telnet_master


	async def _re_search(self, _re, data_in, telnet_master):
		if re.search(_re, data_in) is not None:
			telnet_master = {**telnet_master, **re.search(_re, data_in).groupdict()}
		return telnet_master


	async def run(self) -> list:
		from os import scandir
		telnet_info = []

		with scandir(self.input_path) as file_list:
			for file in file_list:
				telnet_master = {}
				telnet_master['full_name'] = file.name.split(' ')[0]
				with open(file, 'r') as f:
					file_text = f.read()
					telnet_master = await self._parse_master_telnet(file_text, telnet_master)
				telnet_info.append(telnet_master)
		return telnet_info
