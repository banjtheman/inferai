import fasttext


#load model
model = fasttext.load_model("infer_ai.bin")

#Open source file
fo = open("sample.c", 'r')
lines = fo.readlines()



report_json = dict()

if "ok" in report_json:
    print("ok")
else:
    print("not ok")

index = 1
#Run predicts on a file, line by line
for line in lines:
     
    #print(line)
    if len(line.strip()) < 5:
        continue


    try:
        predictions = model.predict(line.strip(), k=-1, threshold=0.75)
        #print(predictions[0][0].replace("__label__",""))
        #print(predictions[1][0])
        #print(line.strip())
        #print(index)

        label = str(predictions[0][0].replace("__label__",""))
        metadata = {}
        metadata["line"] = line.strip()
        metadata["line_number"] = index
        metadata["chance"] = predictions[1][0]
        #print(label)
        #print(metadata)
        
        if len(report_json) == 0:
            report_json[label] = {}
            report_json[label]["metadata"] = []
            report_json[label]["count"] = 0

        if label in report_json:
            print("gotcha")
            print(label)
            report_json[label]["metadata"].append(metadata)
            report_json[label]["count"] += 1
        else:
            print("got one")
            print(label)
            report_json[label] = {}
            report_json[label]["metadata"] = []
            report_json[label]["metadata"].append(metadata)
            report_json[label]["count"] = 1

        #report_json[label] = metadata


    except Exception as  e:
        print(str(e))
        preidctions = []
    

    #print(" ######## "+str(predictions)+ "#######"+line)
    index = index + 1

fo.close()

#Generate report
print(str(report_json))


