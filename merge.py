import os
import re
import argparse

def merge_i18n_chunks(output_file='./build/fr.json', chunk_pattern=r'output_\d+\.txt'):
    # Find all files that match the chunk pattern inside the build folder
    chunk_files = [f for f in os.listdir('build') if re.match(chunk_pattern, f)]
    
    # Sort chunk files by their numeric suffix
    chunk_files.sort(key=lambda x: int(re.search(r'_(\d+)\.txt', x).group(1)))

    # Merge contents of all chunk files
    with open(output_file, 'w', encoding='utf-8') as output:
        for chunk_file in chunk_files:
            with open(os.path.join('build', chunk_file), 'r', encoding='utf-8') as file:
                # Skip the first line as it's the prompt added during splitting
                output.writelines(["\n"]+file.readlines())

    # Delete the chunk files after merging
    for chunk_file in chunk_files:
        os.remove(os.path.join('build', chunk_file))

    print(f"Merged {len(chunk_files)} chunks into '{output_file}' and deleted the chunks.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Merge i18n chunks into a single file.')
    parser.add_argument('--name', '-n', default='fr', help='Output file name')
    args = parser.parse_args()

    output_file = f"./build/{args.name}.json"
    merge_i18n_chunks(output_file=output_file)
