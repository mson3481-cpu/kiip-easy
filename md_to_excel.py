"""
Конвертирует Markdown таблицы из всех папок block_*_quiz в Excel.
Каждая папка блока превращается в отдельный Excel файл.
"""
import re
import pandas as pd
from pathlib import Path


def parse_md_table(md_file: Path) -> list[dict] | None:
    """Парсит markdown таблицу из файла."""
    content = md_file.read_text(encoding='utf-8')

    # Разбиваем на строки и ищем таблицу
    lines = content.split('\n')

    # Находим начало таблицы (строка с | Тип |)
    table_start = -1
    for i, line in enumerate(lines):
        if '| Тип |' in line or '|Тип|' in line:
            table_start = i
            break

    if table_start == -1:
        print(f"  Таблица не найдена в {md_file.name}")
        return None

    # Извлекаем заголовки из строки table_start
    header_parts = lines[table_start].split('|')
    headers = [cell.strip() for cell in header_parts[1:-1]]

    # Извлекаем данные (начиная с table_start + 2, пропуская разделитель)
    data_rows = []
    for i in range(table_start + 2, len(lines)):
        line = lines[i].strip()
        if not line:
            continue  # Пропускаем пустые строки
        if not line.startswith('|'):
            break  # Таблица закончилась
        parts = line.split('|')
        cells = [cell.strip() for cell in parts[1:-1]]
        if cells and any(c for c in cells):  # Пропускаем пустые строки
            data_rows.append(cells)

    # Возвращаем заголовки + данные
    return [headers] + data_rows


def convert_block_to_excel(block_dir: Path) -> Path | None:
    """Конвертирует все MD файлы из папки блока в один Excel файл."""
    md_files = sorted(block_dir.glob('*.md'))

    if not md_files:
        return None

    output_file = block_dir.parent / f'{block_dir.name}_output.xlsx'

    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        for md_file in md_files:
            print(f"  Обработка: {md_file.name}")
            rows = parse_md_table(md_file)

            if not rows or len(rows) < 1:
                continue

            # Первая строка - заголовки, остальные - данные
            headers = rows[0]
            data = rows[1:] if len(rows) > 1 else []

            # Создаём DataFrame
            df = pd.DataFrame(data, columns=headers)

            # Имя листа из имени файла (без расширения), максимум 31 символ
            sheet_name = md_file.stem[:31]
            df.to_excel(writer, sheet_name=sheet_name, index=False)

            # Настраиваем форматирование
            from openpyxl.styles import Alignment
            worksheet = writer.sheets[sheet_name]
            for column in worksheet.columns:
                max_length = 0
                column_letter = column[0].column_letter
                for cell in column:
                    try:
                        if cell.value:
                            cell.alignment = Alignment(wrap_text=True, vertical='top')
                            lines = str(cell.value).split('\n')
                            max_line = max(len(line) for line in lines) if lines else 0
                            if max_line > max_length:
                                max_length = max_line
                    except:
                        pass
                adjusted_width = min(max_length + 2, 60)
                worksheet.column_dimensions[column_letter].width = adjusted_width

            # Высота строк
            for row in worksheet.iter_rows():
                worksheet.row_dimensions[row[0].row].height = 80

    return output_file


def convert_all_blocks():
    """Конвертирует все папки block_*_quiz."""
    base_dir = Path('.')

    # Ищем все папки block_*_quiz
    block_dirs = sorted(base_dir.glob('block_*_quiz'))

    print(f"Found {len(block_dirs)} block folders")
    print()

    for block_dir in block_dirs:
        print(f"[BLOCK] {block_dir.name}")
        output_file = convert_block_to_excel(block_dir)
        if output_file:
            print(f"   [OK] Created: {output_file.name}")
        print()


if __name__ == '__main__':
    convert_all_blocks()
