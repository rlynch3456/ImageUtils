import ImageUtils as iu
import sys

def main():
    args = sys.argv

    if len(args) < 3:
        print('usage <file1> file2> <output file True|False>')
        sys.exit()

    if len(args) == 3:
        results = iu.compare_images(args[1], args[2])
    if len(args) > 3:
        results = iu.compare_images(args[1], args[2], True)
    if not results == None:
        print(f'Pixel Match Percentage: {results['pixel_match']:.2f}%')
        print(f'Color Match Percentage: {results['color_match']:.2f}')
        print(f'Output File: {results['output_file']}')
        return

if __name__ == '__main__':
    main()
