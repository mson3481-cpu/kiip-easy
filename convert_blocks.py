#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Конвертация KIAP вопросов из Markdown в JSON"""

import json
import re
import os

# Настройки блоков
BLOCKS_CONFIG = {
    1: {
        "files": ["block_1_quiz/ch1_Kiip.md", "block_1_quiz/ch2_kiip.md",
                  "block_1_quiz/ch3_Kiip.md", "block_1_quiz/ch4_Kiip.md"],
        "chapters_range": [1, 4],
        "title": "Блок 1: Главы 1-4",
        "theme": "theme-blue",
        "chapters": "1~4과",
        "subtitle": "Знакомство, школа, офис"
    },
    2: {
        "files": ["block_2_quiz/ch5_Kiip.md", "block_2_quiz/ch6_Kiip.md",
                  "block_2_quiz/ch7_Kiip.md", "block_2_quiz/ch8_Kiip.md",
                  "block_2_quiz/ch9_Kiip.md"],
        "chapters_range": [5, 9],
        "title": "Блок 2: Главы 5-9",
        "theme": "theme-yellow",
        "chapters": "5~9과",
        "subtitle": "Время, еда, покупки"
    },
    3: {
        "files": ["block_3_quiz/ch10_Kiip.md", "block_3_quiz/ch11_Kiip.md",
                  "block_3_quiz/ch12_Kiip.md", "block_3_quiz/ch13_Kiip.md",
                  "block_3_quiz/ch14_Kiip.md"],
        "chapters_range": [10, 14],
        "title": "Блок 3: Главы 10-14",
        "theme": "theme-green",
        "chapters": "10~14과",
        "subtitle": "Семья, транспорт, аптека"
    },
    4: {
        "files": ["block_4_quiz/ch15_Kiip.md", "block_4_quiz/ch16_Kiip.md",
                  "block_4_quiz/ch17_Kiip.md", "block_4_quiz/ch18_Kiip.md"],
        "chapters_range": [15, 18],
        "title": "Блок 4: Главы 15-18",
        "theme": "theme-pink",
        "chapters": "15~18과",
        "subtitle": "Погода, больница, планы"
    }
}

def parse_question_type(type_text):
    """Конвертирует тип вопроса в стандартный формат"""
    # Убираем пробелы и скобки
    type_text = type_text.strip()

    # Карта соответствия корейских типов русским
    type_map = {
        "어휘": "Лексика",
        "문법": "Грамматика",
        "읽기": "Чтение",
        "문화": "Культура",
        "발음": "Произношение",
        "례절": "Вежливость",
        "Лексика": "Лексика",
        "Грамматика": "Грамматика",
        "Культура": "Культура",
        "Чтение": "Чтение",
        "Вежливость": "Вежливость",
        "Логика": "Логика"
    }

    for key, value in type_map.items():
        if key in type_text:
            return value

    # Если тип не найден, возвращаем как есть
    return type_text

def parse_markdown_table(file_path, chapter_num):
    """Парсит вопросы из Markdown таблицы"""
    questions = []

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Разбиваем на строки
    lines = content.split('\n')

    # Ищем начало таблицы
    table_start = -1
    for i, line in enumerate(lines):
        if '| Тип |' in line or '| Тип' in line or '| тип' in line:
            table_start = i
            break

    if table_start == -1:
        print(f"Warning: table not found in {file_path}")
        return questions

    # Парсим строки таблицы
    for i in range(table_start + 2, len(lines)):  # +2 пропускает заголовок и сепаратор
        line = lines[i].strip()

        if not line.startswith('|'):
            continue

        # Разбиваем строку по |
        parts = [p.strip() for p in line.split('|')[1:-1]]  # Убираем пустые элементы в начале и конце

        if len(parts) < 5:
            continue

        question_type = parse_question_type(parts[0])
        question_text = parts[1]
        options_text = parts[2]
        answer_num = parts[3].strip()
        explanation = parts[4]

        # Парсим варианты ответов
        options = []
        for opt in options_text.split('<br>'):
            opt = opt.strip()
            # Убираем нумерацию если есть (1), 2) и т.д.)
            opt = re.sub(r'^\d+\)\s*', '', opt)
            if opt:
                options.append(opt)

        # Если вариантов меньше 4, добавляем пустые
        while len(options) < 4:
            options.append("")

        # Парсим номер ответа
        try:
            correct_answer = int(answer_num)
        except ValueError:
            correct_answer = 1

        # Форматируем объяснение
        # Конвертируем Markdown в HTML
        explanation_html = explanation.replace('\n', '<br>')
        # **text** → <strong>text</strong>
        explanation_html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', explanation_html)
        # Оборачиваем в параграфы
        explanation_html = f"<p>{explanation_html}</p>"
        explanation_html = explanation_html.replace('<br><br>', '</p><p>')

        question = {
            "id": 0,  # Будет установлен позже
            "chapter": chapter_num,
            "type": question_type,
            "question": question_text,
            "options": options[:4],
            "correctAnswer": correct_answer,
            "explanation": explanation_html
        }

        questions.append(question)

    return questions

def convert_block(block_num):
    """Конвертирует весь блок"""
    config = BLOCKS_CONFIG[block_num]

    all_questions = []
    start_chapter, end_chapter = config["chapters_range"]

    for idx, file_path in enumerate(config["files"]):
        chapter_num = start_chapter + idx
        full_path = os.path.join(os.path.dirname(__file__), file_path)

        if not os.path.exists(full_path):
            print(f"File not found: {full_path}")
            continue

        questions = parse_markdown_table(full_path, chapter_num)
        all_questions.extend(questions)
        print(f"Chapter {chapter_num}: {len(questions)} questions")

    # Устанавливаем ID
    for i, q in enumerate(all_questions, 1):
        q["id"] = i

    # Создаём JSON структуру
    result = {
        "block": block_num,
        "title": config["title"],
        "theme": config["theme"],
        "chapters": config["chapters"],
        "subtitle": config["subtitle"],
        "questions": all_questions
    }

    # Сохраняем
    output_path = f"kiip-easy/data/block{block_num}.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"\n[OK] Block {block_num} saved: {output_path}")
    print(f"   Total questions: {len(all_questions)}\n")

    return len(all_questions)

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    print("=== Converting KIIP Blocks ===")

    for block_num in [2, 3, 4]:
        print(f"\nConverting Block {block_num}...")
        convert_block(block_num)

    print("\n=== Done! ===")
