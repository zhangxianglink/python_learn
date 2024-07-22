import streamlit as st
import json
import os
import re

# 设置页面配置
st.set_page_config(layout="wide")


# 加载数据
def load_data(file):
    data = json.load(file)
    return data


# 保存标注结果
def save_results(data, output_file):
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


# 初始化状态
if 'data' not in st.session_state:
    st.session_state.data_loaded = False

# 文件选择
st.write("选择标注数据文件和保存文件的位置")
input_file = st.file_uploader("选择标注数据文件", type=["json"])
output_dir = st.text_input("输入保存文件的目录", value="C:\\Users\\admin\\Desktop\\profile")

if input_file and output_dir:
    if not st.session_state.data_loaded:
        output_filename = input_file.name.replace('.json', '_marked.json')
        input_data = load_data(input_file)

        output_file_path = os.path.join(output_dir, output_filename)

        if os.path.exists(output_file_path):
            with open(output_file_path, 'r', encoding='utf-8') as f:
                output_data = json.load(f)
        else:
            output_data = []

        current_index = len(output_data)

        st.session_state.data = input_data
        st.session_state.current_index = current_index
        st.session_state.marked_data = output_data
        st.session_state.output_file_path = output_file_path
        st.session_state.data_loaded = True

if 'data' in st.session_state:
    # 显示标注进度
    total_records = len(st.session_state.data)
    current_index = st.session_state.current_index
    st.write(f"标注进度: {current_index}/{total_records}")

    # 将删除记录和保留标注结果按钮放在顶部，并排显示
    col_top1, col_top2, col_top3 = st.columns([1, 1, 1])
    with col_top1:
        if st.button('删除当前记录', key='delete_record'):
            del st.session_state.data[st.session_state.current_index]
            st.experimental_rerun()
    with col_top2:
        if st.button('保留标注结果', key='keep_marks'):
            st.session_state.marked_data.append(st.session_state.data[st.session_state.current_index])
            st.session_state.current_index += 1
            st.experimental_rerun()
    with col_top3:
        if st.button('中途保存', key='save_partial'):
            save_results(st.session_state.marked_data, st.session_state.output_file_path)
            st.write(f"当前标注结果已保存到 {st.session_state.output_file_path}")

    # 显示当前记录
    if st.session_state.current_index < total_records:
        current_record = st.session_state.data[st.session_state.current_index]

        col1, col2 = st.columns([1, 1])  # 分成两等宽的列

        with col1:
            st.write("**原文**:")
            info_html = current_record['input'].replace('\n', '<br>')  # 将换行符替换为<br>

            st.markdown(
                f'<div style="height: calc(100vh - 150px); overflow-y: scroll; border: 1px solid #ccc; padding: 10px;">{info_html}</div>',
                unsafe_allow_html=True
            )  # 将换行符显示为换行，并设置滚动条

        with col2:
            st.write("**标注信息**:")
            output_data = json.loads(current_record['output'])
            for i, mark in enumerate(output_data):
                st.write(f"**标注 {i + 1}**:")

                # 使标注信息可编辑
                mark['标题'] = st.text_input(f"标题 {i + 1}", value=mark['标题'], key=f"title_{i}")
                mark['结果'] = st.selectbox(f"结果 {i + 1}", ['是', '否'], index=0 if mark['结果'] == '是' else 1,
                                          key=f"result_{i}")
                mark['编号'] = st.number_input(f"编号 {i + 1}", value=mark['编号'], key=f"number_{i}")
                mark['原文摘要'] = st.text_area(f"原文摘要 {i + 1}", value=mark['原文摘要'], key=f"summary_{i}")
                mark['解释'] = st.text_area(f"解释 {i + 1}", value=mark['解释'], key=f"explanation_{i}")

                if st.button(f'删除标注 {i + 1}', key=f'delete_mark_{i}'):
                    output_data.pop(i)
                    current_record['output'] = json.dumps(output_data, ensure_ascii=False, indent=4)
                    st.experimental_rerun()

            # 更新修改后的标注信息
            current_record['output'] = json.dumps(output_data, ensure_ascii=False, indent=4)

        # JavaScript for keyboard shortcuts
        custom_js = """
        <script>
        document.addEventListener('keydown', function(event) {
            if (event.key === 'Enter') {
                document.getElementById('keep_marks').click();
            } else if (event.key === 'Delete') {
                document.getElementById('delete_record').click();
            } else if (event.key >= '1' && event.key <= '9') {
                var buttonId = 'delete_mark_' + (parseInt(event.key) - 1);
                var button = document.getElementById(buttonId);
                if (button) {
                    button.click();
                }
            }
        });
        </script>
        """

        st.markdown(custom_js, unsafe_allow_html=True)

    else:
        st.write("所有记录已标注完毕！")
        if st.button('保存结果', key='save_results'):
            save_results(st.session_state.marked_data, st.session_state.output_file_path)
            st.write(f"标注结果已保存到 {st.session_state.output_file_path}")
