import pandas as pd

# 电滑门控制_PSD
# 电尾门控制_PTM
# 低压能量控制_LVM
# 被动安全控制_PSM
# 低压电源控制_LowPwrModeCtl
# 整车模式_VehMod

#df1 = pd.read_excel('滴滴VDP 通信矩阵问题.xlsx', sheet_name='Sheet1', header=None)  # 读取第一个文件的指定工作表
# 读取 Excel 文件
df1 = pd.read_excel('RT_ASWC_Interface_Description.xlsx', sheet_name='BCM_PTM', header=None)  # 读取第一个文件的指定工作表
df2 = pd.read_excel('VDPM-BDCANFD_Matrix_V1.4.1_20250121.xlsx', sheet_name='Matrix')  # 读取第二个文件的指定工作表
df3 = pd.read_excel('VDPM-CHCAN_Matrix_V1.1_20250120.xlsx', sheet_name='Matrix')  # 读取第二个文件的指定工作表
df4 = pd.read_excel('VDPM-PTCAN_Matrix_V2.2_20250122.xlsx', sheet_name='Matrix')  # 读取第二个文件的指定工作表
df5 = pd.read_excel('VDPM-VCCANFD_Matrix_V1.3_20250121.xlsx', sheet_name='Matrix')  # 读取第二个文件的指定工作表




# 提取第一个 DataFrame 的第 E 列的元素（Excel 中的 E 列对应索引 4）
elements_to_search = df1.iloc[:, 4].dropna().unique()

# 提取第一个 DataFrame 的第 B 列的元素（Excel 中的 E 列对应索引 1）
#elements_to_search = df1.iloc[:, 1].dropna().unique()
#
# # 检查每个元素是否在第二个 DataFrame 中存在
# results = {element: element in df2.values for element in elements_to_search}

# 将所有 DataFrame 的所有值转换为集合，提高查找效率
df2_values_set = set(df2.values.flatten())
df3_values_set = set(df3.values.flatten())
df4_values_set = set(df4.values.flatten())
df5_values_set = set(df5.values.flatten())
# 合并所有集合
combined_values_set = df2_values_set.union(df3_values_set, df4_values_set, df5_values_set)

# 检查每个元素是否在合并后的集合中存在
results = {element: element in combined_values_set for element in elements_to_search}

# 打印结果
for element, found in results.items():
    print(element)
    if not found:
        print(f"元素 '{element}' 是否找到: {found}")
