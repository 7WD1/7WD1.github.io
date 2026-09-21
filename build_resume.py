# -*- coding: utf-8 -*-
"""重建姜文栋简历：论文题目中英对照 + 电话改为大陆号码，版式复刻原 PDF。"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import Color
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFontFamily
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, HRFlowable,
                                Table, TableStyle, KeepTogether, CondPageBreak)

FONT_DIR = r'C:/Windows/Fonts'
pdfmetrics.registerFont(TTFont('KaiTi', FONT_DIR + '/simkai.ttf'))
pdfmetrics.registerFont(TTFont('TNR', FONT_DIR + '/times.ttf'))
pdfmetrics.registerFont(TTFont('TNR-I', FONT_DIR + '/timesi.ttf'))
registerFontFamily('TNR', normal='TNR', bold='TNR', italic='TNR-I', boldItalic='TNR')

GRAY = Color(0.8275, 0.8275, 0.8275)
CW = A4[0] - 57 - 57  # content width ~481.3

def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

def lat(s, italic=False):
    t = '<font name="TNR">' + esc(s) + '</font>'
    return '<i>' + t + '</i>' if italic else t

def is_cjk(ch):
    return ord(ch) > 0x2E80 or ch == '\u2014'  # 全角破折号归楷体

def mix(s):
    """中文用楷体（基础字体），西文自动切换 Times New Roman。"""
    runs = []
    cur, cur_cjk = [], None
    for ch in s:
        c = is_cjk(ch)
        if cur_cjk is None:
            cur_cjk, cur = c, [ch]
        elif c == cur_cjk:
            cur.append(ch)
        else:
            runs.append((cur_cjk, ''.join(cur)))
            cur, cur_cjk = [ch], c
    if cur:
        runs.append((cur_cjk, ''.join(cur)))
    return ''.join(esc(seg) if c else lat(seg) for c, seg in runs)

S = {
    'name': ParagraphStyle('name', fontName='KaiTi', fontSize=18, leading=24, alignment=TA_CENTER),
    'contact': ParagraphStyle('contact', fontName='KaiTi', fontSize=10, leading=15, alignment=TA_CENTER),
    'h1cn': ParagraphStyle('h1cn', fontName='KaiTi', fontSize=13, leading=18, spaceBefore=7),
    'h1en': ParagraphStyle('h1en', fontName='TNR', fontSize=13, leading=18, spaceBefore=7),
    'h2': ParagraphStyle('h2', fontName='KaiTi', fontSize=11, leading=16, spaceBefore=2, spaceAfter=3),
    'body': ParagraphStyle('body', fontName='KaiTi', fontSize=10, leading=16.6, alignment=TA_LEFT, wordWrap='CJK'),
    'date': ParagraphStyle('date', fontName='TNR', fontSize=10, leading=16.6, alignment=TA_RIGHT),
    'bullet': ParagraphStyle('bullet', fontName='KaiTi', fontSize=10, leading=16.5, alignment=TA_LEFT,
                             wordWrap='CJK', leftIndent=7, bulletIndent=0, bulletFontName='TNR'),
    'paper': ParagraphStyle('paper', fontName='KaiTi', fontSize=10, leading=14.2, alignment=TA_JUSTIFY,
                            leftIndent=14, firstLineIndent=-14, spaceBefore=3),
    'cntitle': ParagraphStyle('cntitle', fontName='KaiTi', fontSize=9.5, leading=14, alignment=TA_LEFT,
                              wordWrap='CJK', leftIndent=14, spaceAfter=2),
    'pdesc': ParagraphStyle('pdesc', fontName='KaiTi', fontSize=9.5, leading=14, alignment=TA_LEFT,
                            wordWrap='CJK', leftIndent=7, spaceAfter=1.5),
    'note': ParagraphStyle('note', fontName='KaiTi', fontSize=9.3, leading=12, wordWrap='CJK', spaceBefore=3),
    'jp': ParagraphStyle('jp', fontName='KaiTi', fontSize=11, leading=16, spaceBefore=2, spaceAfter=1),
}

def rule():
    return HRFlowable(width='100%', thickness=0.7, color=GRAY, spaceBefore=2, spaceAfter=2.5)

def school_row(school, date):
    t = Table([[Paragraph(mix(school), S['body']), Paragraph(esc(date), S['date'])]],
              colWidths=[CW - 101, 101])
    t.setStyle(TableStyle([
        ('LEFTPADDING', (0, 0), (-1, -1), 0), ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 0), ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        ('VALIGN', (0, 0), (-1, -1), 'BOTTOM'),
    ]))
    return t

contact = '邮箱：wendongjiang@ieee.org ｜ 电话：+86 18868626534'

edu = [
    ('台湾淡江大学', '2023.09 - 2026.06', [
        '资讯工程学系（工学博士），对应大陆专业：计算机科学与技术',
        '指导教授：张志勇 特聘教授',
        '研究方向：可解释机器学习及其在智慧城市的应用',
        '毕业论文：《从异常识别到因果解释：弱监督视频异常检测方法研究》',
    ]),
    ('台湾铭传大学', '2021.09 - 2023.06', [
        '资讯工程学系（工学硕士），对应大陆专业：计算机科学与技术',
        '指导教授：李御玺教授、颜秀珍教授',
        '研究方向：可解释机器学习、数据挖掘',
        '毕业论文：《一个基于LIME的新可解释机器学习及其评估方法之研究》',
    ]),
    ('台湾龙华科技大学', '2017.06 - 2021.06', [
        '多媒体与游戏科学发展学系（工学学士），对应大陆专业：数字媒体技术',
        '指导教授：梁志雄 助理教授',
        '研究方向：人机交互',
        '毕业作品：《水管英雄—一个基于EyeTracking技术用于渐冻者患者人机互动游戏》',
        'DemoLink：https://www.youtube.com/watch?v=chWE9t0sKaE',
    ]),
]

papers = [
    dict(pre='Wen-Dong Jiang, Chih-Yung Chang, Show-Jane Yen, Shih-Jung Wu, and Diptendu Sinha Roy, '
             '\u201cRealExp: Decoupling Correlation Bias in Shapley Values for Faithful Model Interpretations,\u201d ',
         it='Information Processing & Management (IPM)',
         post=', Vol. 62, No. 4, Pp. 104153, July 2025. (SCI Impact Factor: 7.5; '
              'INFORMATION SCIENCE & LIBRARY SCIENCE: 7/161=4%, ',
         tail='中科院1区Top期刊，CCF-B，第一作者).',
         cn='RealExp：解耦Shapley值中的相关性偏差，实现忠实的模型解释'),
    dict(pre='Wen-Dong Jiang, Chih-Yung Chang, Ming-Yang Su, Yue-Shi Lee, and Diptendu Sinha Roy, '
             '\u201cToward Interpretable Multimodal Violence Detection with Knowledge Distillation '
             'and Modality-Aligned Preprocessing,\u201d ',
         it='IEEE Transactions on Systems, Man, and Cybernetics: Systems (TSMC)',
         post=', Vol. 55, No. 9, Pp. 6215-6228, Sept. 2025. (SCI Impact Factor: 8.6; '
              'AUTOMATION & CONTROL SYSTEMS: 5/84=5.9%, ',
         tail='中科院1区Top期刊，CCF-B，第一作者).',
         cn='基于知识蒸馏与模态对齐预处理的可解释多模态暴力行为检测'),
    dict(pre='Wen-Dong Jiang, Yu-Ting Chin, Yu-Ting Yang, Chih-Yung Chang, and Diptendu Sinha Roy, '
             '\u201cDetection, Retrieval, and Explanation Unified: A Violence Detection System '
             'Based on Knowledge Graphs and GAT,\u201d ',
         it='IEEE Transactions on Systems, Man, and Cybernetics: Systems (TSMC)',
         post=', Vol. 56, No. 4, Pp. 2827-2841, Apr. 2026. (SCI Impact Factor: 8.6; ',
         tail='中科院1区Top期刊，CCF-B，第一作者).',
         cn='检测、检索与解释一体化：基于知识图谱与图注意力网络（GAT）的暴力行为检测系统'),
    dict(pre='Wen-Dong Jiang, Chih-Yung Chang, Tzu-Chia Huang, Yu-Ting Chin, and Diptendu Sinha Roy, '
             '\u201cPEXP: A Scalable Parallel Tree-Based Framework for Interpreting Models on Big Data,\u201d ',
         it='IEEE Transactions on Big Data (TBD)',
         post=', Vol. 12, No. 4, Pp. 1177-1194, Aug. 2026. (SCI Impact Factor: 8.1; ',
         tail='中科院2区期刊，CCF-C，第一作者).',
         cn='PEXP：面向大数据模型解释的可扩展并行树框架'),
    dict(pre='Wen-Dong Jiang, Chih-Yung Chang, Yu-Ting Chin, Tzu-Chia Huang, and Diptendu Sinha Roy, '
             '\u201cInterpretable Federated Learning for Unsupervised Video Anomaly Detection in Smart City,\u201d ',
         it='IEEE Transactions on Emerging Topics in Computing (TETC)',
         post=', Vol. 14, No. 3, Pp. 1164-1180, Jul.-Sep. 2026. (SCI Impact Factor: 5.4; ',
         tail='中科院2区期刊，第一作者).',
         cn='面向智慧城市无监督视频异常检测的可解释联邦学习'),
    dict(pre='Wen-Dong Jiang, Chih-Yung Chang, Ssu-Chi Kuai, and Diptendu Sinha Roy, '
             '\u201cDecoVAD: Divide-and-Conquer Multimodal Learning for Video Anomaly Detection,\u201d ',
         it='IEEE Transactions on Systems, Man, and Cybernetics: Systems (TSMC)',
         post=', to appear, 2026. (Accepted) (SCI Impact Factor: 8.6; ',
         tail='中科院1区Top期刊，CCF-B，第一作者).',
         cn='DecoVAD：面向视频异常检测的分治式多模态学习'),
    dict(pre='Wen-Dong Jiang, Chih-Yung Chang, Tzu-Chia Huang, Yue-Shi Lee, and Diptendu Sinha Roy, '
             '\u201cAn Explainable KAN\u2013Shapley Framework for Many-to-Many Electric Vehicle Charging '
             'Dispatch in Intelligent Transportation Systems,\u201d ',
         it='IEEE Transactions on Intelligent Transportation Systems (TITS)',
         post=', to appear, 2026. (Accepted) (SCI Impact Factor: 8.5; ',
         tail='中科院2区Top期刊，CCF-B，第一作者).',
         cn='智能交通系统中面向多对多电动汽车充电调度的可解释KAN-Shapley框架'),
    dict(pre='Wen-Dong Jiang, Chung-You Tsai, Youxi Li, Chih-Yung Chang, Chong Wang, and Diptendu Sinha Roy, '
             '\u201cUro-PPLD: Physiology and Pathology-Aware Latent Diffusion for Cystoscopic Image '
             'Generation and Augmentation,\u201d ',
         it='IEEE Journal of Biomedical and Health Informatics (JBHI)',
         post=', 2026. (Accepted) (SCI Impact Factor: 6.8; ',
         tail='中科院2区Top期刊，CCF-C，第一作者).',
         cn='Uro-PPLD：面向膀胱镜图像生成与增强的生理病理感知潜在扩散模型'),
    dict(pre='Wen-Dong Jiang, Tsung-Jung Lin, Chih-Yung Chang, and Diptendu Sinha Roy, '
             '\u201cParallel Explainable Internet of Medical Things Framework with a Structured '
             'Multi-Agent Patient-State Representation for Hepatocellular Carcinoma Survival Prediction,\u201d ',
         it='IEEE Internet of Things Journal (IoTJ)',
         post=', 2026. (Accepted) (SCI Impact Factor: 8.7; ',
         tail='中科院2区Top期刊，CCF-C，第一作者).',
         cn='面向肝细胞癌生存预测的并行可解释医疗物联网框架：结构化多智能体患者状态表征'),
    dict(pre='Wen-Dong Jiang, Chih-Yung Chang, Tzu-Chia Huang, You-Xi Li, and Diptendu Sinha Roy, '
             '\u201cTree-Structured Two-Stage System for Efficient Violence Detection in '
             'Privacy-Constrained Event Streams,\u201d ',
         it='IEEE Transactions on Emerging Topics in Computational Intelligence (TETCI)',
         post=', to be published. (Accepted) (SCI Impact Factor: 6.0; ',
         tail='中科院2区期刊，第一作者).',
         cn='面向隐私受限事件流的高效两阶段树状暴力行为检测系统'),
]

projects = [
    ('使用关联规则及类神经网路去发掘属性间的关联性以改善分类效能之研究（NSTC 112-2221-E-130-010），计划参与。',
     '本人负责实验资料的收集、清洗与特征前处理，运用关联规则挖掘发掘属性间的潜在关联，'
     '并构建类神经网络分类模型进行多组对比实验，验证规则筛选对分类效能的提升效果。'),
    ('基于深度学习之霸凌侦测及专注力辨识系统（NSTC 112-2622-E-032-005），计划参与。',
     '本人参与霸凌言论资料的搜集、标注与预处理，负责深度学习侦测模型的训练与参数调校，'
     '并参与专注力辨识模块与整体系统的整合测试，协助系统原型的开发与验证。'),
    ('一个新的可解释机器学习方法之研究（NSTC 114-2221-E-130-005），计划参与。',
     '围绕事后解释方法在忠实性与效率上的不足，本人参与新型可解释框架的算法设计、理论分析与实验验证，|'
     '并在多个公开资料集上完成与LIME、Shapley值等基线方法的系统性对比评估。'),
    ('基于大模型的机器人问答平台开发，技术负责人，2023.05 - 2024.07。',
     '本人担任技术负责人，主导平台需求分析与系统架构设计，基于大语言模型搭建问答流水线，'
     '实现意图理解、知识库检索与多轮对话等核心模块，并带领团队完成开发、联调与版本迭代。'),
]

awards = [
    ('《不同机器学习模型在车牌辨识的应用》|——2022 数位联网智动化创新应用竞赛 佳作。',
     '针对车牌自动辨识任务，比较多种机器学习模型的表现，完成影像前处理、模型训练与准确率评估。'),
    ('《绿色商家推荐ESG之行销影片自动生成》|——2024 AI 智慧应用服务发展环境推动计划 优胜奖。',
     '结合生成式AI技术，实现绿色商家ESG行销影片的自动生成流程，降低行销素材制作成本。'),
    ('《Talk2Moocs：语音转磨课师之一键快速生成具个人风格讲课影片的AI系统》|——2025 智慧创新大赏 佳作。',
     '将教师授课语音一键转换为具个人风格的讲课影片，大幅降低磨课师制作数位课程的门槛与成本。'),
    ('《基于机器学习结合大型语言模型的膀胱癌影像切割系统》|——2025 发展部数位产业署「AIGO 淬炼实战杯竞赛」优等。',
     '结合机器学习与大型语言模型实现膀胱癌医学影像的自动切割，辅助医疗影像标注与后续分析。'),
]

story = []
story.append(Paragraph(esc('姜文栋'), S['name']))
story.append(Spacer(1, 2))
story.append(Paragraph(mix(contact), S['contact']))
story.append(Spacer(1, 10))

story.append(Paragraph(esc('教育经历'), S['h1cn']))
story.append(rule())
for school, date, lines in edu:
    story.append(school_row(school, date))
    for ln in lines:
        story.append(Paragraph(mix(ln), S['body']))
    story.append(Spacer(1, 1.5))

story.append(Paragraph(lat('Publication'), S['h1en']))
story.append(rule())
story.append(Paragraph(lat('Journal Paper') + esc('（第一作者）'), S['jp']))
for i, p in enumerate(papers, 1):
    en = (lat(f'{i}.\u00a0\u00a0') + lat(p['pre']) + lat(p['it'], italic=True)
          + lat(p['post']) + mix(p['tail']))
    cn = Paragraph(esc('中文题目：') + mix('《' + p['cn'] + '》'), S['cntitle'])
    story.append(KeepTogether([Paragraph(en, S['paper']), cn]))

story.append(Paragraph(mix('注：以上期刊分区均为中科院分区表 2025 版（2025年3月发布）数据。'), S['note']))
story.append(Spacer(1, 10))

# 项目经历/比赛得奖章节整体另起一页，避免被拦腰截断
story.append(CondPageBreak(480))
story.append(Paragraph(mix('项目经历 / 比赛得奖'), S['h1cn']))
story.append(rule())
story.append(Paragraph(esc('项目经历'), S['h2']))
for j, (p, desc) in enumerate(projects):
    if j == 0:
        # 手动断行避免行首出现逗号，与原简历断行位置一致
        p = mix('使用关联规则及类神经网路去发掘属性间的关联性以改善分类效能之研究（NSTC') \
            + '<br/>' + mix('112-2221-E-130-010），计划参与。')
        story.append(Paragraph(p, S['bullet'], bulletText='•'))
    else:
        story.append(Paragraph(mix(p), S['bullet'], bulletText='•'))
    desc_markup = '<br/>'.join(mix(seg) for seg in desc.split('|'))
    story.append(Paragraph(desc_markup, S['pdesc']))
story.append(Paragraph(esc('比赛得奖'), ParagraphStyle('h2b', parent=S['h2'], spaceBefore=7)))
for a, desc in awards:
    # '|' 为手动断行标记：避免书名号后长句换行产生孤字行
    parts = [mix(seg) for seg in a.split('|')]
    story.append(Paragraph('<br/>'.join(parts), S['bullet'], bulletText='•'))
    story.append(Paragraph(mix(desc), S['pdesc']))

doc = SimpleDocTemplate(
    r'C:/Users/Faker Lai/Desktop/个人网站/姜文栋-简历-修订版.pdf',
    pagesize=A4, leftMargin=57, rightMargin=57, topMargin=54, bottomMargin=57,
    title='姜文栋 - 个人简历', author='姜文栋', subject='个人简历（论文题目中英对照）',
    creator='Z.ai',
)
doc.build(story)
print('OK -> 姜文栋-简历-修订版.pdf')
