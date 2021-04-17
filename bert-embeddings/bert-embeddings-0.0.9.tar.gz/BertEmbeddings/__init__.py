try:
    import torch
    from torch import nn
except Exception as e:
    print(e)
    print()
    print('You\'ll probably need to install Torch inorder to use this library.\nUse: `pip install torch==1.5.0 -f https://download.pytorch.org/whl/torch_stable.html`')
    quit()

import transformers
from transformers import BertModel, BertTokenizer

from typing import Optional, List, Dict

class BertEmbeddings:

    def __init__(self, model_name:str = 'prajjwal1/bert-tiny'):
        '''
        This class instantiates a model and tokenizer based on model_name
        We can then use that model to create word embeddings

        Args
        - model_name
            The name of the model we want to run the contexts and questions on
            We want to speed over performance since this isn't really crucial but still necessary
        '''

        # Load model and tokenizer
        try:
            self.model = BertModel.from_pretrained(
                model_name,
                output_hidden_states = True
            )
            self.tokenizer = BertTokenizer.from_pretrained(model_name)
        except:
            model_name = 'prajjwal1/bert-tiny'
            self.model = BertModel.from_pretrained(
                model_name,
                output_hidden_states = True
            )
            self.tokenizer = BertTokenizer.from_pretrained(model_name)

    def __call__(self, inputs:List[str]) -> List[Dict[str, list]]:
        '''
        '''

        # Encode into a dictionary readable to the model
        encoded = self.tokenizer.batch_encode_plus(
            inputs, None,
            padding = True,
            max_length = 512,
            return_tensors = 'pt'
        )

        # Run the actual model
        with torch.no_grad():
            model_outputs = self.model(**encoded)

            # Process the hidden states so that we get actual embeddings
            hidden_states = model_outputs[2]
            hidden_states = torch.stack(hidden_states, dim=0)
            hidden_states = hidden_states.permute(1,2,0,3)

        # Turn into byte-pair tokens
        # E.g ["hello", "how", "##'re", "you"]
        tokenized_inputs = [self.tokenizer.tokenize(i) for i in inputs]

        # Generate a list of sentences (a list of word tokens)
        # list[list[str]]
        inputs_sentences = []
        for _input in tokenized_inputs:
            _input_sentence_tokens = []
            current_sentence = []
            for token in _input:
                if token == '.':
                    _input_sentence_tokens.append(current_sentence)
                    current_sentence = []
                else:
                    current_sentence.append(token)
            inputs_sentences.append(_input_sentence_tokens)
        
        # Permute the data
        inputs_ = []
        for i in range(len(inputs)):
            i_tokens = tokenized_inputs[i]
            i_sentence_tokens = inputs_sentences[i]
            print(i_sentence_tokens)
            i_hidden_states = hidden_states[i]
            inputs_.append({
                'tokens': i_tokens,
                'sentence_tokens': i_sentence_tokens,
                'hidden_states': i_hidden_states,
                'embeddings_map': self.create_embeddings(i_hidden_states, i_tokens)
            })

        return inputs_

    def create_embeddings(self, hidden_states:torch.Tensor, tokens:List[str]) -> Dict[str, torch.Tensor]:
        '''
        Purpose is to take the hiddenstates and permute the into 
        embeddings we can use to find similarity between words

        Args
        - hidden_states (torch.Tensor)
            The model outputs generated in the __call__ function
        - tokens (list(str))
            Each word token

        Returns
        A dictionary of each word token with the correlating word embedding
        The word token also includes the word token's index so that contextual embeddings are conserved
        '''

        # Get each embedding for each token in hidden_states
        # hidden_states.size() = [(tokens), (layers), (hidden size)]
        embeddings = {}
        idx = 0
        for token_str, hidden_state in zip(tokens, hidden_states):
            # vec.size() = [(layers * hidden size)]
            vec = torch.cat(
                (hidden_state[-3], hidden_state[-2], hidden_state[-1]), 
                dim=0
            )
            embeddings[f'{token_str}_{idx}'] = vec
            idx += 1
        return embeddings
