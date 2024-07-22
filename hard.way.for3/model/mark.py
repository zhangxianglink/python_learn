import streamlit as st
import json
import os
import re

# 设置页面配置
st.set_page_config(layout="wide")

# 预定义选项及注解
titles_with_numbers = {
    "正确介绍套餐资费": 1,
    "正确介绍套餐内容": 2,
    "客户询问套餐资费": 3,
    "客服正确回答资费问题": 4,
    "客户是否同意订购": 5,
}

annotations = {
    "正确介绍套餐资费": 1,
    "正确介绍套餐内容": 2,
    "客户询问套餐资费": 3,
    "客服正确回答资费问题": 4,
    "客户是否同意订购": 5,
}

# 子选项
subtitles = {
    1: {
        "1.1【未补救】坐席用欺骗方式讲述资费（您每月不需要加XX元、别人单独申请需要加XX元您直接用之类）": 1.1,
        "1.2【已补救】坐席用欺骗方式讲述资费（您每月不需要加XX元、别人单独申请需要加XX元您直接用之类）": 1.2,
        "1.3用户全文未同意订购坐席全文未主动介绍过资费": 1.3,
        "1.4营销两个产品，但是全文只主动介绍一个产品资费。在用户同意后二次确认中第二个产品一句话带过，用户未发觉直接同意了": 1.4,
        "1.5坐席先未主动告知资费，用户同意后，二次确认时资费一句带过": 1.5,
        "1.6【未补救】坐席主动介绍了资费，但是采用诱导话术，强调消费没变（每个月多加X元但消费不改变/还和以前一样之类/还是正常用": 1.6,
        "1.7【已补救】坐席主动介绍了资费，但是采用诱导话术，强调消费没变（每个月多加X元但消费不改变/还和以前一样之类/还是正常用）": 1.7,
        "1.8【未补救】坐席主动介绍了资费，但是玩文字游戏，让用户没理解是在告知资费（您可以享受一个每月多加X元的权益/会员/礼包/福利/流量/语音）": 1.8,
        "1.9【已补救】坐席主动介绍了资费，但是玩文字游戏，让用户没理解这是告知资费（您可以享受一个每月多加X元的权益/会员/礼包/福利/流量/语音）": 1.9,
        "1.10利用客户对低消、赠费等产品政策不理解，告知资费但是实际不会收取（因为消费达到X元会赠送/每月会返还您X元话费，正好用于抵扣之类）": 1.10
    },
    3: {"占位符"},
    4: {
        "4.1【未补救】用户询问资费时，坐席用欺骗方式回答了资费（您每月不需要加XX元、别人单独申请需要加XX元您不要钱之类）": 4.1,
        "4.2【已补救】用户询问资费时，坐席用欺骗方式回答了资费（您每月不需要加XX元、别人单独申请需要加XX元您不要钱之类）": 4.2,
        "4.3【未补救】用户询问资费时，坐席直接回答不会收费": 4.3,
        "4.4【已补救】用户询问资费时，坐席直接回答不会收费": 4.4,
        "4.5【未补救】用户询问资费时，坐席用回答了资费，但是采用诱导话术，强调消费没变（每个月多加X元，但是您套餐不改变/消费不改变/还是那个套餐之类）": 4.5,
        "4.6【已补救】用户询问资费时，坐席用回答了资费，但是采用诱导话术，强调消费没变（每个月多加X元，但是您套餐不改变/消费不改变/还是那个套餐之类）": 4.6,
        "4.7【未补救】用户询问资费时，坐席回答了资费，但是完文字游戏，让用户关注不到资费内容（您可以享受一个每月多加X元的权益/会员/礼包/福利/流量/语音之类）": 4.7,
        "4.8【已补救】用户询问资费时，坐席回答了资费，但是完文字游戏，让用户关注不到资费内容（您可以享受一个每月多加X元的权益/会员/礼包/福利/流量/语音之类）": 4.8,
        "4.9【未补救】用户询问资费时，利用客户对低消、赠费等产品政策不理解，告知资费但是实际不会收取（因为消费达到X元会赠送/每月会返还您X元话费，正好用于抵扣之类）": 4.9,
        "4.10【已补救】用户询问资费时，利用客户对低消、赠费等产品政策不理解，告知资费但是实际不会收取（因为消费达到X元会赠送/每月会返还您X元话费，正好用于抵扣之类）": 4.10
    },
    5: {
        "5.1用户答复敷衍（嗯，哦，知道了，再说吧，好好好好好，行行行行，这类敷衍回答）": 5.1,
        "5.2用户多次拒绝（2次以上说不需要），坐席挽留后勉强同意": 5.2,
        "5.3用户全文未同意订购": 5.3,
        "5.4未主动介绍营销内容，强调来电是通知服务维系（例如网络优化、优惠活动延续等不涉及业务办理的事项），用户误认为不需要办理业务才同意": 5.4
    }
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
output_dir = st.text_input("输入保存文件的目录", value="C:\\Users\\admin\\Desktop")

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
        st.session_state.current_init = True
        st.session_state.page = {}

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
            st.session_state.current_init = True
            st.session_state.page = {}
            st.experimental_rerun()
    with col_top2:
        if st.button('保留标注结果', key='keep_marks'):
            st.session_state.marked_data.append(st.session_state.data[st.session_state.current_index])
            st.session_state.current_index += 1
            st.session_state.current_init = True
            st.session_state.page = {}
            st.experimental_rerun()
    with col_top3:
        if st.button('中途保存', key='save_partial'):
            save_results(st.session_state.marked_data, st.session_state.output_file_path)
            st.write(f"当前标注结果已保存到 {st.session_state.output_file_path}")

    # 显示当前记录
    if st.session_state.current_index < total_records:
        current_record = st.session_state.data[st.session_state.current_index]

        col1, col2 = st.columns([1, 1])  # 分成两等宽的列

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

        if (st.session_state.current_init):
            st.session_state.current_init = False
            for i, mark in enumerate(flat_output_data):
                st.session_state.page[f"summary_{mark['编号']}"] = mark.get('原文摘要')
                st.session_state.page[f"explanation_{mark['编号']}"] = mark.get('解释')
                st.session_state.page[f"subtitle_summary_{mark['编号']}"] = mark.get('子选项原文摘要')
                st.session_state.page[f"subtitle_explanation_{mark['编号']}"] = mark.get('子选项解释')


        with col1:
            st.write("**原文**:")
            info_html = current_record['input'].replace('\n', '<br>')  # 将换行符替换为<br>
            st.markdown(
                f'<div style="height: calc(100vh - 150px); overflow-y: scroll; border: 1px solid #ccc; padding: 10px;">{info_html}</div>',
                unsafe_allow_html=True
            )  # 将换行符显示为换行，并设置滚动条

        with col2:
            st.write("**标注信息**:")
            show_four = False
            for i, mark in enumerate(flat_output_data):
                with st.expander(f"**标注 {i + 1}**:"):
                    # 使用下拉菜单选择标题，并更新编号
                    if mark['标题'] not in titles_with_numbers:
                        mark['标题'] = numbers_to_titles.get(mark['编号'], mark['标题'])

                    annotated_titles = [f"{title}（{annotations[title]}）" for title in titles_with_numbers.keys()]
                    selected_title = st.selectbox(f"标题 {i + 1}", annotated_titles, index=annotated_titles.index(
                        f"{mark['标题']}（{annotations[mark['标题']]}）"), key=f"title_{i}")
                    mark['标题'] = selected_title.split('（')[0]
                    mark['编号'] = titles_with_numbers[mark['标题']]  # 根据标题更新编号
                    st.write(f"编号: {mark['编号']}")  # 显示编号

                    # 级联子选项
                    show_subtitle = False
                    if mark['编号'] in subtitles:
                        mark['结果'] = st.selectbox(f"结果 {i + 1}", ['是', '否'], index=0 if mark['结果'] == '是' else 1,
                                                  key=f"result_{i}")
                        if mark['编号'] in [1, 5]:
                            show_subtitle = mark['结果'] == '否'
                        elif mark['编号'] == 3:
                            show_four = mark['结果'] == '是'
                        else:
                            show_subtitle = (show_four and mark['结果'] == '否')

                    else:
                        mark['结果'] = st.selectbox(f"结果 {i + 1}", ['是', '否'], index=0 if mark['结果'] == '是' else 1,
                                                  key=f"result_{i}")

                    if show_subtitle:
                        subtitle_options = subtitles[mark['编号']]
                        subtitle = st.selectbox(f"子选项 {i + 1}", list(subtitle_options.keys()), key=f"subtitle_{i}")
                        mark['子选项'] = subtitle_options[subtitle]
                        mark['子选项原文摘要'] = st.text_area(f"子选项原文摘要 {i + 1}",value=st.session_state.page[f"subtitle_summary_{mark['编号']}"])  # 如果不存在，则默认为空字符串
                        mark['子选项解释'] = st.text_area(f"子选项解释 {i + 1}",value=st.session_state.page[f"subtitle_explanation_{mark['编号']}"])  # 如果不存在，则默认为空字符串
                    else:
                        mark.pop('子选项', None)
                        mark.pop('子选项原文摘要', None)
                        mark.pop('子选项解释', None)

                    mark['原文摘要'] = st.text_area(f"原文摘要 {i + 1}", value=st.session_state.page[f"summary_{mark['编号']}"])  # 如果不存在，则默认为空字符串
                    mark['解释'] = st.text_area(f"解释 {i + 1}",value=st.session_state.page[f"explanation_{mark['编号']}"])  # 如果不存在，则默认为空字符串

                    if st.button(f'删除标注 {i + 1}', key=f'delete_mark_{i}'):
                        flat_output_data.pop(i)
                        current_record['output'] = flat_output_data  # 无需将其转换为JSON字符串
                        st.session_state.page[f"summary_{mark['编号']}"] = ''
                        st.session_state.page[f"explanation_{mark['编号']}"] = ''
                        st.session_state.page[f"subtitle_summary_{mark['编号']}"] = ''
                        st.session_state.page[f"subtitle_explanation_{mark['编号']}"] = ''
                        st.session_state.current_init = True
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
