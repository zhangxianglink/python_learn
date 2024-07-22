import streamlit as st
import json
import os
import re

# 设置页面配置
st.set_page_config(layout="wide")

# 预定义选项及注解
titles_with_numbers = {
    "客户表示流量够用": 1,
    "客户资费敏感，表示套餐太贵优惠力度小": 2,
    "客户表示可选会员类型少，客户表示没有想要的会员": 3,
    "客户表示套餐流量太少": 4,
    "客户表示后续退订麻烦": 5,
    "客户表示权益领取麻烦": 6,
    "客户询问有没有其他产品可以办理": 7,
    "客户表示之前已经参加过活动了": 8,
    "客户表示办理过但是退订了": 9,
    "需要办理的宽带业务没有资源": 10,
    "客户表示准备转网，客户表示准备销户，客户表示办理了其他运营商卡号": 11,
    "客户表示自行去办理": 12,
    "客户表示害怕乱扣费": 13,
    "客户表示网络不好信号不好": 14,
    "客户表示电话营销骚扰太频繁反感，客户表示接到多次推销不想办": 15,
    "客户表示不信任联通、客户表示不相信电话营销": 16,
    "客户表示暂不考虑换套餐": 17,
    "无理由拒绝推销": 18,
    "老人或小孩接听": 19,
    "客户最终没有进行回复短信，如无明确表述回复了视为没有回复": 20,
    "当前不方便接电话，当前忙": 21,
    "客户对营销的产品比较感兴趣：客户对营销产品感兴趣咨询了一些问题": 22,
    "礼貌友好型客户：能进行良好沟通，多轮对话": 23,
    "简洁直接型：不拖泥带水，要或者不要都很爽快": 24,
    "犹豫纠结型：对是否办理业务很犹豫不决": 25,
    "暴躁易怒型：说脏话，骂人脾气暴躁": 26
}

annotations = {
    "客户表示流量够用": 1,
    "客户资费敏感，表示套餐太贵优惠力度小": 2,
    "客户表示可选会员类型少，客户表示没有想要的会员": 3,
    "客户表示套餐流量太少": 4,
    "客户表示后续退订麻烦": 5,
    "客户表示权益领取麻烦": 6,
    "客户询问有没有其他产品可以办理": 7,
    "客户表示之前已经参加过活动了": 8,
    "客户表示办理过但是退订了": 9,
    "需要办理的宽带业务没有资源": 10,
    "客户表示准备转网，客户表示准备销户，客户表示办理了其他运营商卡号": 11,
    "客户表示自行去办理": 12,
    "客户表示害怕乱扣费": 13,
    "客户表示网络不好信号不好": 14,
    "客户表示电话营销骚扰太频繁反感，客户表示接到多次推销不想办": 15,
    "客户表示不信任联通、客户表示不相信电话营销": 16,
    "客户表示暂不考虑换套餐": 17,
    "无理由拒绝推销": 18,
    "老人或小孩接听": 19,
    "客户最终没有进行回复短信，如无明确表述回复了视为没有回复": 20,
    "当前不方便接电话，当前忙": 21,
    "客户对营销的产品比较感兴趣：客户对营销产品感兴趣咨询了一些问题": 22,
    "礼貌友好型客户：能进行良好沟通，多轮对话": 23,
    "简洁直接型：不拖泥带水，要或者不要都很爽快": 24,
    "犹豫纠结型：对是否办理业务很犹豫不决": 25,
    "暴躁易怒型：说脏话，骂人脾气暴躁": 26
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
output_dir = st.text_input("输入保存文件的目录", value="C:\\Users\\admin\\Desktop\\profile\\half1")

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
