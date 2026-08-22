from docx import Document

doc = Document("Paper_Review_Plain_Language.docx")
for para in doc.paragraphs:
    print(para.text)
