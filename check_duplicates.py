import os
import json
from collections import defaultdict

def extract_questions(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        return []

    questions = []
    in_table = False
    for line in content.split('\n'):
        if line.startswith('|'):
            if 'Тип' in line and 'Вопрос (KR)' in line:
                in_table = True
                continue
            if in_table and line.count('|') >= 4:
                parts = [p.strip() for p in line.split('|')]
                if len(parts) >= 3 and parts[1] and '---' not in parts[1]:
                    question = parts[1].replace('<br>', ' ').strip()
                    if question and len(question) > 10:
                        questions.append((os.path.basename(filepath), question))
    return questions

# Собираем вопросы
all_questions = []
blocks = ['block_1_quiz', 'block_2_quiz', 'block_3_quiz', 'block_4_quiz']

for block in blocks:
    if not os.path.exists(block):
        continue
    for file in os.listdir(block):
        if file.endswith('.md'):
            filepath = os.path.join(block, file)
            all_questions.extend(extract_questions(filepath))

print(f'Всего вопросов: {len(all_questions)}')

# Группируем по вопросам
question_dict = defaultdict(list)
for file, q in all_questions:
    key = q[:100]  # Первые 100 символов
    question_dict[key].append(file)

# Находим дубликаты
duplicates = {}
for q, files in question_dict.items():
    if len(files) > 1:
        duplicates[q] = files

# Сохраняем в файл
with open('duplicates.json', 'w', encoding='utf-8') as f:
    json.dump({
        'total_questions': len(all_questions),
        'duplicates_count': len(duplicates),
        'duplicates': duplicates
    }, f, ensure_ascii=False, indent=2)

print(f'Обработано: {len(all_questions)} вопросов')
print(f'Повторов: {len(duplicates)}')
print('Результат сохранен в duplicates.json')
