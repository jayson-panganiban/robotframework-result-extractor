import time, sys, os, fnmatch, datetime
from lxml import etree

def save_test_result_to_text_file():

    tc_name_list = []
    tc_status_list = []
    tc_error_list = []
    date_today = '{:%Y-%m-%d-%H%M%S}'.format(datetime.datetime.now())
    test_file_result = "test_result.txt" + "-" + str(date_today) + ".txt"
    new_file = open(test_file_result, "w")

    xml_files = get_all_xml_files()
    for each_xml_file in xml_files:
        root = parse_xml_file(each_xml_file)
        for node in root.findall('.//test'):
            tc_name_attrib = node.attrib['name']
            tc_status_value = get_test_status_path(root, tc_name_attrib)[0].attrib['status']
            if tc_status_value == 'FAIL':
                tc_error_value = get_test_status_path(root, tc_name_attrib)[0].text
                tc_status_value = 'FAIL (For Investigation)'
            else:
                tc_error_value = ""
            tc_name_list.append(tc_name_attrib)
            tc_status_list.append(tc_status_value)
            tc_error_list.append(tc_error_value)
            
    range_length = len(tc_name_list)
    with open(test_file_result, "a") as output_file:
        for i in range(1, int(range_length) + 1):
            output_file.write(tc_name_list[i - 1] + "\t" + tc_status_list[i - 1] + "\t" + tc_error_list[i - 1].encode('utf-8') + "\n")
    output_file.close()

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

    return traverse_thru_folders()

def retrieve_from_current_folder():

    xml_files = []
    files_in_dir = listdir(getcwd())
    for file_item in files_in_dir:
        if file_item.endswith(".xml"):
            xml_files.append(file_item)
    return xml_files

def traverse_thru_folders():

    xml_files = []
    for root, dirnames, filenames in os.walk('.'):
        for filename in fnmatch.filter(filenames, '*.xml'):
            xml_files.append(os.path.join(root, filename))
    return xml_files

if __name__ == '__main__':
    save_test_result_to_text_file()