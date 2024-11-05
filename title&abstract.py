import openai
import os
import re

# 设置API密钥和基础URL
openai.api_key = 'sk-xx'
openai.api_base = "https://api.gpt.ge/v1"

def generate_paper_title_and_abstract(structured_references_file):
    try:
        with open(structured_references_file, 'r', encoding='utf-8') as f:
            structured_references = f.read()
    except FileNotFoundError:
        print("Error: The file was not found.")
        return

    prompt_content = """
Based on the following section titles, please generate an appropriate title and a brief abstract for a review paper.

Section Titles:

Title: "{title_here}"
Abstract: "{abstract_here}"  
}

Please generate the paper title and abstract.
"""

    messages = [
        {'role': 'system', 'content': 'You are a helpful assistant.'},
        {'role': 'user', 'content': prompt_content}
    ]

    print(f"Sending prompt for file: {structured_references_file}")
    print(f"Prompt: {prompt_content}")

    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0125",
            messages=messages,
            stream=False  # 不需要流式响应，直接获取完整响应
        )

        full_response = completion.choices[0].message['content']
        print(f"Received response: {full_response}")

        # 使用正则表达式提取所需的文件名部分
        match = re.search(r'(\d+\.\d+)_structured_references\.txt$', structured_references_file)
        if match:
            new_file_name = match.group(1) + '_title_and_abstract.txt'
        else:
            raise ValueError(f"Filename {structured_references_file} does not match the expected pattern")

        output_file = os.path.join(os.path.dirname(structured_references_file), new_file_name)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(full_response)
        
        print(f"Successfully generated {output_file}")
        return output_file

    except Exception as e:
        print(f"An error occurred while processing {structured_references_file}: {e}")

def generate_all_titles_and_abstracts(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for file_name in os.listdir(input_folder):
        if file_name.endswith('_structured_references.txt'):
            match = re.search(r'(\d+\.\d+)_structured_references\.txt$', file_name)
            if match:
                new_file_name = match.group(1) + '_title_and_abstract.txt'
                output_file = os.path.join(output_folder, new_file_name)
                if os.path.exists(output_file):
                    print(f"File {output_file} already exists. Skipping generation of title and abstract.")
                    continue

                print(f"Generating title and abstract for {file_name}")
                generated_file = generate_paper_title_and_abstract(os.path.join(input_folder, file_name))
                if generated_file:
                    os.rename(generated_file, output_file)
                    print(f"Successfully renamed to {output_file}")

# 调用函数
generate_all_titles_and_abstracts('2structured_references-test', '3title_and_abstract-test')
