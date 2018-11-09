class TsvReader:
    """Provides a line-by-line, iterable reader for processing tab-separated values."""

    def __init__(self, filename):
        # Raises error on failure; we just won't catch it.
        self.file = open(filename, 'r', encoding='utf-8')

    def __iter__(self):
        return self

    def __next__(self):

        if self.file is None:
            raise StopIteration

        line = self.file.readline()
        if line == '':
            raise StopIteration

        # Else we have a valid line to process - assuming the line was well-formed.
        # If it's not well-formed, that's the user's problem. we'll do our best.
        return line.strip().split('\t')

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file.close()
        self.file = None
