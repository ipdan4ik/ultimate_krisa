def main():
    import argparse
    import pandas as pd

    index_col = 0

    parser = argparse.ArgumentParser(description='view csv file')
    parser.add_argument('-i', '--index',
                        action='store',
                        help='''Index column''')
    parser.add_argument('FILE',
                        nargs="?",
                        help='csv file')
    args = parser.parse_args()
    if not args.FILE:
        raise Exception('Filename not specified.')

    data = pd.read_csv(args.FILE, index_col=index_col)
    print(data)


if __name__ == '__main__':
    main()
