import fasttext
from datetime import datetime


#Train model
model = fasttext.train_supervised(input="data.train", epoch=50, wordNgrams=5, bucket=200000, dim=50, loss='ova')
#model = fasttext.train_supervised(input="data.train", autotuneValidationFile='data.valid', loss='ova')

#evaluate 
def print_results(N, p, r):
    print("N\t" + str(N))
    print("P@{}\t{:.3f}".format(1, p))
    print("R@{}\t{:.3f}".format(1, r))

print_results(*model.test('data.valid', k=-1))

#save
now = str(datetime.now())
model.save_model(now+"infer_ai.bin")