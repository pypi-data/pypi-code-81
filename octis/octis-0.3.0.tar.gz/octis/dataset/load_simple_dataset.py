from octis.dataset.dataset import  Dataset
fold = r'C:\Users\terra\PycharmProjects\OCTIS\preprocessed_datasets\sample_dataset\\'
'''
d = Dataset()
d.load_custom_dataset_from_folder(fold)
print(d.get_vocabulary())
'''

dataset = Dataset()
dataset.fetch_dataset("sample_dataset")
print(dataset.get_vocabulary())
print(dataset.get_partitioned_corpus())
print(len(dataset.get_partitioned_corpus()[0]))
print(dataset.get_corpus())
