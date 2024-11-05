import json
import os

def extract_references(json_file):
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    references = []
    reference_list = data.get('reference', [])
    reference_content_list = data.get('reference_content', [])

    reference_content_dict = {content['reference_num']: content.get('reference_abstract', "") for content in reference_content_list}

    for i, ref in enumerate(reference_list):
        reference_num = f"[{i+1}]"
        reference_title = ref if isinstance(ref, str) else ref.get('reference_title', "")
        reference_abstract = reference_content_dict.get(reference_num, "")

        references.append({
            "num": reference_num,
            "title": reference_title,
            "abstract": reference_abstract
        })

    return references

def save_references_as_txt(references, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        for ref in references:
            f.write(f'Number: {ref["num"]}\n')
            f.write(f'Title: {ref["title"]}\n')
            f.write(f'Abstract: {ref["abstract"]}\n')
            f.write('\n')

def process_all_json_files_and_save_txt(train_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    for file_name in os.listdir(train_folder):
        if file_name.endswith('.json'):
            json_file = os.path.join(train_folder, file_name)
            references = extract_references(json_file)

            output_file = os.path.join(output_folder, os.path.splitext(file_name)[0] + '_references.txt')
            save_references_as_txt(references, output_file)

process_all_json_files_and_save_txt('test1', 'references-test')
