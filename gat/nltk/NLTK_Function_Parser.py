with open("NLTK_function") as f:
    content = f.readlines()
content = [x.strip('\n') for x in content]
# output.write(content)
module_name = "nltk_lexicon"
is_class = False
is_def = False
is_doc_string = False
is_first = True
function_name = "def "
doc_string = "\t\"\"\"\n"
output = open("NLTK_function_output.txt", "w")


def remove_equals(str):
    start_index = 0
    end_index = 0
    found = False
    for i in range(len(str)):
        if str[i] == "=":
            start_index = i
            found = True
        if str[i] == ")" and found:
            end_index = i
            found = False
    return str[0:start_index] + str[end_index:]


for line in content:
    words = line.split(" ")
    if words[0:4] != ["", "", "", ""]:  # if line isn't indented - usually it's a function or class
        if words[0] == "class":
            is_class = True
            is_def = False
        elif words[0] == "def":
            is_class = False
            is_def = True
            if is_first:  # if this is the first function, don't output.write out a return
                is_first = False
            else:
                output.write(
                    "\treturn " + module_name + "." + remove_equals(" ".join(function_name.split(" ")[1:])[:-1]) + "\n")
                function_name = "def "
            function_name += " ".join(words[1:])
            output.write(function_name + "\n")

    elif words[0:4] == ["", "", "", ""]:  # if line is indented - usually part of a function or class
        if words[4:7] == ["\"\"\""] or words[4:7] == ["\'\'\'"]:  # checks if its a docstring
            if is_doc_string:
                doc_string += "\t\"\"\"\n"
                if is_def:
                    output.write(doc_string)
                    doc_string = "\t\"\"\"\n"

                is_doc_string = False
            else:
                is_doc_string = True
        elif is_doc_string:
            doc_string += line + "\n"
        else:  # if it isn't a docstring
            continue

output.write("\treturn " + module_name + "." + " ".join(function_name.split(" ")[1:])[:-1] + "\n")
output.close()
