from abc import abstractmethod, ABC
from typing import Callable, Type
from pydantic import BaseModel

from scintillant.apimodels import SkillResponse
from scintillant.apimodels.types import SkillRequestType, SkillResponseType
from scintillant.outs import Dictionary

from loguru import logger


class Vault(BaseModel):

    @classmethod
    @abstractmethod
    def create(cls, data: SkillRequestType):
        pass


class ContextUpdater:
    states = {}  # state_name: state_func
    exit_phrases = ['exit', 'выход', 'хватит', 'остановись']
    vault = None

    def __init__(self, data: SkillRequestType,
                 dictionary: Type[Dictionary] = None,
                 vault: Type[Vault] = None):
        # Default parameters for find state and complete it
        self.data = data
        self.context = data.context
        self.response = SkillResponse(status='ok')

        if dictionary and data.user.client.type.lower() == 'voice':
            self.dictionary = dictionary.voice()
        elif dictionary:
            self.dictionary = dictionary.text()

        if vault and '__vault__' in self.context:
            self.vault = vault(**self.context['__vault__'])
        elif vault:
            self.vault = vault.create(data)
            self.context['__vault__'] = self.vault.dict()

    @property
    def next_state(self):
        if 'state' in self.context:
            return self.context['state']
        return None

    @next_state.setter
    def next_state(self, func: Callable):
        if func:
            self.context['state'] = func.__qualname__.split('.')[
                                        0] + '_' + func.__name__
        else:
            self.context.pop('state')

    def execute_state(self):
        # Termination of the skill if the user has asked for it
        if (self.data.update.in_text in self.exit_phrases
                or self.data.update.in_choice in self.exit_phrases):
            self.response.status = 'exit'
        # In case the user has just entered the skill,
        # we call the _initial_state_ function.
        elif 'state' not in self.context:
            state_response = self._initial_state_()
            if state_response and type(state_response) == str:
                self.response.out_text = state_response
        # In case the user already has a state.
        else:
            state = self.next_state.split('ContextUpdater_', maxsplit=1)[1]
            if state not in self.states:
                raise Exception(f"State {state} not registered!")
            else:
                state_response = self.states[state](self)
                if state_response and type(state_response) == str:
                    self.response.out_text = state_response
        # Save vault updated data
        if self.vault:
            self.context['__vault__'] = self.vault.dict()

    def execute_now(self, func: Callable or None) -> None:
        self.next_state = func
        self.execute_state()

    def redirect(self, redirect_to: str) -> None:
        self.response.status = 'redirect'
        self.response.redirect_to = redirect_to

    def get_response(self) -> SkillResponseType:
        logger.debug(
            "Executing state {} from User {} | Update data: {}".format(
                self.next_state,
                self.data.user,
                self.data
            ))
        self.execute_state()
        self.response.context = self.context
        logger.info("Getting response: {}".format(self.response))
        if not self.response.out_text and self.response.status not in ['redirect', 'exit']:
            logger.error(
                'Response out_text field is None inside non-action state!')
        return self.response

    def _initial_state_(self) -> None or str:
        """Execute when state is None"""
        self.response.out_text = "Добро пожаловать в фреймворк Scintillant." \
                                 "\n\n" \
                                 "Вы сгенерировали ваш первый шаблон навыка " \
                                 "и видите это сообщение потому, что не " \
                                 "изменили ответ для шага `_initial_state_`!"

    @classmethod
    def statefunc(cls, func):
        cls.states[
            func.__qualname__.split('.')[0] + '_' + func.__name__] = func

        def wrapper(*args, **kwargs):
            func(*args, **kwargs)

        wrapper.__name__ = func.__qualname__.split('.')[
                               0] + '_' + func.__name__

        return wrapper

    def setup_logs(self, folder, level='DEBUG', rotation='2 GB'):
        logger.add(folder + f'/{self.__class__.__name__}.log', level=level, rotation=rotation)
