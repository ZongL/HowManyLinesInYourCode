import xml.etree.ElementTree as ET
import pandas as pd


def extract_tx_p_ports(arxml_file,SWC_name):
    tree = ET.parse(arxml_file)
    root = tree.getroot()

    def get_local_tag(tag):
        return tag.split('}')[-1] if '}' in tag else tag

    target_shortname = SWC_name
    p_port_names = []

    # 遍历所有 APPLICATION-SW-COMPONENT-TYPE 节点
    for app_sw_node in root.iter():
        if get_local_tag(app_sw_node.tag) != "APPLICATION-SW-COMPONENT-TYPE":
            continue

        # 在节点内查找 SHORT-NAME 和 PORTS
        found_shortname = None
        ports_node = None
        for child in app_sw_node:
            tag = get_local_tag(child.tag)
            if tag == "SHORT-NAME":
                found_shortname = child.text
            elif tag == "PORTS":
                ports_node = child

        # 如果找到目标组件
        if found_shortname == target_shortname and ports_node is not None:
            # 提取所有 P-PORT-PROTOTYPE 的 SHORT-NAME
            for port_node in ports_node:
                if get_local_tag(port_node.tag) != "P-PORT-PROTOTYPE":
                    continue
                for field in port_node:
                    if get_local_tag(field.tag) == "SHORT-NAME":
                        p_port_names.append(field.text)
                        break  # 找到后跳出循环
            break  # 假设只有一个目标组件，找到后提前退出
    # 打印结果
    # for name in p_port_names:
    #     print(name)
    return p_port_names

def get_group_name_and_value(file_path, search_value):
    """
    在指定的Excel文件中查找包含特定值的行，并返回该行所在组的组名以及该组指定列的值
    :param file_path: Excel文件路径
    :param search_value: 要查找的精确匹配值
    :return: (Excel行号, 组名, 第二列值)
    """
    # 读取Excel文件（假设没有标题行）
    df = pd.read_excel(file_path, sheet_name='Matrix', header=None)

    # 在第I列（索引8）中精确匹配搜索值
    target_column = 8
    mask = df[target_column].astype(str) == search_value
    matched_rows = df[mask]

    if not matched_rows.empty:
        # 获取第一个匹配行的索引（pandas中的0-based索引）
        row_idx = matched_rows.index[0]
        excel_row = row_idx + 1  # 转换为基于1的Excel行号

        # 查找组名（横向移到A列后向上查找）
        a_column = 0  # A列索引
        current_row = row_idx

        # 先横向移动到A列
        # 然后向上查找直到找到非空值
        while current_row >= 0:
            group_candidate = df.iloc[current_row, a_column]
            if pd.notna(group_candidate) and str(group_candidate).strip() != "":
                # 打印组所在的行的第一列元素
                target_value = df.iloc[current_row, 0]
                return excel_row, group_candidate, target_value
            current_row -= 1

        return excel_row, None, None
    else:
        return None, None, None


# 核心处理函数（复用逻辑）
def process_ports(port_names):
    """处理端口列表并返回结果DataFrame"""
    # 初始化DataFrame
    df = pd.DataFrame({'Search Value': port_names})

    # 为每个文件添加对应的列
    for file_path, prefix in file_list:
        df[f'{prefix}_'] = ''  # Group名称列
        df[f'{prefix}_Excel Position'] = ''  # 位置信息列

    # 遍历Excel文件进行搜索
    for file_path, prefix in file_list:
        print('正在处理....'+prefix)
        group_col = f'{prefix}_'
        position_col = f'{prefix}_Excel Position'

        # 遍历每个端口名称
        for index, search_value in enumerate(port_names):
            # 调用原有搜索函数
            excel_row, group_name, _ = get_group_name_and_value(file_path, search_value)

            # 填充数据
            if group_name:
                df.at[index, group_col] = group_name
                df.at[index, position_col] = f'第I列，第{excel_row}行'
            else:
                df.at[index, group_col] = ''
                df.at[index, position_col] = ''
    return df


if __name__ == "__main__":
    #找到arxml中的P-port
    arxml_file_path_bcm = "VDPR_20250313.arxml"  # 替换为实际的ARXML文件路径
    arxml_file_path_vcu = "VDP_VCU.arxml"  # 替换为实际的ARXML文件路径
    p_port_names_in_BCM = extract_tx_p_ports(arxml_file_path_bcm,'BCM_Tx')  # 替换为你的ARXML文件路径
    print(p_port_names_in_BCM[:5])
    #去除前缀
    p_port_names_in_BCM = [name[4:] if name.startswith("ASW_") else name for name in p_port_names_in_BCM]
    print(p_port_names_in_BCM[:5])
    print(len(p_port_names_in_BCM))

    '''found P-port in VCU'''
    p_port_names_in_VCU = extract_tx_p_ports(arxml_file_path_vcu,'VDP_VCU')  # 替换为你的ARXML文件路径
    print(p_port_names_in_VCU[:5])
    p_port_names_in_VCU = [name[4:] if name.startswith("ASW_") else name for name in p_port_names_in_VCU]
    print(p_port_names_in_VCU[:5])
    print(len(p_port_names_in_VCU))
    '''
    # 定义Excel文件路径
    file_path = 'VDPM-BDCANFD_Matrix_V1.4.1_20250121.xlsx'

    # 创建一个空的DataFrame，用于存储结果
    results = []

    # 遍历所有P-port，抓取所属的Group信息
    for search_value in p_port_names_in_BCM:
        excel_row, group_name, group_col_value = get_group_name_and_value(file_path, search_value)
        if group_name:
            # 如果找到，将结果添加到results列表中
            results.append([search_value, f"第I列，第{excel_row}行", group_name])
        else:
            # 如果未找到，也添加到results列表中，但group_name为空
            results.append([search_value, f"第I列，未找到", ""])

    # 将结果转换为DataFrame
    results_df = pd.DataFrame(results, columns=["Search Value", "Excel Position", "Group Name"])
    # 将结果保存到新的Excel文件中
    output_file_path = "BCM_VCU_signal.xlsx"
    results_df.to_excel(output_file_path, index=False)
    with pd.ExcelWriter(output_file_path) as writer:
        results_df.to_excel(writer, sheet_name="bcm_checkresult", index=False)
    print(f"结果已保存到文件：{output_file_path}")
    '''

    # 定义需要搜索的Excel文件及其对应的列名前缀
    file_list = [
        ('VDPM-BDCANFD_Matrix_V1.4.1_20250121.xlsx', 'BDCANFD'),
        ('VDPM-ADCAN_Matrix_V1.5_20150121.xlsx', 'ADCAN'),
        ('VDPM-CHCAN_Matrix_V1.1_20250120.xlsx', 'CHCAN'),
        ('VDPM-PTCAN_Matrix_V2.2_20250122.xlsx', 'PTCAN'),
        ('VDPM-VCCANFD_Matrix_V1.3_20250121.xlsx', 'VCCANFD')
    ]

    bcm_results = process_ports(p_port_names_in_BCM)  # BCM数据
    vcu_results = process_ports(p_port_names_in_VCU)  # VCU数据
    # 保存到Excel文件
    output_file_path = "BCM_VCU_signal.xlsx"
    with pd.ExcelWriter(output_file_path) as writer:
        bcm_results.to_excel(writer, sheet_name="bcm_checkresult", index=False)
        vcu_results.to_excel(writer, sheet_name="vcu_checkresult", index=False)
    print(f"结果已保存到文件：{output_file_path}")
