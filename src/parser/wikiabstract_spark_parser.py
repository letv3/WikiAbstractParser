import re, csv, datetime, glob, os


DEFAULT_DIR = "../../data"
DOCUMENT_DIR = "/document_base"
PARSED_CSV_DIR = "/parsed_abstracts"
DOCUMENT_BASE_PATH = DEFAULT_DIR + DOCUMENT_DIR + PARSED_CSV_DIR

def get_csv_filenames(file_dir):
    all_files = glob.glob(f"{file_dir}/*.csv*")
    csv_files = []
    for file_name in all_files:
        if re.match(r"(.*)(?=(\.csv))", file_name):
            csv_files.append(file_name)
        else:
            continue
    return csv_files

if __name__ == "__main__":
    sum = 0
    for filename in get_csv_filenames(DOCUMENT_BASE_PATH):
        with open(filename, mode='r') as file:
            reader = csv.reader(file)
            print('------------------')
            num_of_lines = len(list(reader))
            sum += num_of_lines
            print(f'{num_of_lines} lines in {filename}')

