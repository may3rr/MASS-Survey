# 代码运行顺序
1. **提取阶段 (extract)**: 首先运行 `extract.py`，从 JSON 文件中提取参考文献。该阶段会读取指定文件夹中的 JSON 文件，并提取出参考文献的相关信息，生成结构化的参考文献文件。
2. **结构化阶段 (structured)**: 接下来运行 `chapterContent.py`，根据提取的参考文献生成章节内容。此阶段会将参考文献转化为章节内容，并保存为文本文件，便于后续处理。
3. **标题阶段 (title)**: 然后运行 `title&abstract.py`，生成章节标题和摘要。该阶段会根据章节内容自动生成相应的标题和摘要，确保文档的逻辑性和可读性。
4. **内容阶段 (content)**: 接着运行 `content.py`，生成章节的详细内容。此阶段会根据标题和摘要生成详细的章节内容，丰富文档的内容。
5. **结论阶段 (conclusion)**: 最后运行 `Conclusion.py`，生成总结部分。该阶段会根据章节内容和主题生成总结，帮助读者快速理解文档的核心观点。
6. **整合阶段 (integrator)**: 最后运行 `integrator.py`，将所有部分整合在一起，形成完整的文档。此阶段会将提取的参考文献、章节内容、标题、摘要和结论整合为一个完整的文档格式，如 XML 或其他所需格式。

# 使用说明
请确保在运行代码之前，已准备好相应的 JSON 文件，并将其放置在指定的文件夹中。运行顺序应按照上述步骤进行，以确保生成的文档完整且结构合理。每个阶段的输出文件将作为下一个阶段的输入文件，因此请确保每个阶段都成功运行并生成所需的文件。

# 注意事项
- 确保 Python 环境中已安装所需的库，如 `openai` 和 `os`。
- 在运行代码之前，请检查 API 密钥和基础 URL 是否正确配置。
- 如果在运行过程中遇到文件未找到的错误，请检查文件路径和文件名是否正确。

# 示例
以下是一个示例文件夹结构，展示如何组织输入和输出文件：
```
project/
│
├── input/
│ ├── train2001.02611.content.ref.json
│ ├── train2002.12691.content.ref.json
│ └── ...
│
├── output/
│ ├── structured_references/
│ ├── chapter_contents/
│ ├── titles_and_abstracts/
│ ├── conclusions/
│ └── final_document.xml
│
└── scripts/
├── extract.py
├── chapterContent.py
├── title&abstract.py
├── content.py
├── Conclusion.py
└── integrator.py


```