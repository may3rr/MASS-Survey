import openai
import os
import re

# 设置API密钥和基础URL
openai.api_key = 'sk-xx'
openai.api_base = "https://api.gpt.ge/v1"

def generate_chapter_content_from_file(structured_references_file):
    try:
        with open(structured_references_file, 'r', encoding='utf-8') as f:
            structured_references = f.read()
    except FileNotFoundError:
        print(f"Error: The file {structured_references_file} was not found.")
        return
    
    # 定义GPT-3.5的提示
    prompt_content = f"The following are section titles and related references. Please write the text content for each section.\n\n{structured_references}\n\nPlease write the section content. Only the body text needs to be outputted, omitting all other parts. Do not include #, and do not reply in Markdown format. Respond as per the specified requirements. Ensure that each section's content is sufficiently detailed and provides comprehensive analysis. The output should be at least 3000 characters long. Without hashtag#."
    
    
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

        response_message = completion.choices[0].message['content']
        print(f"Received response: {response_message}")

        if response_message:
            match = re.search(r'(\d+\.\d+)_structured_references\.txt$', structured_references_file)
            if match:
                new_file_name = match.group(1) + '_chapter_contents.txt'
            else:
                raise ValueError(f"Filename {structured_references_file} does not match the expected pattern")

            output_file = os.path.join(os.path.dirname(structured_references_file), new_file_name)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(response_message)
            
            print(f"Successfully generated {output_file}")
            return output_file
        else:
            print(f"Warning: No content generated for {structured_references_file}")

    except Exception as e:
        print(f"An error occurred while processing {structured_references_file}: {e}")

def generate_all_chapter_contents(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for file_name in os.listdir(input_folder):
        if file_name.endswith('_structured_references.txt'):
            match = re.search(r'(\d+\.\d+)_structured_references\.txt$', file_name)
            if match:
                new_file_name = match.group(1) + '_chapter_contents.txt'
                output_file = os.path.join(output_folder, new_file_name)
                if os.path.exists(output_file):
                    print(f"File {output_file} already exists. Skipping generation of chapter contents.")
                    continue

                print(f"Generating chapter contents for {file_name}")
                generated_file = generate_chapter_content_from_file(os.path.join(input_folder, file_name))
                if generated_file:
                    os.rename(generated_file, output_file)
                    print(f"Success: {output_file}")

# 调用函数
generate_all_chapter_contents('2structured_references-test', '4chapter_contents-test')
