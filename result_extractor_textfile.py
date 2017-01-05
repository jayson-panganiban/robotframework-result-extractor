import os
import fnmatch
import datetime
from lxml import etree

def save_test_result_to_text_file():
    tc_name_list = []
    tc_status_list = []
    tc_error_list = []
    xml_files = get_all_xml_files()
    for each_xml_file in xml_files:
        root = parse_xml_file(each_xml_file)
        for node in root.findall('.//test'):
            tc_name_attrib = node.attrib['name']
            tc_name_list.append(tc_name_attrib)
            tc_status_list.append(get_test_status_path(root, tc_name_attrib)[0].attrib['status'])
            tc_error_list.append(get_test_status_path(root, tc_name_attrib)[0].text)

    date_stamp = '{:%Y-%m-%d-%H%M%S}'.format(datetime.datetime.now())
    test_file_result = "test_result.txt" + "-" + str(date_stamp) + ".txt"
    with open(test_file_result, "a") as output_file:
        for name, status, error in zip(tc_name_list, tc_status_list, tc_error_list):
            output_file.write(name + "\t" + status + "\t" + error.encode('utf-8') + "\n")

def get_test_status_path(root, tc_name_attrib):
    if "'" in tc_name_attrib:
        tc_name_quoted = '"%s"' % tc_name_attrib
        return root.xpath(".//test[@name=" + tc_name_quoted + "]/status")
    else:
        return root.xpath(".//test[@name='" + tc_name_attrib + "']/status")

def parse_xml_file(xml_file):
    tree = etree.parse(xml_file)
    return tree.getroot()

def get_all_xml_files():
    xml_files = []
    for root, dirnames, filenames in os.walk('.'):
        for filename in fnmatch.filter(filenames, '*.xml'):
            xml_files.append(os.path.join(root, filename))
    return xml_files

if __name__ == '__main__':
    save_test_result_to_text_file()
