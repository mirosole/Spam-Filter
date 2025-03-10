# utils.py
import os

def read_classification_from_file(file_path, base_path=''):
    classification_dict = {}

    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:         
            parts = line.strip().split()
            if len(parts) == 2:
                file_name, label = parts
                # Присоединяем базовый путь, если он предоставлен
                full_path = os.path.join(base_path, file_name)
                classification_dict[full_path] = label

    return classification_dict