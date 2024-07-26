OCR_FIX_TO_MARKDOWN_PROMPT = """Please proofread the following OCR-recognized text and convert it into Markdown format:
```
{ocr_text}
```
When proofreading and converting to Markdown, please follow these guidelines:

1. Correct OCR errors to make the text smooth and understandable.
2. Retain the original paragraph structure and overall document organization.
3. Use appropriate Markdown syntax for headings, lists, and other elements.
4. Remove any irrelevant characters or garbage text produced by OCR.
5. If the text includes image URLs, embed them using Markdown syntax.
6. For mathematical formulas, use LaTeX syntax in Markdown. For code snippets, use the appropriate Markdown code block syntax.
7. Use the same language as the OCR text (e.g., if the OCR text is in Chinese, the proofread text should also be in Chinese).
8. Maintain accuracy in technical terms and domain-specific vocabulary.
9. Ensure correct formatting of any tables or structured data in the text.
10. Ignore repeated content such as headers, footers, book titles, page numbers, etc.
11. If the text is truncated at the end, do not add any new characters or `...` after the last recognized character. Do not append any additional content to the end of the proofread Markdown.
12. The current document is a portion of all OCR content, which means there will be more sections to be fixed subsequently. Therefore, do not delete the content at the end arbitrarily, as it will be the beginning of the next OCR content.

Please output the proofread and formatted Markdown text within the code block, starting from the table of contents.

Example output:
```markdown
# Section 1
Content of Section 1...

## 1.1 Subsection
Content of Subsection 1.1...

# Section 2
Content of Section 2...

[Embed Image](image_url.jpg)

Mathematical Formula: $E = mc^2$

```code
print("Hello, World!")
```
```

Please remember, this is the first part of the document, so focus on establishing a clear structure and format for continuity in the subsequent parts.
"""

BLOCK_OCR_FIX_TO_MARKDOWN_PROMPT = """Please proofread the following OCR-recognized text and convert it into Markdown format, ensuring seamless integration with the previous content:

Previous part content (last {overlap} characters):
```
{pre_overlap}
```

Current OCR text to process:
```
{ocr_text}
```

Previous table of contents:
```
{pre_toc}
```

When proofreading and converting to Markdown, please follow these guidelines:

1. Ensure a smooth transition from the previous part. Begin precisely from the end of the previous section.
2. Maintain consistent formatting and style with the previous content.
3. Continue any incomplete sentences or ideas from the end of the previous part.
4. Use appropriate Markdown syntax for headings, lists, and other elements. Ensure heading levels are consistent with the overall document structure.
5. Correct OCR errors to make the text smooth and understandable.
6. Remove any irrelevant characters or garbage text produced by OCR.
7. For image URLs, use the correct Markdown embedding syntax.
8. For mathematical formulas, use LaTeX syntax in Markdown. For code snippets, use the appropriate Markdown code block syntax.
9. Use the same language as the OCR text (e.g., if the OCR text is in Chinese, the proofread text should also be in Chinese).
10. Maintain accuracy in technical terms and domain-specific vocabulary.
11. If processing content split across pages, ensure correct connection and smooth transition.
12. Do not repeat any overlapping content from the previous section.
13. Ignore repeated content such as headers, footers, book titles, page numbers, etc.
14. If the text is truncated at the end, do not add any new characters or `...` after the last recognized character. Do not append any additional content to the end of the proofread Markdown.
13. The current document is a portion of all OCR content, which means there will be more sections to be fixed subsequently. Therefore, do not delete the content at the end arbitrarily, as it will be the beginning of the next OCR content.


Please output the proofread and formatted Markdown text within the code block. The output should begin precisely from the end of the previous part, ensuring seamless continuity in the document.

Example output:
```markdown
...Content that continues from the previous section if applicable...

## New Section (if applicable)
Content of the new section...

### Subsection
Additional content...

[Embed Image](image_url.jpg)

Mathematical Formula: $E = mc^2$

```code
print("Hello, World!")
```
```

Please remember, the goal is to produce a section that can be directly appended to the previous content without manual adjustments, forming a complete and coherent document.
"""

OCR_FIX_TO_JSON_PROMPT = """Please correct the following OCR-recognized text and output the result in JSON format:
```
{ocr_text}
```

User-enforced JSON Format:
```
{enforced_json_format}
```
When making corrections, please adhere to these guidelines:
1. Correct misrecognized words and phrases to improve readability and comprehension
2. Maintain the original paragraph structure and line breaks
3. Identify and extract key information such as titles, headings, lists, names, dates, and numbers
4. Remove irrelevant characters, symbols, and garbled text introduced by OCR recognition errors
5. If user-enforced JSON format is provided, ensure that the corrected text is formatted accordingly
6. You should use language that is corresponding to the ocr text, for example, if the ocr text is in Chinese, the corrected text should also be in Chinese.

Finally, please output the corrected JSON text in a code block.

Example:
```
{{
  "key": "value",
  "key2": "value2"
}}
```"""

EXTRACT_MARKDOWN_PROMPT = """Please analyze the provided image and extract the content in Markdown format. The image will contain text, headings, lists, tables, and possibly code snippets.
When extracting the content, please adhere to the following guidelines:
1. Identify and extract text, preserving the original formatting and structure as much as possible
2. Detect and properly format headings (H1, H2, H3, etc.) using Markdown syntax
3. Recognize and format lists (ordered and unordered) using Markdown syntax
4. Identify and format tables using Markdown syntax, preserving the table structure and content
5. Detect and format any code snippets using Markdown code blocks, preserving the code's syntax and indentation
6. For mathematical formulas or equations, use appropriate Markdown syntax to maintain readability
7. If the image contains any inline images or diagrams, describe them using alt text in Markdown format
8. Preserve the original line breaks and paragraph structure to maintain readability

Finally, please output the extracted content in Markdown format within a code block.

Example:
```
# Title
This is a list:
- Item 1
- Item 2
```"""

EXTRACT_JSON_PROMPT = """Please analyze the image and extract the content in JSON format. The image may contain structured data, key-value pairs, lists, or other JSON-compatible content.
When extracting the content, please adhere to the following guidelines:
1. Identify and extract structured data, key-value pairs, lists, or other JSON-compatible content
2. Maintain the original structure and hierarchy of the extracted data
3. Correct any misrecognized words or phrases to ensure the extracted JSON is accurate
4. Remove any irrelevant characters, symbols, or garbled text introduced by OCR recognition errors
5. If the image contains nested data structures, represent them accurately in the extracted JSON format
6. You should use language that is corresponding to the ocr text, for example, if the ocr text is in Chinese, the extracted JSON should also be in Chinese.

Finally, please output the extracted content in JSON format within a code block.

Example:
```
{{
  "key": "value",
  "key2": "value2"
}}
```"""


COMMENT_PROMTPT = """You should also follow the instruction to complete the task:
{comment}
"""
