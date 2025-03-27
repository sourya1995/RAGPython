import logging
from file_parser import FileParser

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    files = ["obama.txt", "obama.pdf", "obama-ocr.pdf"]

    for filename in files:
        try:
            parser = FileParser(filepath=filename)
            content = parser.parse()
            print(f"Content of {filename}:")
            print(content[:500])
            print("-------------------------------------------------")
        except Exception as e:
            logging.error(f"Failed to process file '{filename}': {e}")

if __name__ == "__main__":
    main()