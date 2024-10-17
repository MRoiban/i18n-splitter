import os
import argparse

def split_i18n_file(input_file, lines_per_file=50):
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    original_filename, _ = os.path.splitext(input_file)
    total_pieces = len(lines) // lines_per_file + (1 if len(lines) % lines_per_file else 0)

    # Create the 'build' folder if it doesn't exist
    if not os.path.exists('build'):
        os.makedirs('build')

    for piece_number in range(total_pieces):
        start_line = piece_number * lines_per_file
        end_line = start_line + lines_per_file
        piece_content = lines[start_line:end_line] # ["translate the entire i18n file i'm giving you, make sure you translate it all in french:\n"] + 

        piece_filename = f"./build/{original_filename}-{piece_number + 1}.txt"
        with open(piece_filename, 'w', encoding='utf-8') as piece_file:
            piece_file.writelines(piece_content)

    print(f"File '{input_file}' split into {total_pieces} pieces.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Split i18n file into pieces.')
    parser.add_argument('input_file', help='Path to the input file')
    args = parser.parse_args()

    split_i18n_file(args.input_file, lines_per_file=50)
