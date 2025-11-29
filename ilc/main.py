import argparse
from frontend import compile_file, execute_file

def main():
    parser = argparse.ArgumentParser(prog='imagelang')
    sub = parser.add_subparsers(dest='cmd')
    c = sub.add_parser('compile'); c.add_argument('input'); c.add_argument('-o','--output', required=True)
    e = sub.add_parser('executar'); e.add_argument('input')
    args = parser.parse_args()
    if args.cmd == 'compile':
        compile_file(args.input, args.output)
        print('Compilação concluída.')
    elif args.cmd == 'executar':
        execute_file(args.input)
    else:
        parser.print_help()

if __name__ == '__main__': 
    main()
