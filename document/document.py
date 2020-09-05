import csv
def read_lines(path):
    with open(path, 'r') as file:
        reader = file.read().split('\n')
        result = []
        for i in reader:
            i = i.strip()
            if i != '':
                result.append(i)
    return result


def read_csv(path):
    with open(path, 'r') as file:
        reader = [i for i in csv.reader(file) if i]
    return reader


def read_document(path):
    with open(path, 'r') as file:
        return file.read()

def cut_lines(path, count):
    reader = read_lines(path)
    write_lines(path, reader[count:], 'w')
    return del_protocol(reader[:count])

def write_csv_lines(path, string, mod='a'):
    with open(path, mod, encoding='utf8', newline='\n') as file:
        writer = csv.writer(file)
        writer.writerows(string)

def write_line(path, string, mod='a'):
    with open(path, mod, encoding='utf8', newline='\n') as file:
        writer = csv.writer(file)
        writer.writerow(string)


def debug(html, mod='r'):
    if mod == 'w':
        write_line('test.html', html, 'w')
    if mod == 'r':
        read_document('test.html')

def get_proxy():
    proxies = read_lines('text_files/proxies.txt')
    proxy = proxies.pop(0)
    proxies.append(proxy)
    write_lines('text_files/proxies.txt', proxies, 'w')
    return proxy
def write_lines(path, strings, mod='a'):
    strings = strings if type(strings) == list else [strings]

    with open(path, mod, encoding='utf8') as file:
        for i in strings:
            if i:
                file.write(str(i) + '\n')

def del_protocol(urls):
    return [i.replace('https://', '').replace('http://', '') for i in urls if i]