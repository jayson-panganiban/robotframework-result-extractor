import os
import fnmatch
import datetime
from lxml import etree

def save_test_result_to_text_file():
    tc_name_list = []
    tc_status_list = []
    tc_error_list = []
    tc_tag_list = []
    xml_files = get_all_xml_files()
    for each_xml_file in xml_files:
        context = etree.iterparse(each_xml_file, events=('end',))
        for event, elem in context:
            if elem.tag == 'test':
                tc_name_attrib = elem.attrib['name']
                tc_name_list.append(tc_name_attrib)
                tc_status_list.append(get_test_status_path(elem, tc_name_attrib)[0].attrib['status'])
                tc_error_list.append(get_test_status_path(elem, tc_name_attrib)[0].text)
                tc_tag_list.append(get_test_tags(elem, tc_name_attrib))
                elem.clear()
                while elem.getprevious() is not None:
                    del elem.getparent()[0]
        del context

    date_stamp = '{:%Y-%m-%d-%H%M%S}'.format(datetime.datetime.now())
    test_file_result = "test_result.txt" + "-" + str(date_stamp) + ".txt"
    with open(test_file_result, "a") as output_file:
        for name, status, error, tags in zip(tc_name_list, tc_status_list, tc_error_list, tc_tag_list):
            output_file.write(name + "\t" + status + "\t" + str(error) + "\t" + ', '.join(tags) + "\n")

def get_test_status_path(elem, tc_name_attrib):
    if "'" in tc_name_attrib:
        tc_name_quoted = '"%s"' % tc_name_attrib
        return elem.xpath("//test[@name=" + tc_name_quoted + "]/status")
    else:
        return elem.xpath("//test[@name='" + tc_name_attrib + "']/status")

def get_test_tags(elem, tc_name_attrib):
    if "'" in tc_name_attrib:
        tc_name_quoted = '"%s"' % tc_name_attrib
        return elem.xpath("//test[@name=" + tc_name_quoted + "]/tags/tag/text()")
    else:
        return elem.xpath("//test[@name='" + tc_name_attrib + "']/tags/tag/text()")

def get_all_xml_files():
    xml_files = []
    for root, dirnames, filenames in os.walk('.'):
        for filename in fnmatch.filter(filenames, '*.xml'):
            xml_files.append(os.path.join(root, filename))
    return xml_files

if __name__ == '__main__':
    save_test_result_to_text_file()
