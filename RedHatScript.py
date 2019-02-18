import re,argparse,sys

# Use flags and arguments
parser = argparse.ArgumentParser()

# Use flags which can't run together
optional_group = parser.add_mutually_exclusive_group()

# Get a required argument after -r/--regex and store it in "regex" var.
parser.add_argument('-r', '--regex', action='store', dest='regex',
                    help='Searches for lines matching regular expression', required=True)
# Get an argument after -f/--files and store it in "in_files" var. This var is a list.
parser.add_argument('-f', '--files', action='store', dest='in_files', nargs='+',
                    required=False, help='The file to search in')
# Get an argument -u/--underscore. "underscore" will be True/False.
optional_group.add_argument('-u', '--underscore', action='store_true', dest='underscore',
                    help='prints ^ under the matching text', required=False)
# Get an argument -c/--color. "color" will be True/False.
optional_group.add_argument('-c', '--color', action='store_true', dest='color',
                    help='highlight matching text', required=False)
# Get an argument -m/--machine. "machine" will be True/False.
optional_group.add_argument('-m', '--machine', action='store_true', dest='machine',
                    help='generate machine readable output format: '
                    'file_name:no_line:start_pos:matched_text', required=False)

# Save all the results of the arguments in "results"
results = parser.parse_args()

# Use STDIN if file/s option wasn’t provided.
if results.in_files == None:
    results.in_files = str.split(sys.stdin.read())

# This function get pattern and list of files.
# It prints the file name and the line number for every match.
def fregex(pattern, files):
    index=1
    # For each file in the list "files"
    for file in files:
        # open the file
        with open(str(file)) as filedesc:
            # for each line on the file
            for line in filedesc:
                # if the pattern matches the text in the line
                if re.findall(pattern, line):
                    print('Filename:', file, 'line number:', index)
                    print(line)
                index+=1
            print('------------------')
            index=0

# This function get pattern and list of files.
# prints '^' under the matching text.
def funderscore (pattern, files):
    # For each file in the list "files"
    for file in files:
        # open the file
        with open(str(file)) as filedesc:
            # for each line on the file
            for line in filedesc:
                # creating a list of spaces in the length of the line
                expected = [' '] * len(line)
                # for each match between the pattern and the line
                for match in re.finditer(pattern, line):
                    # add '^' in each index which the pattern matches
                    expected[match.span()[0]] = '^'
                # if the pattern matches the text in the line
                if re.findall(pattern, line):
                    print(line, end="")
                    print(''.join(expected))
            print('------------------')

# function which gets a match between the pattern the text and returns it highlighted
def highlight_match(match):
    return "\033[1;42m" + format(match.group()) + "\033[1;m"

# This function get pattern and list of files.
# It prints the pattern highlighted in the line.
def fcolor(pattern, files):
    # For each file in the list "files"
    for file in files:
        # open the file
        with open(str(file)) as filedesc:
            for line in filedesc:
                # if the pattern matches the text in the line
                if re.findall(pattern,line):
                    # replace the patterned in the line with highlighted
                    replaced = re.sub(pattern, highlight_match, line)
                    print(replaced)
            print('------------------')

# This function get pattern and list of files.
# It prints it generated machine readable output
# format: file_name:no_line:start_pos:matched_text
def fmachine(pattern,files):
    index=1
    # For each file in the list "files"
    for file in files:
        # open the file
        with open(str(file)) as filedesc:
            for line in filedesc:
                # for each match between the pattern and the line
                for match in re.finditer(pattern, line):
                    print(file,':',index,':',match.span()[0],':',match.group())
                index+=1
            print('------------------')
            index=0

# if the user decided to use -u as an argument
if results.underscore:
    funderscore(results.regex, results.in_files)

# if the user decided to use -c as an argument
elif results.color:
    fcolor(results.regex,results.in_files)

# if the user decided to use -m as an argument
elif results.machine:
    fmachine(results.regex,results.in_files)

# if the user decided to use only -r,-f as arguments
else:
    fregex(results.regex,results.in_files)
