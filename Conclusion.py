import openai
import os
import re

# 设置API密钥和基础URL
openai.api_key = 'sk-xx'
openai.api_base = "https://api.gpt.ge/v1"

def generate_conclusion(chapter_contents_file):
    try:
        with open(chapter_contents_file, 'r', encoding='utf-8') as f:
            chapter_contents = f.read()
    except FileNotFoundError:
        print("Error: The file was not found.")
        return

    prompt_content = "Based on the following section contents, please write the Conclusion section for the review paper.\n\nSection Contents:\n\n" + chapter_contents + "\n\n Do not include #, Please write the Conclusion:"

    messages = [
        {'role': 'system', 'content': 'You are a helpful assistant.'},
        {'role': 'user', 'content': prompt_content}
    ]

    print(f"Sending prompt for file: {chapter_contents_file}")
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
        match = re.search(r'(\d+\.\d+)_chapter_contents\.txt$', chapter_contents_file)
        if match:
            new_file_name = match.group(1) + '_conclusion.txt'
        else:
            raise ValueError(f"Filename {chapter_contents_file} does not match the expected pattern")

        output_file = os.path.join(os.path.dirname(chapter_contents_file), new_file_name)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(full_response)
        
        print(f"success: {output_file}")
        return output_file

    except Exception as e:
        print(f"An error occurred while processing {chapter_contents_file}: {e}")

def generate_all_conclusions(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for file_name in os.listdir(input_folder):
        if file_name.endswith('_chapter_contents.txt'):
            match = re.search(r'(\d+\.\d+)_chapter_contents\.txt$', file_name)
            if match:
                new_file_name = match.group(1) + '_conclusion.txt'
                output_file = os.path.join(output_folder, new_file_name)
                if os.path.exists(output_file):
                    print(f"File {output_file} already exists. Skipping generation of conclusion.")
                    continue

                print(f"Generating conclusion for {file_name}")
                generated_file = generate_conclusion(os.path.join(input_folder, file_name))
                if generated_file:
                    os.rename(generated_file, output_file)
                    print(f"Success: {output_file}")

# 调用函数
generate_all_conclusions('4chapter_contents-test', '5conclusion-test')
