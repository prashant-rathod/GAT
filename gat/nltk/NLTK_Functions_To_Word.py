from collections import OrderedDict

with open("NLTK_function") as f:
    content = f.readlines()
content = [x.strip('\n') for x in content]
# output.write(content)
module_name = "nltk_lexicon"
is_class = False
is_def = False
is_doc_string = False
is_first = True
function_name = ""
doc_string = "\t\"\"\"\n"
dict = OrderedDict()
output = open("NLTK_function_output.txt", "w")


def find_parenthesis_index(str):
    index = 0
    for i in range(len(str)):
        if str[i] == '(':
            index = i
            break
    return index


for line in content:
    words = line.split(" ")
    if words[0:4] != ["", "", "", ""]:  # if line isn't indented - usually it's a function or class
        if words[0] == "def":
            function_name = ""
            function_name += line[4:find_parenthesis_index(line)] + "\n\n"
            if is_first:  # if this is the first function, don't put it in the dictionary yet
                is_first = False
            else:
                if function_name not in dict:
                    dict[function_name] = ""


    elif words[0:4] == ["", "", "", ""] or is_doc_string:  # if line is indented - usually part of a function or class
        if words[4:7] == ["\"\"\""] or words[4:7] == ["\'\'\'"]:  # checks if its a docstring
            if is_doc_string:
                doc_string += "\n"
                dict[function_name] = doc_string
                doc_string = "\t Description: \n"
                is_doc_string = False
            else:
                is_doc_string = True
        elif is_doc_string:
            doc_string += "\t" + line + "\n"
        else:  # if it isn't a docstring
            continue
count = 1
for k, v in dict.items(): #prints out the functions with docstrings
    if v != "":
        print((str(count) + "."), k, v)
        count += 1
count = 1
for k, v in dict.items(): #prints out the functions without docstrings
    if v == "":
        print((str(count) + "."), k, v)
        count += 1
output.close()
