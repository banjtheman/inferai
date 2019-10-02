import fasttext

#Train model
#model = fasttext.train_supervised(input="data_full.txt", epoch=50, wordNgrams=5, bucket=200000, dim=50, loss='ova')

model = fasttext.train_supervised(input="data.train", autotuneValidationFile='data.valid', loss='ova')


model.save_model("infer_ai.bin")

#TODO load model, will have to make option at some point
#model = fasttext.load_model("model/infer_ai.bin")

#Open source file
fo = open("sample.c", 'r')
lines = fo.readlines()

#Run predicts on a file, line by line
for line in lines:
     
    #print(line)
    try:
        predictions = model.predict(line.strip(), k=-1, threshold=0.5)
    except:
        predictions = []
    
    if len(line.strip()) < 3:
        predictions = []

    print(" ######## "+str(predictions)+ "#######"+line)

fo.close()

def print_results(N, p, r):
    print("N\t" + str(N))
    print("P@{}\t{:.3f}".format(1, p))
    print("R@{}\t{:.3f}".format(1, r))

print_results(*model.test('data.valid', k=-1))
