with open('dictionary.txt', 'r') as f:
    words_string = f.readline()

words_list = words_string.split()

result_text = '\n'.join(words_list)

with open('result.txt', 'w') as f:
    f.write(result_text)

print('Преобразование завершено.')