import streamlit as st
import pandas as pd
import json

# 设置页面标题
st.title('Excel 数据展示')

# 上传文件
uploaded_file = st.file_uploader("选择一个 Excel 文件", type=['xlsx'])

if uploaded_file:
    # 读取 Excel 文件
    df = pd.read_excel(uploaded_file)

    # 检查 Excel 文件是否至少有两列
    if df.shape[1] < 2:
        st.error("Excel 文件需要至少两列数据。")
    else:
        # 提取第二列数据，假设已经是 JSON 格式
        second_column_data = df.iloc[:, 0].tolist()

        # 初始化状态
        if 'index' not in st.session_state:
            st.session_state.index = 0

        # 显示当前行的 JSON 数据
        current_json_str = second_column_data[st.session_state.index]
        try:
            current_json = json.loads(current_json_str)
            st.json(current_json)
        except json.JSONDecodeError:
            st.error("当前行的内容不是有效的 JSON 格式。")

        # 展示当前行数和总行数
        total_rows = len(second_column_data)
        st.write(f"当前行数: {st.session_state.index + 1} / 总行数: {total_rows}")

        # 定义按钮点击行为
        prev_disabled = st.session_state.index == 0
        next_disabled = st.session_state.index == total_rows - 1

        prev_clicked = st.button('上一行', disabled=prev_disabled, key='prev')
        next_clicked = st.button('下一行', disabled=next_disabled, key='next')

        if prev_clicked and not prev_disabled:
            st.session_state.index = max(st.session_state.index - 1, 0)
            st.experimental_rerun()  # 重新运行以更新界面

        if next_clicked and not next_disabled:
            st.session_state.index = min(st.session_state.index + 1, total_rows - 1)
            st.experimental_rerun()  # 重新运行以更新界面

        # 添加文本框输入指定行数并切换页面
        row_input = st.text_input("输入行数并按回车跳转", "", key='row_input')
        if row_input:
            try:
                # 将输入的行数转换为整数
                row_num = int(row_input) - 1  # 用户输入是从 1 开始的
                if 0 <= row_num < total_rows:
                    st.session_state.index = row_num

                    # 更新显示行数据和行数，不使用 st.experimental_rerun()
                    current_json_str = second_column_data[st.session_state.index]
                    try:
                        current_json = json.loads(current_json_str)
                        st.json(current_json)
                    except json.JSONDecodeError:
                        st.error("当前行的内容不是有效的 JSON 格式。")
                    st.write(f"当前行数: {st.session_state.index + 1} / 总行数: {total_rows}")

                else:
                    st.error(f"行数必须在 1 和 {total_rows} 之间。")
            except ValueError:
                st.error("请输入有效的数字。")
