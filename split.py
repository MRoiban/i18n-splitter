import os
import argparse

def split_i18n_file(input_file, source_language, target_language, lines_per_file=50):
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    original_filename, _ = os.path.splitext(os.path.basename(input_file))
    total_pieces = len(lines) // lines_per_file + (1 if len(lines) % lines_per_file else 0)

    # Create the 'build' folder if it doesn't exist
    if not os.path.exists('build'):
        os.makedirs('build')

    for piece_number in range(total_pieces):
        start_line = piece_number * lines_per_file
        end_line = start_line + lines_per_file
        piece_content = [f"make a new canvas: translate the entire i18n file i'm giving you, make sure you translate it all from {source_language} to {target_language}, remove all comments,"+"never remove or add any '{ or } or remove any , (commas)' unless they were already present in the original text! Keep the same json form as the original text at all costs"+"\n"] +['"']+lines[start_line:end_line]+['"']

        piece_filename = f"./build/{original_filename}-{piece_number + 1}.txt"
        with open(piece_filename, 'w', encoding='utf-8') as piece_file:
            piece_file.writelines(piece_content)

    print(f"File '{input_file}' split into {total_pieces} pieces.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Split i18n file into pieces.')
    parser.add_argument('input_file', help='Path to the input file')
    parser.add_argument('--source_language', '-s', required=True, help='Source language of the file')
    parser.add_argument('--target_language', '-t', required=True, help='Target language for translation')
    args = parser.parse_args()

    split_i18n_file(args.input_file, args.source_language, args.target_language, lines_per_file=50)
