import random
from json_database import JsonStorage
from enum import Enum


class SequenceScoringStrategy(str, Enum):
    MAX = "max"
    MIN = "min"
    MULTIPLY = "multiply"
    AVERAGE = "average"
    SUM = "sum"
    PROB_AVERAGE = "prob_average"
    PROB_MAX = "prob_max"
    PROB_MIN = "prob_min"
    PROB_SUM = "prob_sum"
    PROB_MULTIPLY = "prob_multiply"


class MarkovJson:
    def __init__(self, order=1, reverse=False,
                 strategy=SequenceScoringStrategy.PROB_MULTIPLY):
        self.START_OF_SEQ = "[/START]"
        self.END_OF_SEQ = "[/END]"
        self.NULL_SEQ = "[/NULL]"
        self.WILDCARD_SEQ = "[/]"
        self.reverse_modelling = reverse
        if not reverse:
            self.START_OF_SEQ = "[/START]"
            self.END_OF_SEQ = "[/END]"
        else:
            self.START_OF_SEQ = "[/END]"
            self.END_OF_SEQ = "[/START]"
        self.order = order
        self.records = {}
        self.strategy = strategy
        self._current_state = [self.START_OF_SEQ] * self.order

    # tokenization
    @property
    def tokens(self):
        toks = []
        for state in self.records:
            toks += list(state)
        return list(set(toks))

    def tokenize(self, text, wildcards=False):
        sequence = text.split(" ")
        if wildcards:
            sequence = self.replace_wildcards(sequence)
        if self.reverse_modelling:
            sequence.reverse()
        return sequence

    def replace_wildcards(self, sequence):
        # replace unknown tokens with wildcard
        prev_token = self.START_OF_SEQ
        for idx, s in enumerate(sequence):
            if s not in self.tokens:
                if prev_token == self.WILDCARD_SEQ:
                    sequence[idx] = None
                    continue
                else:
                    sequence[idx] = self.WILDCARD_SEQ
            prev_token = sequence[idx]
        sequence = [s for s in sequence if s is not None]
        return sequence

    # "training"
    def add_string(self, text):
        tokens = self.tokenize(text)
        self.add_tokens(tokens)

    def add_tokens(self, tokens):
        tokens = [self.START_OF_SEQ] * self.order + tokens + [self.END_OF_SEQ]

        for i in range(len(tokens) - self.order):
            current_state = tuple(tokens[i:i + self.order])
            next_state = tokens[i + self.order]
            self.add_state(current_state, next_state)

    def add_state(self, current_state, next_state):
        if current_state not in self.records:
            self.records[current_state] = {}

        if next_state not in self.records[current_state]:
            self.records[current_state][next_state] = 0

        self.records[current_state][next_state] += 1

    # sequence handling
    def get_state(self, initial_state=None, pad=True):
        sequence = self.state2sequence(initial_state, pad=pad)
        return tuple(sequence[-self.order:])

    def state2sequence(self, initial_state, pad=False, wildcards=False):
        if initial_state is None:
            sequence = [self.START_OF_SEQ] * self.order
        elif isinstance(initial_state, str):
            sequence = self.tokenize(initial_state, wildcards=wildcards)
        else:
            sequence = initial_state[:]

        if pad or len(sequence) < self.order:
            sequence = [self.START_OF_SEQ] * self.order + sequence
        sequence = [s for s in sequence if s]  # filter empty strings and such
        return sequence

    def sequence2states(self, sequence, wildcards=False):
        if isinstance(sequence, str):
            sequence = self.state2sequence(sequence, wildcards=wildcards)
        # convert a list of tokens into tuples of states
        # that can be looked up in self.records
        states = []
        for i in range(len(sequence)):
            state = tuple(sequence[i:self.order + i])
            if len(state) < self.order:
                break
            states.append(state)
        return states

    def get_transition_weights(self, sequence, wildcards=False):
        states = self.sequence2states(sequence, wildcards=wildcards)
        weights = []  # raw integer count
        avg_weights = []  # probs 0 to 1 for each transition
        for idx, state in enumerate(states):

            next_state = states[idx + 1] if idx < len(states) - 1 else None
            if not next_state:
                continue
            jump = next_state[-1]
            # transition does not exist in the model
            if state not in self.records or not self.records[state].get(jump):
                w = 0
                t = 1
            else:
                w = self.records[state][jump]
                t = sum(self.records[state][s] for s in self.records[state])
            weights.append(w)
            avg_weights.append(w / t)
        return weights, avg_weights

    def get_sequence_prob(self, sequence,
                          strategy=SequenceScoringStrategy.PROB_MULTIPLY,
                          wildcards=False):
        weights, avg_weights = self.get_transition_weights(sequence,
                                                           wildcards=wildcards)
        if not weights:  # sequence is not possible
            return 0

        if strategy == SequenceScoringStrategy.AVERAGE:
            return sum(weights) / len(weights)

        if strategy == SequenceScoringStrategy.PROB_AVERAGE:
            return sum(avg_weights) / len(avg_weights)

        if strategy == SequenceScoringStrategy.MAX:
            return max(weights)

        if strategy == SequenceScoringStrategy.PROB_MAX:
            return max(avg_weights)

        if strategy == SequenceScoringStrategy.MIN:
            return min(weights)

        if strategy == SequenceScoringStrategy.PROB_MIN:
            return min(avg_weights)

        if strategy == SequenceScoringStrategy.SUM:
            return sum(weights)

        if strategy == SequenceScoringStrategy.PROB_SUM:
            return sum(avg_weights)

        if strategy == SequenceScoringStrategy.MULTIPLY:
            score = 1
            for c in weights:
                score = score * c
            return score

        if strategy == SequenceScoringStrategy.PROB_MULTIPLY:
            score = 1
            for c in avg_weights:
                score = score * c
            return score

    def iterate_sequences(self, initial_state=None, max_len=10, pad=False,
                          strategy=None, max_depth=25, thresh=0.01):
        # TODO max_loops, how many times can end up in same state before
        #  path starts being ignored
        strategy = strategy or self.strategy
        current_state = self.get_state(initial_state, pad)
        sequence = self.state2sequence(initial_state, pad)

        if current_state not in self.records:
            return

        for possible_next, val in self.records[current_state].items():

            max_depth -= 1
            if max_depth <= 0:
                return

            seq = sequence + [possible_next]

            if len(seq) >= max_len + self.order:
                # sequence is too big
                # accounts for some infinite loops that can happen
                # without max_len, like autocorrect loops on old phones
                return

            # found a full path!
            if possible_next == self.END_OF_SEQ:
                score = self.get_sequence_prob(seq, strategy)
                if score >= thresh:
                    yield seq, score

            # check all sequences starting from the new sequence
            else:
                for seq2, conf2 in self.iterate_sequences(
                        seq, max_len=max_len, strategy=strategy,
                        thresh=thresh, max_depth=max_depth):
                    yield seq2, conf2

    def __iter__(self):
        for p in self.iterate_sequences(self._current_state):
            yield p

    # sampling
    def sample(self, current_state=None):
        if current_state is None:
            current_state = tuple([self.START_OF_SEQ] * self.order)
        elif isinstance(current_state, str):
            sequence = [self.START_OF_SEQ] * self.order + \
                       self.tokenize(current_state)
            current_state = tuple(sequence[-self.order:])

        possible_next = self.records[current_state]
        n = sum(possible_next.values())

        m = random.randint(0, n)
        count = 0
        for k, v in possible_next.items():
            count += v
            if m <= count:
                return k

    def generate_sequence(self, max_len=100, initial_state=None, pad=False):
        sequence = self.state2sequence(initial_state, pad=pad)
        for i in range(max_len):
            current_state = tuple(sequence[-self.order:])
            next_token = self.sample(current_state)
            if next_token == self.NULL_SEQ:
                continue
            sequence.append(next_token)
            if next_token == self.END_OF_SEQ:
                return sequence
        return sequence

    # persistence
    def save(self, filename):
        """
        Saves Markov chain to filename
        :param filename: string - where to save chain
        :return: None
        """
        with JsonStorage(filename) as db:
            db["order"] = self.order
            db["START_OF_SEQ"] = self.START_OF_SEQ
            db["END_OF_SEQ"] = self.END_OF_SEQ
            db["reverse_modelling"] = self.reverse_modelling
            # convert tuple keys to strings
            db["records"] = {str(k): v for k, v in self.records.items()}

    def load(self, filename):
        """
        Saves Markov chain to filename
        :param filename: string - where to save chain
        :return: None
        """
        with JsonStorage(filename) as db:
            if self._current_state == [self.START_OF_SEQ] * self.order:
                self._current_state = [db["START_OF_SEQ"]] * db["order"]
            self.order = db["order"]
            self.START_OF_SEQ = db["START_OF_SEQ"]
            self.END_OF_SEQ = db["END_OF_SEQ"]
            self.reverse_modelling = db.get("reverse_modelling") or False
            # convert str keys back to tuples
            self.records = {
                tuple(k.replace("',)", "')")[2:-2].split("', '")): v
                for k, v in db["records"].items()}
        return self

    # metrics
    def calc_approximate_removal_score(self, state, sequences=None,
                                       required_states=None,
                                       blacklisted_states=None, max_seqs=100,
                                       *args, **kwargs):
        if state == self.WILDCARD_SEQ:
            return 0
        required_states = required_states or [self.END_OF_SEQ]
        blacklisted_states = blacklisted_states or [self.NULL_SEQ]

        # sample sequences from the model
        if not sequences:
            sequences = []

            # sample sequences containing the token
            for p in self.iterate_sequences(
                    thresh=0.01,
                    strategy=SequenceScoringStrategy.PROB_MULTIPLY,
                    initial_state=state, *args, **kwargs):
                sequences.append(p)
                if len(sequences) >= max_seqs / 2:
                    break

            # sample sequences randomly
            for p in self.iterate_sequences(
                    thresh=0.01,
                    strategy=SequenceScoringStrategy.PROB_MULTIPLY,
                    *args, **kwargs):
                sequences.append(p)
                if len(sequences) >= max_seqs:
                    break
        # filter any path that doesn't contain all required states
        if required_states:
            sequences = [p for p in sequences
                         if all([t in p[0] for t in required_states])]

        # filter any path that contains any forbidden state
        if blacklisted_states:
            sequences = [p for p in sequences
                         if not any([t in p[0] for t in blacklisted_states])]

        with_state = [p for p in sequences if state in p[0]]
        no_state = [p for p in sequences if state not in p[0]]

        if len(sequences) == 0:
            return 0  # no paths found

        # normalize scores
        max_p = max(p[1] for p in sequences)
        all_p = sum(p[1] / max_p for p in sequences)
        # sum up to 1
        no_p = sum(p[1] / max_p for p in no_state) / all_p
        yes_p = sum(p[1] / max_p for p in with_state) / all_p
        if yes_p == 0:
            return 0
        return 1 - no_p / all_p
