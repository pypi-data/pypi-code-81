MESSAGE = """
import flokilum.arch as floki

### session info
floki.info()

### google drive
gdrive = floki.gdrive()

### utils: np, einops, mpl, sns
np = floki.numpy()
mpl, plt, sns = floki.matplotlib()

%matplotlib inline
plt.style.use("seaborn")
from einops import rearrange

### spacy
spacy = floki.spacy()

### spacy english
spacy_ensm = floki.spacy_ensm()
spacy_enmd = floki.spacy_enmd()
spacy_enlg = floki.spacy_enlg()
spacy_entr = floki.spacy_entr()

### spacy german
spacy_desm = floki.spacy_desm()

### pytorch
torch, device = floki.torch()
torchtext = floki.torchtext()
torchvision = floki.torchvision()

### tensorboard
tensorboard = floki.tensorboard()
%load_ext tensorboard
"""

def help():

    print(MESSAGE)
