import sys
import os
import fnmatch
import openpyxl
from lxml import etree

def save_test_result_to_excel_file(master_excel_file):
    tc_name_list = []
    tc_status_list = []
    tc_error_list = []
    wb = openpyxl.load_workbook(master_excel_file)
    created_sheet = wb.create_sheet()
    xml_files = get_all_xml_files()
    for each_xml_file in xml_files:
        root = parse_xml_file(each_xml_file)
        for node in root.findall('.//test'):
            tc_name_attrib = node.attrib['name']
            tc_status_value = get_test_status_path(root, tc_name_attrib)[0].attrib['status']
            tc_name_list.append(tc_name_attrib)
            tc_status_list.append(tc_status_value)
            tc_error_list.append(tc_error_value)            
    range_length = len(tc_name_list)
    for i in range(1, int(range_length) + 1):
        created_sheet['A' + str(i)] = tc_name_list[i - 1]
        created_sheet['B' + str(i)] = tc_status_list[i - 1]
        created_sheet['C' + str(i)] = tc_error_list[i - 1]
    wb.save(master_excel_file)

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
    save_test_result_to_excel_file(sys.argv[1])
