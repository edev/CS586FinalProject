def sqlstr(string):
    """Return a string representation of the given string that can be used in a SQL query. string can be None."""
    if string is None:
        return 'NULL'
    else:
        return "'{}'".format(string)


def sqlint(integer):
    """Return an integer (or bigint) representation of the given integer that can be used in a SQL query.
    integer can be None."""
    if integer is None:
        return 'NULL'
    else:
        return integer


def sqlbool(boolean):
    """Return a boolean representation of the given boolean that can be used in a SQL query. boolean can be None."""
    if boolean is None:
        return "NULL"
    elif boolean is True or boolean is False:
        return str(boolean)
    else:
        # What IS it? Don't know.
        raise TypeError