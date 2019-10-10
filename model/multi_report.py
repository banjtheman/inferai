import fasttext
import os
import sys
import glob
import pprint
import sys
import json


# pretty printer
pp = pprint.PrettyPrinter(indent=4)
# load model
model = fasttext.load_model("infer_ai.bin")
# final report
high_level_report = {}


def gen_report_on_file(project, filepath):
    # Open source file
    output_path = "../output/" + project + "/"
    fo = open(filepath, "r")
    lines = fo.readlines()
    report_json = dict()

    index = 1
    # Run predicts on a file, line by line
    for line in lines:

        # print(line)
        if len(line.strip()) < 5:
            continue

        try:
            predictions = model.predict(line.strip(), k=-1, threshold=0.75)
            label = str(predictions[0][0].replace("__label__", ""))
            metadata = {}
            metadata["line"] = line.strip()
            metadata["line_number"] = index
            metadata["chance"] = predictions[1][0]

            if len(report_json) == 0:
                report_json[label] = {}
                report_json[label]["metadata"] = []
                report_json[label]["count"] = 0

            if label in report_json:
                report_json[label]["metadata"].append(metadata)
                report_json[label]["count"] += 1
            else:
                report_json[label] = {}
                report_json[label]["metadata"] = []
                report_json[label]["metadata"].append(metadata)
                report_json[label]["count"] = 1

        except Exception as e:
            # print(str(e))
            preidctions = []

        index = index + 1

    # close file
    fo.close()

    # Write to file
    output_file_path = output_path + filepath.replace("/", "__") + ".json"
    with open(output_file_path, "w") as outfile:
        json.dump(report_json, outfile)

    # print(str(report_json))

    # Create high level report
    high_level_report[project][filepath] = {}
    for label in report_json.keys():

        # Skip these labels for now, as ther are mostly noise?
        if label == "DEAD_STORE":
            continue
        if label == "NULL_DEREFERENCE":
            continue
        if label == "UNINITIALIZED_VALUE":
            continue

        high_level_report[project][filepath][label] = report_json[label]["count"]


def main():

    source_paths = []
    for arg in sys.argv[1:]:
        source_paths.append(arg)
        print("Adding project " + arg + " to InferAI run")

    if len(source_paths) == 0:
        print("No projects input")
        print("Usage: python multi_report.py project_path1 project_path2 ....")
        sys.exit(-1)

    print("InferAI")

    print("Making output directory")
    path = "output"
    try:
        os.mkdir(path)
    except OSError:
        print("Creation of the directory %s failed or it already exists..." % path)
    else:
        print("Successfully created the directory %s " % path)

    for project in source_paths:
        print("Running on project: " + project)
        high_level_report[project] = {}
        print("Making output directory")
        try:
            path = "output/" + project
            os.mkdir(path)
        except OSError:
            print("Creation of the directory %s failed or it already exists..." % path)
        else:
            print("Successfully created the directory %s " % path)
        # .glob('**/*.txt)
        os.chdir(project)
        # predict on all files
        for file in glob.glob("**/*.c", recursive=True):
            print("getting file... " + file)
            # gen_report(source_path+"/"+file)
            gen_report_on_file(project, file)
        os.chdir("../")
        pp.pprint(high_level_report)
        output_file_path = "output/high_level_report.json"
        # Write to file
        with open(output_file_path, "w") as outfile:
            json.dump(high_level_report, outfile)
    

    print("Done and Done, results in output folder")


if __name__ == "__main__":
    main()
