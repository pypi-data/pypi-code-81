import json
import logging
import math
import re
import yaml


try:
    from collections.abc import Mapping
except ImportError:  # python <3.7
    from collections import Mapping


WELCOME_STATE_NAME = '__WELCOME__'
FINISH_STATE_NAME = '__FINISH__'
DEFAULT_STATE_NAME = '__default__'


def normalize_wikititle(title: str):
    r""" Case folding and whitespace normalization for wikipedia cache titles (keys)

    >>> normalize_wikititle("\n _Hello_\t\r\n_world_!  _\n")
    'hello world !'
    """
    return re.sub(r'[\s_]+', ' ', title).strip().lower()


log = logging.getLogger(__name__)


####################################################################
# duplicated in src/qary/etl/nesting.py

def default_normalizer(s, lower=True, underscores=True, strip=True):
    """ String normalizer: lower, strip whitespace, replace whitespace with underscores.

    >>> default_normalizer(' a a _')
    'a_a__'
    """
    if lower:
        s = str.lower(s)
    if strip:
        s = str.strip(s)
    if underscores:
        s = re.sub(r'[\s-]', '_', s)
    return s


def dict_key_normalize(unclean, normalizer=default_normalizer):
    """ Recursively lower, strip whitespace, replace whitespace with underscores.

    Inputs:
      unclean (dict): original dictionary
    Returns:
      clean (dict): deepcopy of clean with keys normalized

    >>> old = {' a a _': 1, '__b__': 2, 'c': {'  d  ': 3}}
    >>> dict_key_normalize(old)
    {'a_a__': 1, '__b__': 2, 'c': {'d': 3}}
    """
    clean = {}
    for k, v in unclean.items():
        if isinstance(unclean[k], Mapping):
            # TODO: test with dest `dict` replaced with `Mapping`
            clean[normalizer(k)] = dict_key_normalize(v, normalizer=normalizer)
        else:
            clean[normalizer(k)] = v
    return clean

# duplicated in src/qary/etl/nesting.py
####################################################################


class TurnsPreparation:
    """Helper class methods to prepare the turns datastructure like with next state info.

    Note: This class is merely a means to organize the various methods needed in a sane fashion
    """

    def __init__(self, turns_list=None, use_nlp=False):
        """Raw turns that need to be cleaned up and prepared

        Args:
            use_nlp (bool)
            turns_list (list)

        Returns:
            dialog_v2_datastructure: list of dicts
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
            turn = {default_normalizer(key): value for key, value in turn.items()}
            if 'nlp' in turn:
                turn['match_method'] = turn['nlp']
                del turn['nlp']
            self.turns_list_input[i] = turn
        return

    def prepare_turns(self):
        """Processes the turns to a form that allows for conditional transitions in the FSM. This
        will convert the player value in each turn from a list of dicts and strings to a pure
        dictionary, each being of the following form.
        { <intent string>: {
                'next_state': <next_state_for_that_intent>,
                'match_method': <nlp processing method for that intent>
                }
        }
        If the player repsone is empty, the key will be None."""

        self.turns_list_input = [
            turn for turn in self.turns_list_input if turn
        ]  # Remove empty values
        self.normalize_keys()
        self.normalize_state_names()
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
                next_default = None
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
        next_condition_rev[None] = {'next_state': next_default}
        return next_condition_rev

    def parse_defaults(self):
        """Incorporates any defaults for the yml file into the turns data structure. The first
        list item should have the defaults if any. If found these will be incorporated into the
        data structure and that particular list item will be removed"""
        defaults = self.turns_list_input[0]
        if defaults['state'] == DEFAULT_STATE_NAME:
            if ('match_method' in defaults) and ('__default__' in defaults['match_method']):
                self.defaults['match_method'] = defaults['match_method'].get('__default__').upper()
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
            if intent is None:  # fall through state does not need a match_method
                next_state_dict['match_method'] = None
            elif 'match_method' not in turn_orig:
                next_state_dict['match_method'] = self.defaults['match_method']
            elif next_state not in turn_orig['match_method']:
                if '__default__' in turn_orig['match_method']:
                    next_state_dict['match_method'] = turn_orig['match_method']['__default__']
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
        # turns_list = self.turns_list_input
        for turn in self.turns_list_input:
            state_orig = turn['state']
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
        return


def script_to_dialog(stream, state_name_prefix='turn_id_'):
    turn_list = yaml.load(stream, Loader=yaml.SafeLoader)
    dialog_tree = [{
        # optional defaults for this yml file
        'state': '__default__',
        'nlp': {'__default__': 'exact'},
        'version': 2.0,
    }]
    print(len(turn_list))
    digits = math.ceil(math.log10(len(turn_list)))
    name_template = f'{state_name_prefix}' + '{i:0' + f'{digits}' + 'd}'
    print(name_template)
    for i, turn in enumerate(turn_list):
        name = name_template.format(i=i)
        next_name = name_template.format(i=i + 1)
        dialog_state = {}
        statements = list(turn.items())
        dialog_state['state'] = name
        dialog_state['bot'] = statements[0][1]
        dialog_state['next_condition'] = {next_name: statements[1][1]}
        dialog_tree.append(dialog_state)
    return dialog_tree


if __name__ == '__main__':
    import sys
    serializer = json.dumps
    if len(sys.argv) > 1:
        if sys.argv[1] in ('--yaml', '-y'):
            serializer = yaml.dump
        stream = open(sys.argv[1])
    else:
        stream = sys.stdin
    turn_list = script_to_dialog(stream)
    # yaml_text = stream.read()
    sys.stdout.write(serializer(turn_list))
