def read_header_and_rows_as_strings(filepath):
    f = open(filepath, "r")
    data = [[v.strip() for v in line.split(",")] for line in f.readlines()]
    f.close()
    header = data[0]
    rows = data[1:]
    return header, rows

def write_header_and_rows(filepath, header, rows):
    content = ""
    content += str(header)[1:-1] + "\n"
    for row in rows:
        row_str = ""
        for value in row:
            row_str += str(value) + ","
        content += row_str[:-1] + "\n"
    f = open(filepath, "w")
    f.write(content)
    f.close()
