import datetime

yellow = '\033[01;33m'
white = '\033[01;37m'
green = '\033[01;32m'
blue = '\033[01;34m'
red = '\033[1;31m'
end = '\033[0m'
res = ""


def read_file_in_chunks(file_path, chunk_size=8):
    with open(file_path, 'r') as file:
        while True:
            data = file.read(chunk_size)
            if not data:
                break
            yield data


def remove_extra_chars(data):
    return data if len(data) == 8 else ''


file_path = 'res/res.txt'
for chunk in read_file_in_chunks(file_path):
    cleaned_chunk = remove_extra_chars(chunk)
    if cleaned_chunk:
        print(f"[{blue}{datetime.datetime.now().strftime('%H:%M:%S')}{end}] [{green}INFO{end}] {cleaned_chunk}: {chr(int(cleaned_chunk, 2))}")
        res += chr(int(cleaned_chunk, 2))

print(f"[{blue}{datetime.datetime.now().strftime('%H:%M:%S')}{end}] [{green}INFO{end}] {res}")
