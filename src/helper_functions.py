"""Useful functions for dealing with data from csv files."""

def qmarks(l: list):
    """Returns a comma separated string of question marks based on list length."""

    return (len(l) * "?,")[:-1] # exclude "," from the end

def to_str(l: list):
    """Returns a comma separated string of a list's contents."""

    return ",".join(l)

def ifnull(value):
    """Returns None datatype if the value is NULL in string format."""

    if value == "NULL":
        return None
    return value