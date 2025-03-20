from pathlib import Path
from sys import stderr
from pypdf import PdfReader, PdfWriter

# 30 pages is the maximum that PaperCut will allow in a single print job
# Note that this should be even so that double-sided printing can carry forward
PAGES_PER_CHUNK = 10


def get_file_path():
    raw_input = input("Enter PDF file path: ")
    # Allow quoted path, like you get if you drag and drop a file into the terminal
    if raw_input.startswith("'") and raw_input.endswith("'"):
        raw_input = raw_input[1:-1]
    return Path(raw_input)


def main():
    file_path = get_file_path()
    try:
        reader = PdfReader(file_path)
        print(f"Opened PDF {file_path}")
    except OSError as error:
        print(error, file=stderr)
        return

    total_pages = len(reader.pages)
    print(f"Processing {total_pages} pages")

    done = False
    chunk_number = 1
    while not done:
        print(f"Creating chunk #{chunk_number}...")
        writer = PdfWriter()
        pages_added = 0
        for page in reader.pages:
            writer.add_page(page)
            pages_added += 1
            if pages_added == PAGES_PER_CHUNK:
                break
        # Write the file
        output_path = Path("temp", f"Part {chunk_number} - {file_path.stem}.pdf")
        output_path.parent.mkdir(exist_ok=True)
        with open(output_path, "wb") as output_file:
            writer.write(output_file)
        print(f"Created {output_path}")
        # End the loop if we've gotten through the PDF
        chunk_number += 1
        if pages_added < PAGES_PER_CHUNK:
            done = True


if __name__ == "__main__":
    main()
