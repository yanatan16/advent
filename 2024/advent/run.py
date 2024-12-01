import importlib
import sys

def main():
    assert len(sys.argv) > 1
    assert isinstance(int(sys.argv[1]), int)

    day = sys.argv[1]
    mod = importlib.import_module(f'solutions.day{day}')
    mod.__dict__[f'Day{day}']().main()

if __name__ == '__main__':
    main()

