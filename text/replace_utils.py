import re

lithuanian_character = "ąčęėįšųūžĄČĘĖĮŠŲŪŽ"
french_german_characters = "ÀàÂâÆæÇçÈèÉéÊêËëÎîÏïÔôŒœÙùÛûÜüÄäÖöß"


def remove_invalid_characters_in(string_list):
    valid_string_list = []
    for string in string_list:
        valid_string_list.append(remove_invalid_characters_from(string))
    return valid_string_list


def remove_invalid_characters_from(string):
    string = string.replace("\n", " ")
    string = string.replace("  ", " ")
    return re.sub(r'[^ \-–—0-9.,;:?!()a-zA-Z' + lithuanian_character + french_german_characters + ']', "", string)
