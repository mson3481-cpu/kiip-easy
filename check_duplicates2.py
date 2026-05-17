import os
import json
import re
from collections import defaultdict

def extract_questions(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        return []

    questions = []
    lines = content.split('\n')
    i = 0
    while i < len(lines):
        line = lines[i]
        # Ищем начало таблицы
        if 'Тип' in line and 'Вопрос (KR)' in line:
            i += 2  # Пропускаем заголовок и разделитель
            # Читаем строки таблицы
            while i < len(lines) and lines[i].startswith('|'):
                parts = [p.strip() for p in lines[i].split('|')]
                # Пропускаем пустые или короткие строки
                if len(parts) >= 4 and parts[1] and '---' not in parts[1]:
                    question = parts[1].strip()
                    # Очищаем от тегов и коротких строк
                    question = re.sub(r'<br>', ' ', question)
                    question = question.strip()
                    # Берем только вопросы с корейским текстом (содержат хангыль)
                    if len(question) > 20 and re.search(r'[가-힣]', question):
                        questions.append((os.path.basename(filepath), question))
                i += 1
        else:
            i += 1
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
            questions = extract_questions(filepath)
            print(f'{block}/{file}: {len(questions)} вопросов')
            all_questions.extend(questions)

print(f'\nВсего вопросов: {len(all_questions)}')

# Группируем по вопросам (ищем точные совпадения)
question_dict = defaultdict(list)
for file, q in all_questions:
    question_dict[q].append(file)

# Находим дубликаты
duplicates = {q: files for q, files in question_dict.items() if len(files) > 1}

print(f'\nРезультат проверки:')
print(f'Уникальных вопросов: {len(question_dict)}')
print(f'Дубликатов: {len(duplicates)}')

if duplicates:
    print('\n⚠️ НАЙДЕННЫЕ ДУБЛИКАТЫ:')
    for i, (q, files) in enumerate(list(duplicates.items())[:10]):
        print(f'\n{i+1}. {q[:80]}...')
        print(f'   Файлы: {", ".join(set(files))}')

    with open('real_duplicates.json', 'w', encoding='utf-8') as f:
        json.dump({
            'total': len(all_questions),
            'unique': len(question_dict),
            'duplicates': len(duplicates),
            'duplicate_list': [{'question': q, 'files': list(set(files))} for q, files in list(duplicates.items())[:20]]
        }, f, ensure_ascii=False, indent=2)
else:
    print('✅ ПОВТОРОВ НЕТ — все вопросы уникальные!')
