
import xml.etree.ElementTree as ET
from xml.dom import minidom
import sys

# 定义命名空间配置
NS_CONFIG = {
    'xmlns': "http://autosar.org/schema/r4.0",
    'xsi': "http://www.w3.org/2001/XMLSchema-instance"
}


def format_xml(elem, level=0, indent="  "):
    """递归格式化XML元素保持缩进"""
    # 计算当前缩进
    current_indent = "\n" + level * indent
    # 子元素缩进
    child_indent = current_indent + indent

    # 处理元素内容
    if len(elem):
        # 如果有子元素
        if not elem.text or not elem.text.strip():
            elem.text = child_indent
        for child in elem:
            format_xml(child, level + 1, indent)
        # 处理最后一个子元素的尾部
        if not child.tail or not child.tail.strip():
            child.tail = current_indent
    else:
        # 空元素保持展开格式
        if not elem.text or not elem.text.strip():
            elem.text = ""
        elem.tail = current_indent


# def add_init_values(input_file, output_file):
#     try:
#         # 解析XML文件
#         tree = ET.parse(input_file)
#         root = tree.getroot()
#
#         # 配置命名空间
#         ET.register_namespace('', NS_CONFIG['xmlns'])
#         ET.register_namespace('xsi', NS_CONFIG['xsi'])
#
#         # 查找所有P-PORT-PROTOTYPE
#         for p_port in root.iterfind('.//{http://autosar.org/schema/r4.0}P-PORT-PROTOTYPE'):
#             # 定位通信规范
#             com_specs = p_port.find('./{http://autosar.org/schema/r4.0}PROVIDED-COM-SPECS')
#             if com_specs is None:
#                 continue
#
#             sender_com_spec = com_specs.find('./{http://autosar.org/schema/r4.0}NONQUEUED-SENDER-COM-SPEC')
#             if sender_com_spec is None:
#                 continue
#
#             # 跳过已有初始化值的
#             if sender_com_spec.find('./{http://autosar.org/schema/r4.0}INIT-VALUE') is not None:
#                 continue
#
#             # 创建初始化值节点
#             init_value = ET.SubElement(sender_com_spec, 'INIT-VALUE')
#             num_spec = ET.SubElement(init_value, 'NUMERICAL-VALUE-SPECIFICATION')
#             ET.SubElement(num_spec, 'VALUE').text = '0'
#
#             # 保持元素顺序
#             e2e_protection = sender_com_spec.find('./{http://autosar.org/schema/r4.0}USES-END-TO-END-PROTECTION')
#             if e2e_protection is not None:
#                 # 复制缩进格式
#                 init_value.tail = e2e_protection.tail
#                 sender_com_spec.remove(init_value)
#                 insert_pos = list(sender_com_spec).index(e2e_protection) + 1
#                 sender_com_spec.insert(insert_pos, init_value)
#
#         # 格式化整个XML树
#         format_xml(root)
#
#         # 生成XML字符串
#         xml_str = ET.tostring(root, encoding='utf-8', method='xml')
#
#         # 使用minidom进行最终格式化
#         dom = minidom.parseString(xml_str)
#         pretty_xml = dom.toprettyxml(indent="  ", encoding='utf-8').decode('utf-8')
#
#         # 清理多余空行
#         pretty_xml = '\n'.join([line for line in pretty_xml.split('\n') if line.strip()])
#
#         # 保留原文件声明格式
#         header_line = '<?xml version="1.0" encoding="utf-8"?>'
#         if pretty_xml.startswith(header_line):
#             pretty_xml = pretty_xml.replace(
#                 header_line,
#                 '<?xml version="1.0" encoding="utf-8"?>\n',
#                 1
#             )
#
#         # 写入文件
#         with open(output_file, 'w', encoding='utf-8') as f:
#             f.write(pretty_xml)
#
#         print(f"成功处理并保存到: {output_file}")
#
#     except Exception as e:
#         print(f"处理失败: {str(e)}")
#         sys.exit(1)
#---------------------------------------------------------------无法解决多个comspce问题----------------


def add_init_values(input_file, output_file):
    try:
        # 解析XML文件
        tree = ET.parse(input_file)
        root = tree.getroot()

        # 配置命名空间
        ET.register_namespace('', NS_CONFIG['xmlns'])
        ET.register_namespace('xsi', NS_CONFIG['xsi'])

        # 查找所有P-PORT-PROTOTYPE
        for p_port in root.iterfind('.//{http://autosar.org/schema/r4.0}P-PORT-PROTOTYPE'):
            # 定位通信规范
            com_specs = p_port.find('./{http://autosar.org/schema/r4.0}PROVIDED-COM-SPECS')
            if com_specs is None:
                continue

            # 修改点：查找所有NONQUEUED-SENDER-COM-SPEC -------------------------------------------------
            for sender_com_spec in com_specs.findall('./{http://autosar.org/schema/r4.0}NONQUEUED-SENDER-COM-SPEC'):
                # 跳过已有初始化值的
                if sender_com_spec.find('./{http://autosar.org/schema/r4.0}INIT-VALUE') is not None:
                    continue

                # 创建初始化值节点
                init_value = ET.SubElement(sender_com_spec, 'INIT-VALUE')
                num_spec = ET.SubElement(init_value, 'NUMERICAL-VALUE-SPECIFICATION')
                ET.SubElement(num_spec, 'VALUE').text = '0'

                # 保持元素顺序
                e2e_protection = sender_com_spec.find('./{http://autosar.org/schema/r4.0}USES-END-TO-END-PROTECTION')
                if e2e_protection is not None:
                    # 复制缩进格式
                    init_value.tail = e2e_protection.tail
                    sender_com_spec.remove(init_value)
                    insert_pos = list(sender_com_spec).index(e2e_protection) + 1
                    sender_com_spec.insert(insert_pos, init_value)
            # 修改结束 ----------------------------------------------------------------------------------

        # 以下保持原有代码不变
        # 格式化整个XML树
        format_xml(root)

        # 生成XML字符串
        xml_str = ET.tostring(root, encoding='utf-8', method='xml')

        # 使用minidom进行最终格式化
        dom = minidom.parseString(xml_str)
        pretty_xml = dom.toprettyxml(indent="  ", encoding='utf-8').decode('utf-8')

        # 清理多余空行
        pretty_xml = '\n'.join([line for line in pretty_xml.split('\n') if line.strip()])

        # 保留原文件声明格式
        header_line = '<?xml version="1.0" encoding="utf-8"?>'
        if pretty_xml.startswith(header_line):
            pretty_xml = pretty_xml.replace(
                header_line,
                '<?xml version="1.0" encoding="utf-8"?>\n',
                1
            )

        # 写入文件
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(pretty_xml)

        print(f"成功处理并保存到: {output_file}")

    except Exception as e:
        print(f"处理失败: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    input_path = "VDPR_todo.arxml"
    output_path = "VDPR_done.arxml"
    add_init_values(input_path, output_path)
