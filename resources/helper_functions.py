def format_currency(val):
    """
    Convert the given value to a string with no decimal places and comma as thousand separator.
    """
    return val.apply(lambda x: "£ {:,.0f}".format(x))
