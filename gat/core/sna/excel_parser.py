import xlrd

# Read xlsx file and save the header and all the cells, each a dict with value and header label
# Input: xlsx file, sheet
def readFile(subAttrs, excel_file, sheet):

    workbook = xlrd.open_workbook(excel_file)
    sh = workbook.sheet_by_name(sheet)
    header = [str(sh.cell(0, col).value).strip("\n") for col in range(sh.ncols)]
    New_ncols = sh.ncols - 1

    # If any, delete all the empty features in the header
    while header[New_ncols] == '':
        header.remove(header[New_ncols])
        New_ncols -= 1

    # a list of nodes
    list = []
    for row in range(1, sh.nrows):
        tempList = []
        for col in range(New_ncols + 1):
            feature = str(sh.cell(0, col).value).strip("\n")
            cell = sh.cell(row, col).value
            if type(cell) == type(""):
                val = cell.strip("\n")
            else:
                val = str(cell)
            if val != "":  # handle empty cells
                # Make each node a dict with node name and node header, to assign later
                tempList.append({'val': val, 'header': feature})  # need to define attributes later
        list.append(tempList)

    # remove repeated column titles
    consolidatedHeader = []
    personal = True
    for feature in header:
        if (feature not in [header for header, tag in consolidatedHeader]) and (feature not in subAttrs):
            if feature == '':
                personal = False
                continue
            consolidatedHeader.append((feature,personal))

    return consolidatedHeader, list