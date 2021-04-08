import os
import pymacaroons
import random
import string
import logging
import json
import time

log = logging.getLogger(__name__)

IDENT_ALPHABET = string.digits + string.ascii_letters + string.punctuation

_key_cache = None

rand = random.SystemRandom()


def _auth_dir():
    d = os.path.join(__opts__['pki_dir'], 'spiro_auth')
    if not os.path.exists(d):
        os.makedirs(d)
    return d


def _getkey():
    global _key_cache
    if _key_cache is None:
        keyfile = os.path.join(_auth_dir(), 'macaroon-key')
        if os.path.exists(keyfile):
            with open(keyfile, 'rt') as kf:
                _key_cache = kf.read()
        else:
            _key_cache = ''.join(rand.choice(IDENT_ALPHABET) for _ in range(64))
            with open(keyfile, 'wt') as kf:
                kf.write(_key_cache)
    return _key_cache


def _genident():
    return ''.join(
        rand.choice(IDENT_ALPHABET)
        for _ in range(20)
    )


def _mkpredicate(**preds):
    return json.dumps(preds)


def _parsepredicate(txt):
    for name, arg in json.loads(txt).items():
        yield name, arg


def _check_predicates(pred, project=None, now=None):
    if now is None:
        now = time.time()
    log.debug("Check predicate (proj=%r): %r", project, pred)

    def _check_single_pred(kind, arg):
        if kind == 'not_before':
            return now > arg
        elif kind == 'not_after':
            return now < arg
        elif kind == 'project_allow':
            return project in arg or project is None
        elif kind == 'project_deny':
            return project not in arg or project is None
        else:
            log.error("Unknown predicate: %r %r", kind, arg)
            return False

    return all(
        _check_single_pred(kind, arg)
        for kind, arg in _parsepredicate(pred)
    )


def generate_token(projects=None, lifespan=None, now=None):
    m = pymacaroons.Macaroon(
        identifier=_genident(),
        key=_getkey(),
    )

    if now is None:
        now = time.time()

    caveat = {
        'not_before': now,
    }

    if lifespan is not None:
        caveat['not_after'] = now + lifespan
    if projects is not None:
        caveat['project_allow'] = projects

    m.add_first_party_caveat(_mkpredicate(**caveat))

    return m.serialize()


def check_token(token, project=None):
    """
    Checks if the given token is valid for the given project. If not project is
    given, only check that the token is valid.
    """
    try:
        m = pymacaroons.Macaroon.deserialize(token)
    except (TypeError, ValueError):  # Raised by b64decode()
        log.info("Invalid token (Invalid base64)")
        return False
    except pymacaroons.exceptions.MacaroonDeserializationException:
        log.info("Invalid token (deserialization)")
        return False

    v = pymacaroons.Verifier()
    v.satisfy_general(lambda p: _check_predicates(p, project))

    # TODO: Check m.identifier against {white,black}list

    try:
        isok = v.verify(m, _getkey())
    except pymacaroons.exceptions.MacaroonVerificationFailedException:
        log.info("Verification problem")
        # XXX: Do we want to return something more useful?
        return False
    else:
        return isok


def inspect_token(token):
    try:
        m = pymacaroons.Macaroon.deserialize(token)
    except pymacaroons.exceptions.MacaroonDeserializeException:
        return "(invalid)"

    return m.inspect()


def revoke_token(token):
    log.warning("TODO: Implement revoke_token")
