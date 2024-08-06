import streamlit as st
import json
import os
import re

# 设置页面配置
st.set_page_config(layout="wide")

# 预定义选项及注解
titles_with_numbers = {
    "欺骗不收费": 1,
    "不提资费": 2,
    "强调消费不变": 3,
    "告知错误的试用政策": 4,
    "强调套餐不变": 5,
    "误导免费": 6,
    "利用赠送活动误导": 7,
    "强调试用期免费": 8,
    "干扰资费": 9,
    "营销文字游戏话术": 10,
    "误导在套餐": 11,
    "没有以上任何问题": 12
}

annotations = {
    "欺骗不收费": "您不需要付费/没有任何收费",
    "不提资费": "利用网络提速/改善信号等借口",
    "强调消费不变": "每月加X元，不增加任何费用/消费不改变/还是以前的月租、月费/每月还是XX元的消费",
    "告知错误的试用政策": "前X个月您免费用，到期想继续用，联系我们，才会收每月X元",
    "强调套餐不变": "每月加X元，您套餐不改变/用的还是XX套餐/还是原来的套餐",
    "误导免费": "每月多加X元，都是赠送的/免费的/给您体验的/试用的",
    "利用赠送活动误导": "每月加X元，但是又赠送您X元直接抵扣了",
    "强调试用期免费": "每月多加X元，但是费用我们会减免",
    "干扰资费": "每月加X元您直接用，您正常用/您放心用/您安心用",
    "营销文字游戏话术": "您可以享受/回馈一个每月多加X元的权益/会员/礼包/福利/流量/语音",
    "误导在套餐": "每月加X元，都在您现在的XX元消费/XX元套餐以内的",
    "没有以上任何问题": "客服营销很规范。"
}

titles = [f"{title}（{annotation}）" for title, annotation in annotations.items()]
numbers_to_titles = {v: k for k, v in titles_with_numbers.items()}

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
#output_dir = st.text_input("输入保存文件的目录", value="")
output_dir = st.text_input("输入保存文件的目录", value="D:\\data\\convert16")

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

            # 高亮原文摘要
            output_data = current_record['output']
            if isinstance(output_data, str):
                output_data = json.loads(output_data)  # 如果是字符串，则将其加载为JSON

            # 展平嵌套列表
            flat_output_data = []
            for sublist in output_data:
                if isinstance(sublist, list):
                    flat_output_data.extend(sublist)
                else:
                    flat_output_data.append(sublist)

            for mark in flat_output_data:
                if "原文摘要" in mark and isinstance(mark["原文摘要"], str):  # 确保摘要存在且是字符串
                    pattern = re.escape(mark["原文摘要"])
                    replacement = f'<span style="background-color: yellow;">{mark["原文摘要"]}</span>'
                    info_html = re.sub(pattern, replacement, info_html)
                else:
                    st.write(f"原文摘要不是字符串或不存在：{mark}")

            st.markdown(
                f'<div style="height: calc(100vh - 150px); overflow-y: scroll; border: 1px solid #ccc; padding: 10px;">{info_html}</div>',
                unsafe_allow_html=True
            )  # 将换行符显示为换行，并设置滚动条

        with col2:
            st.write("**标注信息**:")
            for i, mark in enumerate(flat_output_data):
                st.write(f"**标注 {i + 1}**:")

                # 使用下拉菜单选择标题，并更新编号
                if mark['标题'] not in titles_with_numbers:
                    mark['标题'] = numbers_to_titles.get(mark['编号'], mark['标题'])

                annotated_titles = [f"{title}（{annotations[title]}）" for title in titles_with_numbers.keys()]
                selected_title = st.selectbox(f"标题 {i + 1}", annotated_titles, index=annotated_titles.index(f"{mark['标题']}（{annotations[mark['标题']]}）"), key=f"title_{i}")
                mark['标题'] = selected_title.split('（')[0]
                mark['编号'] = titles_with_numbers[mark['标题']]  # 根据标题更新编号
                st.write(f"编号: {mark['编号']}")  # 显示编号
                mark['结果'] = st.selectbox(f"结果 {i + 1}", ['是', '否'], index=0 if mark['结果'] == '是' else 1, key=f"result_{i}")
                mark['原文摘要'] = st.text_area(f"原文摘要 {i + 1}", value=mark.get('原文摘要', ''), key=f"summary_{i}")  # 如果不存在，则默认为空字符串
                mark['解释'] = st.text_area(f"解释 {i + 1}", value=mark.get('解释', ''), key=f"explanation_{i}")  # 如果不存在，则默认为空字符串

                if st.button(f'删除标注 {i + 1}', key=f'delete_mark_{i}'):
                    flat_output_data.pop(i)
                    current_record['output'] = flat_output_data  # 无需将其转换为JSON字符串
                    st.experimental_rerun()

            # 新增标注按钮
            if st.button('新增标注'):
                new_mark = {
                    '标题': titles[0].split('（')[0],
                    '编号': titles_with_numbers[titles[0].split('（')[0]],
                    '结果': '是',
                    '原文摘要': '',
                    '解释': ''
                }
                flat_output_data.append(new_mark)
                current_record['output'] = flat_output_data  # 无需将其转换为JSON字符串
                st.experimental_rerun()

            # 更新修改后的标注信息
            current_record['output'] = flat_output_data  # 无需将其转换为JSON字符串

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
