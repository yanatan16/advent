import importlib
import sys

def main():
    assert len(sys.argv) > 1
    assert isinstance(int(sys.argv[1]), int)

    day = sys.argv[1]

    try:
        mod = importlib.import_module(f'solutions.day{day}')
    except ImportError:
        print(f"Couldnt import solutions.day{day}. Templating...")
        from . import template
        template.main()

        mod = importlib.import_module(f'solutions.day{day}')

    mod.__dict__[f'Day{day}']().main()

if __name__ == '__main__':
    main()

