import json
import os

#TODO Constants, should make them inputs at some point....
project_location = "data/code_and_static_analyzer/data"
output_file = open("output/data.txt", 'a')
fo = open("data/code_and_static_analyzer/test.txt", 'r')

projects = fo.readlines()

total_projects = len(projects)
for project in projects:

    proj = project.strip()
    print(proj)
    curr_path = project_location+"/"+proj
    try:
        infer_path = curr_path+"/derivatives/infer-out"
        source_path = curr_path+"/source"
        source_folder = next(os.walk(source_path))[1][0]
        source_path = source_path +"/"+source_folder
    except:
        print("ERROR on "+proj)
        continue

    #open report.json
    report_file = infer_path+"/report.json"
    try:
        with open(report_file) as json_file:
            data = json.load(json_file)
            #print(data)
            for bug in data:
                #we want to skip DEAD_STORE AND UNINITIALIZED_VALUE for now
                label = bug["bug_type"]
                bug_file = bug["file"]
                bug_line = bug["line"]

                if label == "DEAD_STORE":
                    continue

                if label == "UNINITIALIZED_VALUE":
                    continue                

                #print(label)
                #print(bug_file)
                #print(bug_line)

                #get line from source code           
                try:
                    soucre_file = open(source_path+"/"+bug_file, 'r')
                    lines=soucre_file.readlines()
                except:
                    print("ERROR on "+proj)
                    soucre_file.close()
                    continue
                error_line = lines[bug_line-1].strip()
                #print(error_line)

                #now write the label in fasttext format
                #__label__MEMORY_LEAK logfile = strdup(optarg);

                fasttext_formated_line = "__label__"+label+" "+ error_line
                print(fasttext_formated_line)
                #write to file
                output_file.write(fasttext_formated_line+"\n")
                soucre_file.close()

    except:
        print("ERROR on "+proj)
        continue



print("Done and done")
fo.close()