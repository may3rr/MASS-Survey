from pathlib import Path
import openai
import os
import re

# 设置API密钥和基础URL
openai.api_key = 'sk-xx'
openai.api_base = "https://api.gpt.ge/v1"

def get_file_size(file_path):
    """
    获取文件大小，以KB为单位
    """
    return os.path.getsize(file_path) / 1024  # 转换为KB

def analyze_references(references_txt_file):
    with open(references_txt_file, 'r', encoding='utf-8') as file:
        file_content = file.read()

    # 根据文件大小选择使用的模型
    file_size_kb = get_file_size(references_txt_file)
    if file_size_kb > 150:
        model_name = "gpt-4o-2024-05-13"
    else:
        model_name = "gpt-3.5-turbo-0125"

    prompt_content = f"""
The following are some references and their abstracts. Please analyze these references, find their logical relationships in a review, and classify them. You are not allowed to omit any references; you must classify all of them. Output structured section titles with the related references listed under each section title. Here is an example:

**Analysis of References and Logical Relationships**

**Section 1: Navigation and Route Planning**
- [1] M. Duckham, L. Kulik, "Simplest" Paths: Automated Route Selection for Navigation. This paper introduces the concept of "simplest" paths in contrast to shortest paths, focusing on reducing instruction complexity for human navigators. It proposes an algorithm with quadratic computation time and demonstrates its potential benefits for navigation systems, suggesting future cognitive studies to validate the computational results.

**Section 2: Exoplanet Research and Atmospheric Characterization**
- The reference provided seems to be a misnumbered continuation from another part of the text and does not have a clear title or number associated with the abstract provided. However, it discusses the measurement of exoplanet eclipse depths and the implications for the planet's atmosphere, indicating research into astrobiology or extrasolar planet characterization.

**Section 3: Music Analysis and Generation**
- [306] A. Anglade, R. Ramirez, S. Dixon, et al., Genre Classification Using Harmony Rules Induced from Automatic Chord Transcriptions. This study explores techniques for genre classification in music through harmony rules derived from automatic chord transcriptions.
- [123] T. E. Ahonen, K. Lemström, S. Linkola, Compression-based Similarity Measures in Symbolic, Polyphonic Music. This work focuses on developing compression-based similarity measures for symbolic, polyphonic music, contributing to the field of music information retrieval.

These classifications group the references into thematic sections based on their primary subjects, such as navigation technology, AI safety, exoplanetary science, music analysis and generation, linguistic and music theoretical frameworks, and interactive content creation.

Please start the analysis(Most Important!!!!Most Important!!!!Most Important!!!!: Do not group any multiple references into a single entry. Each reference must be listed as a separate entry, even if they cover related topics. Ensure that every reference is individually listed and described, avoiding any form of consolidation or summary of multiple references into one. Without hashtag#.
):

{file_content}
"""

    messages = [
        {'role': 'system', 'content': 'You are a helpful assistant.'},
        {'role': 'user', 'content': prompt_content}
    ]

    completion = openai.ChatCompletion.create(
        model=model_name,
        messages=messages,
        stream=True
    )

    full_response = ""
    for chunk in completion:
        if chunk.choices[0].delta.get("content"):
            full_response += chunk.choices[0].delta["content"]

    match = re.search(r'train(\d+\.\d+)\.content\.ref_references\.txt$', references_txt_file)
    if match:
        new_file_name = match.group(1) + '_structured_references.txt'
    else:
        raise ValueError(f"Filename {references_txt_file} does not match the expected pattern")

    output_file = os.path.join(os.path.dirname(references_txt_file), new_file_name)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(full_response)
    print(f"Successfully generated {output_file}")
    return output_file

def analyze_all_references(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for file_name in os.listdir(input_folder):
        if file_name.endswith('_references.txt'):
            match = re.search(r'train(\d+\.\d+)\.content\.ref_references\.txt$', file_name)
            if match:
                new_file_name = match.group(1) + '_structured_references.txt'
                output_file = os.path.join(output_folder, new_file_name)
                if os.path.exists(output_file):
                    print(f"File {output_file} already exists. Skipping analysis.")
                    continue

                generated_file = analyze_references(os.path.join(input_folder, file_name))
                os.rename(generated_file, output_file)
                print(f"Successfully renamed to {output_file}")

analyze_all_references('references-test', '2structured_references-test')
