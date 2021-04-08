""" Pattern and template based chatbot dialog engines """
import logging
import os
from pathlib import Path
import yaml
from copy import deepcopy

from qary.constants import DATA_DIR
from qary.etl.nesting import lod_replace
from qary.etl.utils import squash_wikititle as normalize_text
# from qary.etl.dialog import TurnsPreparation

# FIXME: make this a config option and dont default to a test file
DEFAULT_QUIZ = os.path.join(DATA_DIR, 'writing/ogden-script.v2.dialog.yml')
DIALOG_TREE_END_STATE_NAMES = (None, False, 0, '', ''.encode(), '0', 'none', 'None')
DIALOG_TREE_END_BOT_STATEMENTS = (None, 'none', )

WELCOME_STATE_NAME = '__WELCOME__'
FINISH_STATE_NAME = '__FINISH__'
DEFAULT_STATE_NAME = '__default__'
DEFAULT_BOT_USERNAME = 'bot'
EXIT_STATE_NAME = None
EXIT_BOT_STATEMENTS = ['Session is already over! Type "quit" to exit or press "Enter" for a new session']
EXIT_STATE_TURN_DICT = {'state': EXIT_STATE_NAME, DEFAULT_BOT_USERNAME: EXIT_BOT_STATEMENTS}


log = logging.getLogger(__name__)


def load(datafile):
    """Load datafile (currently yml) and create a turns datastructure

    >>> datafile = os.path.join(DATA_DIR, 'yes_no/intern_quiz.yml')
    >>> load(datafile) # doctest: +ELLIPSIS
    [{'state': 'Welcome', 'Bot':...
    """
    datafile = Path(datafile)
    if not datafile.exists():
        log.error(f'Quiz bot data file {datafile} does not exist')
        turns = None
    elif datafile.suffix not in ['.yml', '.yaml']:
        log.error(f'Quiz bot currently only supports YAML datafiles with extensions yml or yaml')
        turns = None
    else:
        with open(datafile, 'r') as infile:
            turns = yaml.load(infile, Loader=yaml.SafeLoader)
    turns = lod_replace(turns, mapping={False: 'No', True: 'Yes'})
    return turns


def normalize_keys(self, turns_list_input=None):
    """ Lowercase the keys in each turn dict; convert the 'nlp' key to 'match_method' """
    for i, turn in enumerate(turns_list_input):
        if not turn:  # possibility of empty list values
            continue
        turn = {key.lower(): value for key, value in turn.items()}
        if 'nlp' in turn:
            turn['match_method'] = turn['nlp']
            del turn['nlp']
        self.turns_list_input[i] = turn
    return turns_list_input


def listify_bot_statements(turns_list):
    r""" Ensure that all bot statements are lists of strs (alternative bot statements)

    >>> listify_bot_statements([{'state': '1', 'bot': 'hello world'}])
    [{'state': '1', 'bot': ['hello world']}]
    >>> listify_bot_statements([{'state': '1', 'bot': [1, 2]}])
    [{'state': '1', 'bot': ['1', '2']}]
    >>> listify_bot_statements([{'state': '1', 'bot': b'hello bytes'}])
    [{'state': '1', 'bot': ['hello bytes']}]
    """
    listified_turns_list = []
    for i, turn in enumerate(turns_list):
        listified_turn = deepcopy(turn)
        if DEFAULT_BOT_USERNAME in listified_turn:
            if isinstance(turn['bot'], (str, bytes)):
                bot_statements = [turn['bot']]
            else:
                bot_statements = list(turn['bot'])
            listified_turn['bot'] = []
            for statement in bot_statements:
                if isinstance(statement, bytes):
                    try:
                        listified_turn['bot'].append(statement.decode('utf-8'))
                    except UnicodeDecodeError:
                        listified_turn['bot'].append(statement.decode('latin'))
                elif isinstance(statement, str):
                    listified_turn['bot'].append(statement)
                else:
                    log.warning(f'Coercing Bot Statement from type `{type(statement)}` to `str`.')
                    listified_turn['bot'].append(str(statement))
        listified_turns_list.append(listified_turn)
    return listified_turns_list


def normalize_state_names(turns_list_input):
    """ Lowercase state names everywhere they're used in the nested turn dicts """
    for turn in turns_list_input:
        state_orig = turn.get('state', '')
        state = state_orig.lower()
        # first normalize the state name
        if state != state_orig:
            log.warning(f'Normalized state name {state_orig} to {state}')
            turn['state'] = state
        # normalize the 'next' key if it exists
        if 'next' in turn:
            turn['next'] = turn['next'].lower()
        if 'next_condition' in turn:
            next_condition_new = (
                {}
            )  # create a new dictionary to avoid inplace mod of dict in loop
            for next_state, intent in turn['next_condition'].items():
                next_condition_new[next_state.lower()] = intent
            turn['next_condition'] = next_condition_new
        if 'match_method' in turn:
            match_method_new = (
                {}
            )  # create a new dictionary to avoid inplace mod of dict in loop
            for next_state, match_method in turn['match_method'].items():
                match_method_new[next_state.lower()] = match_method
            turn['match_method'] = match_method_new
    return turns_list_input

def compose_statement(statements):
    r""" Pick a sttement or combine multiple statements into one.

    Currently uses `'\n'.join(statements)`.
    Alternatively we could use the normalize_replies() method and
     probabilitistically/psychometrically chose an optimal one.

    >>> compose_statement(statements=['Hello', 'Trisolaris'])
    'Hello\nTrisolaris'
    """
    if not statements:
        return statements
    if isinstance(statements, str):
        return statements
    return '\n'.join(statements)


class TurnsPreparation:
    """ Prepare the turns datastructure to ensure each has a next state (outgoing graph edges)

    TODO: move all these to the dialog.py module as independent functions
    """

    DEFAULTS = {'match_method': 'exact'}

    def __init__(self, turns_list=None, use_nlp=False):
        """Raw turns that need to be cleaned up and prepared

        Args:
            use_nlp (bool):
            turns_list (List):

        Returns:
            Dict:
        """
        self.turns_list_input = turns_list
        self.use_nlp = use_nlp
        self.defaults = self.DEFAULTS

    def normalize_keys(self):
        """Normalize the keys of the turns dictionary as well as convert the 'nlp' key names to
        the more intuitive 'match_method'"""

        for i, turn in enumerate(self.turns_list_input):
            if not turn:  # possibility of empty list values
                continue
            turn = {key.lower(): value for key, value in turn.items()}
            if 'nlp' in turn:
                turn['match_method'] = turn['nlp']
                del turn['nlp']
            self.turns_list_input[i] = turn
        return

    def prepare_turns(self, turns_list_input=None):
        """Processes the turns to a form that allows for conditional transitions in the FSM. This
        will convert the player value in each turn from a list of dicts and strings to a pure
        dictionary, each being of the following form.
        { <intent string>: {
                'next_state': <next_state_for_that_intent>,
                'match_method': <nlp processing method for that intent>
                }
        }
        If the player repsone is empty, the key will be None."""
        if not turns_list_input:
            turns_list_input = self.turns_list_input
        self.turns_list_input = [
            turn for turn in turns_list_input if turn
        ]  # Remove empty values
        self.normalize_keys()
        self.normalize_state_names()
        self.turns_list_input = listify_bot_statements(self.turns_list_input)
        turns = {}  # convert to a dictionary with the keys being the states
        # TODO: keep track of state normalizations and if multiple states map to the same
        #  normalized state name.
        # state_normalizations = {} # keep track of state normalizations for error reporting
        self.parse_defaults()
        for i, turn_orig in enumerate(self.turns_list_input):
            # construct a new turn to avoid certain corner case errors in later processing
            turn = {}
            # Copy over any unknown keys as such for possible downstream processing
            keys_to_avoid = ['next_condition', 'next', 'state', 'match_method']
            for key, value in turn_orig.items():
                if key not in keys_to_avoid:
                    turn[key] = value
            # check if a next_condition key exists and if not create one
            next_condition = turn_orig['next_condition'] if 'next_condition' in turn_orig else {}
            next_default = self.evaluate_next_default_state(i, turn_orig)
            # now flip around the next state and the response that triggers the next state since
            # that is more useful; Also explode the multiple responses into separate keys
            next_condition_rev = self.process_next_conditions(next_condition, next_default)
            # now add nlp info for that particular intent
            next_condition_rev = self.add_match_methd_info(next_condition_rev, turn_orig)
            turn['next_condition'] = next_condition_rev
            state_name = turn_orig['state']
            turns[state_name] = turn
            if i == 0:
                # special key to indicate which is the welcome state since a dictionary does not
                # indicate which state was the first turn that was parsed
                turns[WELCOME_STATE_NAME] = state_name
            elif i == len(self.turns_list_input) - 1:
                turns[FINISH_STATE_NAME] = state_name
        self.turns_new = turns  # Add as a property for debugging ease
        return turns

    def evaluate_next_default_state(self, i, turn_orig):
        # assign the default next state to be the next sequential state if the 'next' key is
        # not present. Also unify all next_condition and next key into one dictionary
        if 'next' in turn_orig:
            state_orig = turn_orig['next']
            next_default = state_orig.lower()
            if next_default != state_orig:
                log.warning(f'Normalized "next" state name {state_orig} to {next_default}')
        else:
            if i < len(self.turns_list_input) - 1:
                state_orig = self.turns_list_input[i + 1]['state']
                next_default = state_orig.lower()
                if next_default != state_orig:
                    log.warning(f'Normalized "next" state name {state_orig} to {next_default}')
            else:
                next_default = EXIT_STATE_NAME
        return next_default

    def process_next_conditions(self, next_condition, next_default):
        next_condition_rev = {}  # keys and values reversed as well as unrolled
        for next_state, responses in next_condition.items():
            for response in responses:
                # response = normalize_text(response)
                next_state_lower = next_state.lower()
                if next_state != next_state_lower:
                    log.warning(f'Normalized "next" state name {next_state} to {next_state_lower}')
                next_condition_rev[response] = {'next_state': next_state_lower}
        next_condition_rev[''] = {'next_state': next_default}
        return next_condition_rev

    def parse_defaults(self):
        """Incorporates any defaults for the yml file into the turns data structure. The first
        list item should have the defaults if any. If found these will be incorporated into the
        data structure and that particular list item will be removed"""
        defaults = self.turns_list_input[0]
        if defaults['state'] == DEFAULT_STATE_NAME:
            if ('match_method' in defaults) and (DEFAULT_STATE_NAME in defaults['match_method']):
                self.defaults['match_method'] = defaults['match_method'].get(DEFAULT_STATE_NAME).upper()
            # now remove this item from the list
            del self.turns_list_input[0]
        return

    def add_match_methd_info(self, next_condition_rev, turn_orig):
        """Adds match_method information to the turn based on a priority scheme as follows:
        - If the 'match_method' dict within the turn has a key corresponding to the next_condition state
        name, the value of that key will be used for that next_condition
        - if the next_condition state name is missing in the 'match_method' dict, then if a __default__
        key exists inside the 'match_method' dict, then that key's value will be used
        - if there is no __default__ key either in the match_method dict, then the __default__ key's value
        from that yaml file's defaults will be used, if that is also missing, then the global
        default for the match_method key (defined as a class variable)will be used. This is not explicitly
        done in this method, but the defaults property of this class would already have been
        pre-populated with the global defaults
        """

        for intent, next_state_dict in next_condition_rev.items():
            next_state = next_state_dict['next_state']
            if not intent:  # fall through state does not need a match_method
                next_state_dict['match_method'] = None
            elif 'match_method' not in turn_orig:
                next_state_dict['match_method'] = self.defaults['match_method']
            elif next_state not in turn_orig['match_method']:
                if DEFAULT_STATE_NAME in turn_orig['match_method']:
                    next_state_dict['match_method'] = turn_orig['match_method'][DEFAULT_STATE_NAME]
                else:
                    next_state_dict['match_method'] = self.defaults['match_method']
            else:
                next_state_dict['match_method'] = turn_orig['match_method'][next_state]
            # these are really constants which is made clearer by the uppercase
            if intent:
                next_state_dict['match_method'] = next_state_dict['match_method'].upper()
        return next_condition_rev

    def normalize_state_names(self):
        """Normalizes state names in various fields of the turn list by lowercasing them to keey
        things consistent"""
        for turn in self.turns_list_input:
            state_orig = turn.get('state', '')
            state = state_orig.lower()
            # first normalize the state name
            if state != state_orig:
                log.warning(f'Normalized state name {state_orig} to {state}')
                turn['state'] = state
            # normalize the 'next' key if it exists
            if 'next' in turn:
                turn['next'] = turn['next'].lower()
            if 'next_condition' in turn:
                next_condition_new = {}  # create a new dictionary to avoid inplace mod of dict in loop
                for next_state, intent in turn['next_condition'].items():
                    next_condition_new[next_state.lower()] = intent
                turn['next_condition'] = next_condition_new
            if 'match_method' in turn:
                match_method_new = {}  # create a new dictionary to avoid inplace mod of dict in loop
                for next_state, match_method in turn['match_method'].items():
                    match_method_new[next_state.lower()] = match_method
                turn['match_method'] = match_method_new
        return self.turns_list_input


class Skill:
    r"""Skill for Quiz"""

    def __init__(self, datafile=DEFAULT_QUIZ, turns_list=None, use_nlp=False):
        """ If datafile is not given, the turns list of dicts can directly be passed to seed the data
        """
        self.datafile = datafile
        self.turns = {}
        self.use_nlp = use_nlp
        # if turns is passed, then you should not set the datafile
        if turns_list:
            self.turns_input = turns_list
        else:
            self.turns_input = load(datafile)
        if self.turns_input:
            # Do more complex operations using the helper '_TurnsPreparation' class
            turns_preparation = TurnsPreparation(turns_list=self.turns_input, use_nlp=self.use_nlp)
            self.turns = turns_preparation.prepare_turns()
        else:  # some sort of error
            log.error('An empty turns_list and/or datafile was passed to quiz.Skill.__init__()')
        self.state = ''  # State names must be strings
        self.current_turn = {}  # None or empty dict used to indicate start of quiz that bot says something first?
        return

    def get_nxt_cndn_match_mthd_dict(self, nxt_cndn):
        """Creates a dict with the match_method keyword being the key and a list of next_states which use
        that keyword as a value. This is needed because there is a priority in which the match_method
        keywords are handled

        Args:
            nxt_cndn (dict): dict with the intent being the key and the value being another dict
                with a key value pair for the next state and the 'match_method' for that intent

        Returns:
            object: A dictionary which looks like :
                    { match_method1: [intent1: next_state1], } where the list is a list of all the
                    next_conditions that use that match method

        """
        nxt_cndn_match_mthd_dict = {
            'EXACT': [],
            'LOWER': [],
            'CASE_SENSITIVE_KEYWORD': [],
            'KEYWORD': [],
            'NORMALIZE': [],
            None: [],
        }
        for intent, nxt_state_dict in nxt_cndn.items():
            match_method = nxt_state_dict['match_method']
            next_state = nxt_state_dict['next_state']
            nxt_cndn_match_mthd_dict[match_method].append((intent, next_state))
        return nxt_cndn_match_mthd_dict

    def check_for_match(self, statement, next_state_option, match_condition):
        intent = next_state_option[0]
        match_found = False
        if match_condition == 'EXACT':
            if statement == intent:
                self.state = next_state_option[1]
                match_found = True
        elif match_condition == 'LOWER':
            if statement.lower() == intent.lower():
                self.state = next_state_option[1]
                match_found = True
        elif match_condition == 'CASE_SENSITIVE_KEYWORD':
            if intent in statement:
                self.state = next_state_option[1]
                match_found = True
        elif match_condition == 'KEYWORD':
            if intent.lower() in statement.lower():
                self.state = next_state_option[1]
                match_found = True
        elif match_condition == 'NORMALIZE':
            if normalize_text(statement) == normalize_text(intent):
                self.state = next_state_option[1]
                match_found = True
        return match_found

    def reply(self, statement, context=None):
        r"""Except for the welcome state, all other states are mere recordings of the quiz responses
        """

        if statement in DIALOG_TREE_END_BOT_STATEMENTS:
            statement = None

        # First check to see if we are in the time before the welcome state
        if self.state in DIALOG_TREE_END_STATE_NAMES:
            # First figure out the welcome state name using a magical special WELCOME_STATE_NAME string
            # as the key. This will allow you to access the actual welcome turn
            self.state = self.turns[WELCOME_STATE_NAME]
            self.current_turn = self.turns[self.state]
            response = compose_statement(self.current_turn['bot'])
        else:
            nxt_cndn = self.current_turn['next_condition']
            nxt_cndn_match_mthd_dict = self.get_nxt_cndn_match_mthd_dict(nxt_cndn)
            # for match_method_keyword in ['EXACT', '']
            match_found = False
            for next_state_option in nxt_cndn_match_mthd_dict['EXACT']:
                match_found = self.check_for_match(statement, next_state_option, 'EXACT')
                if match_found:
                    break
            if not match_found:
                for next_state_option in nxt_cndn_match_mthd_dict['LOWER']:
                    match_found = self.check_for_match(statement, next_state_option, 'LOWER')
                    if match_found:
                        break
            if not match_found:
                for next_state_option in nxt_cndn_match_mthd_dict['CASE_SENSITIVE_KEYWORD']:
                    match_found = self.check_for_match(
                        statement, next_state_option, 'CASE_SENSITIVE_KEYWORD'
                    )
                    if match_found:
                        break
            if not match_found:
                for next_state_option in nxt_cndn_match_mthd_dict['KEYWORD']:
                    match_found = self.check_for_match(statement, next_state_option, 'KEYWORD')
                    if match_found:
                        break
            if not match_found:
                for next_state_option in nxt_cndn_match_mthd_dict['NORMALIZE']:
                    match_found = self.check_for_match(statement, next_state_option, 'NORMALIZE')
                    if match_found:
                        break
            if not match_found:
                self.state = nxt_cndn_match_mthd_dict[None][0][1]
            self.current_turn = self.turns.get(self.state, EXIT_STATE_TURN_DICT)
            response = compose_statement(self.current_turn.get(DEFAULT_BOT_USERNAME, EXIT_BOT_STATEMENTS))

        return [(1.0, response)]
