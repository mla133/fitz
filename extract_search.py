import fitz  # PyMuPDF

def search_pdf_text(pdf_path, search_term):
    doc = fitz.open(pdf_path)
    results = []

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text = page.get_text()
        lines = text.split('\n')

        for line_num, line in enumerate(lines, start=1):
            if search_term.lower() in line.lower():
                results.append({
                    'page': page_num + 1,
                    'line': line_num,
                    'text': line.strip()
                })

    doc.close()
    return results

# Example usage
matches = search_pdf_text("../../PDFs/blough_revised-hhw-tutorial.pdf", "VS.85")
for match in matches:
    print(f"Page {match['page']}, Line {match['line']}: {match['text']}")
