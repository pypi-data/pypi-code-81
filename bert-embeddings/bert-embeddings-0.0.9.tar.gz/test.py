import BertEmbeddings as main

context = 'Denmark is a Nordic country in Northern Europe. Denmark proper, which is the southernmost of the Scandinavian countries, consists of a peninsula, Jutland, and an archipelago of 443 named islands, with the largest being Zealand, Funen and the North Jutlandic Island.'
question = 'what is denmark'

bert_embeddings = main.BertEmbeddings()
bert_embeddings_output = bert_embeddings([context]*2)