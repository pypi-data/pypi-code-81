from octis.dataset.dataset import Dataset
from octis.preprocessing.preprocessing import Preprocessing

fold = r'C:\Users\terra\PycharmProjects\OCTIS\preprocessed_datasets\sample_dataset\\'
'''
d = Dataset()
d.load_custom_dataset_from_folder(fold)
print(d.get_vocabulary())
'''
'''
dataset = Dataset()
dataset.fetch_dataset("sample_dataset")
print(dataset.get_vocabulary())
print(dataset.get_partitioned_corpus())
print(len(dataset.get_partitioned_corpus()[0]))
print(dataset.get_corpus())
'''

# preprocessing





data_dir = r"C:\Users\terra\PycharmProjects\OCTIS\preprocessed_datasets\\"
p = Preprocessing(vocabulary=None, max_features=None, remove_punctuation=True,
                  lemmatize=False, stopword_list=None, min_chars=2, min_df=0.0, max_df=1.0, split=True, verbose=True)
dataset = p.preprocess_dataset(
    documents_path=data_dir+"M10\\raw_docs.txt",
)

dataset.save(data_dir + "/m10_NEW/")
dataset.load_custom_dataset_from_folder(data_dir + "/m10_NEW")
