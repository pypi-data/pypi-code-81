from kolibri.core.component import Component
from kolibri.preprocess.text.cleaning.cleaning_scripts import fix_formating
from kdmt.dict import update
from kdmt.text import clean_text
from kolibri.preprocess.text.cleaning.email2text import EmailMessage

class EmailCleaner(Component):
    name = "email_cleaner"

    provides = ["text"]
    hyperparameters= {
        "fixed": {
            "input-fromat": "text", #or "eml"
            "fix-formating": True,
            "clean-text": True,
            "fragments": "all" #"first", "last", "all"

        },

        "tunable": {
        }
    }

    def __init__(self, config={}):
        self.hyperparameters=update(self.hyperparameters, Component.hyperparameters)
        super().__init__(config)
        self.email_cleaner=EmailMessage()
        self.override_default_parameters(config)
    def transform(self, X):
        return [self.clean(x) for x in X]

    def clean(self, text):
        if self.get_prameter("clean-text"):
            text=clean_text(text)

        if self.get_prameter("fix-formating"):
            text = fix_formating(text)
        parsed= self.email_cleaner.read(text)
        if parsed.title:
            text=parsed.title+"\n"
        if self.get_prameter("fragments")=="first":
            if len(parsed.fragments)>0:
                text+=parsed.fragments[0].title+ '\n' + parsed.fragments[0].body
        if self.get_prameter("fragments")=="last":
            if len(parsed.fragments)>0:
                text+=parsed.fragments[-1].title+ '\n' + parsed.fragments[-1].body
        else:
            text+= '\n'.join([fragment.title + '\n' + fragment.body for fragment in parsed.fragments])
        return text




from kolibri.registry import ModulesRegistry
ModulesRegistry.add_module(EmailCleaner.name, EmailCleaner)
