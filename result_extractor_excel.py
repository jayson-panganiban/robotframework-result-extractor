import os
import fnmatch
import openpyxl
import datetime
from lxml import etree
from openpyxl import Workbook
from itertools import izip, count

def save_test_result_to_excel_file():
    tc_name_list = []
    tc_status_list = []
    tc_error_list = []
    tc_tag_list = []
    xml_files = get_all_xml_files()
    for each_xml_file in xml_files:
        root = parse_xml_file(each_xml_file)
        for node in root.findall('.//test'):
            tc_name_attrib = node.attrib['name']
            tc_name_list.append(tc_name_attrib)
            tc_status_list.append(get_test_status_path(root, tc_name_attrib)[0].attrib['status'])
            tc_error_list.append(get_test_status_path(root, tc_name_attrib)[0].text)
            tc_tag_list.append(str(get_test_tags(root, tc_name_attrib)))

    date_stamp = '{:%Y-%m-%d-%H%M%S}'.format(datetime.datetime.now())
    result_file = 'test_result-' + date_stamp + '.xlsx'
    wb = Workbook()
    worksheet = wb.worksheets[0]
    worksheet['A1'] = 'Test Case Name'
    worksheet['B1'] = 'Test Case Status'
    worksheet['C1'] = 'Test Case Error'
    worksheet['D1'] = 'Test Case Tags'
    for i, name, status, error, tags in izip(count(), tc_name_list, tc_status_list, tc_error_list, tc_tag_list):
        worksheet['A' + str(i + 2)] = name
        worksheet['B' + str(i + 2)] = status
        worksheet['C' + str(i + 2)] = error
        worksheet['D' + str(i + 2)] = tags
    wb.save(filename=result_file)

def get_test_status_path(root, tc_name_attrib):
    if "'" in tc_name_attrib:
        tc_name_quoted = '"%s"' % tc_name_attrib
        return root.xpath(".//test[@name=" + tc_name_quoted + "]/status")
    else:
        return root.xpath(".//test[@name='" + tc_name_attrib + "']/status")

def get_test_tags(root, tc_name_attrib):
    if "'" in tc_name_attrib:
        tc_name_quoted = '"%s"' % tc_name_attrib
        return root.xpath(".//test[@name=" + tc_name_quoted + "]/tags/tag/text()")
    else:
        return root.xpath(".//test[@name='" + tc_name_attrib + "']/tags/tag/text()")

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
    save_test_result_to_excel_file()
