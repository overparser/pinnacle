def read_lines(path):
    with open(path, 'r') as file:
        reader = file.read().split('\n')
        result = []
        for i in reader:
            i = i.strip()
            if i != '':
                result.append(i)
    return result
    return del_protocol(result)

def read_document(path):
    with open(path, 'r') as file:
        return file.read()

def cut_lines(path, count):
    reader = read_lines(path)
    write_lines(path, reader[count:], 'w')
    return del_protocol(reader[:count])


def write_line(path, string, mod='a'):
    with open(path, mod, encoding='utf8') as file:
        file.write(str(string) + '\n')
def debug(html, mod='r'):
    if mod == 'w':
        write_line('test.html', html, 'w')
    if mod == 'r':
        read_document('test.html')

def write_lines(path, strings, mod='a'):
    strings = strings if type(strings) == list else [strings]

    with open(path, mod, encoding='utf8') as file:
        for i in strings:
            if i:
                file.write(str(i) + '\n')

def del_protocol(urls):
    return [i.replace('https://', '').replace('http://', '') for i in urls if i]