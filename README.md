# document-reader

Leitor de documentos em Python para extrair campos, baseado em expressões regulares.

## Instalação

```bash

pip install document-reader
```

## Uso

```python
from document_reader import Document, Field


doc = Document("pdf_file.pdf")
doc.register_fields(
    Field(name="contract", regex=r"\d+/.*?/\d+", page=0),
    Field(name="nup", regex=r"\d{5}\.\d{6}/\d{4}-\d{2}", page=1),
)
data = doc.open()
print(data)
```