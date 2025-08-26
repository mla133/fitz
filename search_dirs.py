import fitz  # PyMuPDF
import os

def search_pdfs_in_directory(directory_path, search_term):
    results = []

    for filename in os.listdir(directory_path):
        if filename.lower().endswith(".pdf"):
            file_path = os.path.join(directory_path, filename)
            doc = fitz.open(file_path)

            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                text = page.get_text()
                lines = text.split('\n')

                for line_num, line in enumerate(lines, start=1):
                    if search_term.lower() in line.lower():
                        results.append({
                            'file': filename,
                            'page': page_num + 1,
                            'line': line_num,
                            'text': line.strip()
                        })

            doc.close()

    return results

# Example usage
directory = "../../PDFs/"
term = "Matt"
matches = search_pdfs_in_directory(directory, term)

for match in matches:
    print(f"{match['file']} - Page {match['page']}, Line {match['line']}: {match['text']}")
