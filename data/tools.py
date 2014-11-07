def read_file(path):
    """
    :param path:
    :return:
    """
    with open(path) as f:
        content = f.readlines()
        return content


def read_open_file(file):
    """
    :param path:
    :return:
    """
    content = file.readlines()
    return content


def print_html_message(message):
    """
    :param message:
    """
    print "<p style=\"font-family:sans-serif\">"+str(message)+"</p>"


def print_html_message_h1(message):
    """
    :param message:
    """
    print "<h1 style=\"font-family:sans-serif\">"+str(message)+"</h1>"


def print_html_message_h3(message):
    """
    :param message:
    """
    print "<h3 style=\"font-family:sans-serif\">"+str(message)+"</h3>"


def cut_string_after_char(char, string, many):
    return char.join(string.split(char)[0:many])