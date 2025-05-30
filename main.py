# Get a directory path from the user after checking the args for a directory path
import sys
import os



def get_directory_path():
    while True:
        dir_path = input("Please enter a directory path: ").strip()
        if os.path.isdir(dir_path):
            return dir_path
        else:
            print("Invalid directory path. Please try again.")

# read the contents of the directory
def read_directory_contents(dir_path):
    try:
        contents = os.listdir(dir_path)
        return contents
    except Exception as e:
        print(f"An error occurred while reading the directory: {e}")
        return []
    
# filter the contents looking for files which end with a number and .mp4
def filter_mp4_files(contents):
    mp4_files = [file for file in contents if file.endswith('.mp4') and any(char.isdigit() for char in file)]
    return mp4_files

# sort the filtered files by the number in their names
def sort_mp4_files(mp4_files):
    def extract_number(file_name):
        # Extract the number from the file name
        num_str = ''.join(filter(str.isdigit, file_name))
        return int(num_str) if num_str else float('inf')  # Return inf if no number found

    return sorted(mp4_files, key=extract_number)

# use the list of mp4 files to derive a file name for the output
def derive_output_file_name(sorted_files, dir_path):
    if not sorted_files:
        return "output.mp4"  # Default name if no files found

    # Use the first file's name to derive the output file name
    first_file = sorted_files[0]
    base_name = os.path.splitext(first_file)[0]  # Remove the .mp4 extension
    # and remove any digits from the base name
    base_name = ''.join(filter(lambda x: not x.isdigit(), base_name))
    # Create the output file name by appending "_concatenated" to the base name
    return os.path.join(dir_path, f"{base_name}_concatenated.mp4")

def concatenate_mp4_files(dir_path, sorted_files, output_file):
    if not sorted_files:
        print("No MP4 files to concatenate.")
        return
    
    # Create a temporary file to store the list of files to concatenate
    with open('file_list.txt', 'w') as f:
        for file in sorted_files:
            f.write(f"file '{os.path.join(dir_path, file)}'\n")
    
    # Use ffmpeg to concatenate the files
    command = f"ffmpeg -f concat -safe 0 -i file_list.txt -c copy '{output_file}'"
    os.system(command)
    
    # Clean up the temporary file
    os.remove('file_list.txt')
    
    print(f"Concatenation complete. Output file: {output_file}")

# use ffmpeg to concatenate the sorted mp4 files into a single file from the derived name
def main():
    if len(sys.argv) > 1:
        dir_path = sys.argv[1]
    else:
        dir_path = get_directory_path()
    if not os.path.isdir(dir_path):
        print(f"Provided path '{dir_path}' is not a valid directory.")
        sys.exit(1)
    
    contents = read_directory_contents(dir_path)
    mp4_files = filter_mp4_files(contents)
    
    if not mp4_files:
        print("No valid MP4 files found in the directory.")
        return
    
    sorted_files = sort_mp4_files(mp4_files)
    output_file = derive_output_file_name(sorted_files, dir_path)
    
    print(f"Sorted MP4 files: {sorted_files}")
    concatenate_mp4_files(dir_path, sorted_files, output_file)

if __name__ == "__main__":
    main()