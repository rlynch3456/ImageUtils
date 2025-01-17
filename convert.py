import ImageUtils as iu
import sys
import os

def main():

    args = sys.argv
    if len(args) < 2:
        print('Usage <file path> | <folder path>')
        sys.exit()

    if os.path.isfile(args[1]):
        files = iu.convert_heic(args[1])
    elif os.path.isdir(args[1]):
        files = iu.convert_heic_directory(args[1])
    else:
        print(f'{args[1]} is neither a file nor a directory')
        return

    print(files)
    return

if __name__ == '__main__':
    main()