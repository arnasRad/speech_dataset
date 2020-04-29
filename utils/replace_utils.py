import re
from utils import file_utils as fu


def replace_in_file(input_file_path, pattern, string_replacement):
    text = fu.read_file(input_file_path)
    print("\tfound patterns: %s" % re.findall(pattern, text))
    return re.sub(pattern=pattern, repl=string_replacement, string=text)


def replace_and_rewrite_file(file_path, pattern, string_replacement):
    text = replace_in_file(file_path, pattern, string_replacement)
    fu.write_file(file_path, text)


def replace_aeneas_paragraph(paragraph):
    paragraph = paragraph.replace("\n", " ")
    paragraph = paragraph.replace("- ", "")
    paragraph = paragraph.replace("– ", "")
    paragraph = paragraph.replace(" - ", "")
    paragraph = paragraph.replace("- ", "")
    paragraph = paragraph.replace("— ", "")
    return re.sub(r'[^a-zA-Z0-9 _*.,;?!ąčęėįšųūžĄČĘĖĮŠŲŪŽÀàÂâÆæÇçÈèÉéÊêËëÎîÏïÔôŒœÙùÛûÜüÄäÖöß]', "", paragraph)