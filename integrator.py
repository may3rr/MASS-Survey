import os
import re
import xml.etree.ElementTree as ET

def generate_xml(input_folder, output_folder):
    # 设置文件夹路径
    title_and_abstract_folder = os.path.join(input_folder, '3title_and_abstract-test')
    chapter_contents_folder = os.path.join(input_folder, '4chapter_contents-test')
    conclusion_folder = os.path.join(input_folder, '5conclusion-test')
    references_folder = os.path.join(input_folder, 'references-test')

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for file_name in os.listdir(title_and_abstract_folder):
        if file_name.endswith('_title_and_abstract.txt'):
            base_name = file_name.split('_')[0]

            try:
                with open(os.path.join(title_and_abstract_folder, file_name), 'r', encoding='utf-8') as f:
                    title_and_abstract = f.read().strip()
                print(f"Title and Abstract read successfully from {file_name}.")
            except FileNotFoundError:
                print(f"Error: The file '{file_name}' was not found.")
                continue

            # 解析title和abstract
            title_match = re.search(r'Title:\s*"(.+?)"', title_and_abstract)
            abstract_match = re.search(r'Abstract:\s*(.*)', title_and_abstract, re.DOTALL)
            
            if title_match and abstract_match:
                title = title_match.group(1).strip()
                abstract = abstract_match.group(1).strip()
                print("Title and Abstract parsed successfully.")
            else:
                print("Error: Title or Abstract not found in the expected format.")
                continue

            # 创建XML结构
            root = ET.Element("Literature")

            title_element = ET.SubElement(root, "Title")
            title_element.text = title

            abstract_element = ET.SubElement(root, "Abstract")
            abstract_element.text = abstract

            # 读取4chapter_contents文件夹中的文件
            chapter_file = os.path.join(chapter_contents_folder, f'{base_name}_chapter_contents.txt')
            try:
                with open(chapter_file, 'r', encoding='utf-8') as f:
                    chapter_contents = f.read().strip()
                print(f"Chapter Contents read successfully from {chapter_file}.")
            except FileNotFoundError:
                print(f"Error: The file '{chapter_file}' was not found.")
                continue

            # 去掉所有的*号，并提取章节标题和内容
            chapter_contents = chapter_contents.replace('*', '')
            
            # 使用正则表达式匹配章节标题和内容
            chapter_matches = re.findall(r'Section \d+: (.*?)\n(.*?)(?=\nSection \d+:|$)', chapter_contents, re.DOTALL)
            
            for i, (chapter_title, chapter_text) in enumerate(chapter_matches, 1):
                chapter_title_element = ET.SubElement(root, f"Section_{i}_title")
                chapter_title_element.text = chapter_title.strip()
                print(f"Added {chapter_title} to XML.")
                
                # 去掉章节内容中可能重复的章节标题
                chapter_text = re.sub(r'Section \d+: .*?\n', '', chapter_text).strip()

                chapter_text_element = ET.SubElement(root, f"Section_{i}_text")
                chapter_text_element.text = chapter_text
                print(f"Added content for {chapter_title} to XML with length: {len(chapter_text)}")

            # 读取5conclusion文件夹中的文件
            conclusion_file_path = os.path.join(conclusion_folder, f'{base_name}_conclusion.txt')
            try:
                with open(conclusion_file_path, 'r', encoding='utf-8') as f:
                    conclusion = f.read().strip()
                print(f"Conclusion read successfully from {conclusion_file_path}.")
            except FileNotFoundError:
                print(f"Error: The file '{conclusion_file_path}' was not found.")
                continue

            # 添加Conclusion章节
            conclusion_section_num = len(chapter_matches) + 1
            conclusion_title_element = ET.SubElement(root, f"Section_{conclusion_section_num}_title")
            conclusion_title_element.text = "Conclusion"

            conclusion_text_element = ET.SubElement(root, f"Section_{conclusion_section_num}_text")
            conclusion_text_element.text = conclusion
            print(f"Added Conclusion to XML.")

            # 读取references文件夹中的文件
            references_file_path = os.path.join(references_folder, f'train{base_name}.content.ref_references.txt')
            try:
                with open(references_file_path, 'r', encoding='utf-8') as f:
                    references = f.read().strip()
                print(f"References read successfully from {references_file_path}.")
            except FileNotFoundError:
                print(f"Error: The file '{references_file_path}' was not found.")
                continue

            # 提取所有的参考文献
            reference_matches = re.findall(r'Number: \[\d+\]\nTitle: (.*?)\nAbstract: .*?(?=\nNumber: \[\d+\]|\Z)', references, re.DOTALL)
            
            # 将参考文献拼接成一个字符串
            references_text = ' '.join(ref.strip() for ref in reference_matches)

            # 添加参考文献到XML
            references_element = ET.SubElement(root, "References")
            references_element.text = references_text
            print(f"Added References to XML.")

            # 将XML写入文件
            output_file = os.path.join(output_folder, f"{base_name}.xml")
            tree = ET.ElementTree(root)
            tree.write(output_file, encoding='utf-8', xml_declaration=True)
            print(f"success: {output_file}")

generate_xml('', '6final_papers-test')
