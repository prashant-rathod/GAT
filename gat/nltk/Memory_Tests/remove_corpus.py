import filecmp
import os
import shutil
import zipfile
from gat.nltk.Memory_Tests.createExpected import create_expected
file_path = "/home/daniel/nltk_data/corpora/"
corpora_actual = [x for x in os.listdir(file_path) if x[-4:] != '.zip']
corpora_zips = [x[:-4] for x in os.listdir(file_path) if x[-4:] == '.zip']
f = open(str('gat/nltk/Memory_Tests/removed_corpora/results.txt'), 'w+')

for corpus in corpora_actual:
    print(corpus)

    shutil.rmtree(file_path + corpus)
    corpora_actual = [x for x in os.listdir(file_path) if x[-4:] != '.zip']

    difference = list(set(corpora_zips) - set(corpora_actual))
    print(difference)

    try:
        create_expected(corpus)

        result = filecmp.cmp('gat/nltk/Memory_Tests/removed_corpora/' + corpus + ".txt",'gat/nltk/Memory_Tests/removed_corpora/expected.txt')
    except Exception as e:
        result = e
    f.write(corpus + " " + str(result) + "\n")

    for file in difference:
        zip_ref = zipfile.ZipFile(file_path + file + ".zip", 'r')
        zip_ref.extractall(file_path)
        zip_ref.close()
f.close()
