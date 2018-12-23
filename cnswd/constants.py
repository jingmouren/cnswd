"""
全局性常量
"""
import pandas as pd

MARKET_START = pd.Timestamp('1990-12-10', tz='UTC')

EARLIEST_POSSIBLE_DATE = pd.Timestamp('2006-3-1', tz='UTC')

ROOT_DIR_NAME = '~/.cndata'

DB_DIR_NAME = 'cn'  # 确定数据库目录

DB_NAME = 'stock.db'

QUOTE_COLS = (
    '股票代码', '股票简称',
    '开盘', '前收盘', '现价', '最高', '最低',
    '竞买价', '竞卖价', '成交量', '成交额',
    '买1量', '买1价',
    '买2量', '买2价',
    '买3量', '买3价',
    '买4量', '买4价',
    '买5量', '买5价',
    '卖1量', '卖1价',
    '卖2量', '卖2价',
    '卖3量', '卖3价',
    '卖4量', '卖4价',
    '卖5量', '卖5价',
    '日期', '时间'
)
# 可使用脚本整理数据(industry_to_dict.py)

# 行业分类
## 证监会行业一级编码
CRSC_INDUSTRY_1 = {
    'A': '农、林、牧、渔业',
    'B': '采矿业',
    'C': '制造业',
    'D': '电力、热力、燃气及水生产和供应业',
    'E': '建筑业',
    'F': '批发和零售业',
    'G': '交通运输、仓储和邮政业',
    'H': '住宿和餐饮业',
    'I': '信息传输、软件和信息技术服务业',
    'J': '金融业',
    'K': '房地产业',
    'L': '租赁和商务服务业',
    'M': '科学研究和技术服务业',
    'N': '水利、环境和公共设施管理业',
    'O': '居民服务、修理和其他服务业',
    'P': '教育',
    'Q': '卫生和社会工作',
    'R': '文化、体育和娱乐业',
    'S': '综合',
}
## 证监会行业二级编码
CRSC_INDUSTRY_2 = {
    'A01': '农业',
    'A02': '林业',
    'A03': '畜牧业',
    'A04': '渔业',
    'A05': '农、林、牧、渔服务业',
    'B06': '煤炭开采和洗选业',
    'B07': '石油和天然气开采业',
    'B08': '黑色金属矿采选业',
    'B09': '有色金属矿采选业',
    'B10': '非金属矿采选业',
    'B11': '开采辅助活动',
    'B12': '其他采矿业',
    'C13': '农副食品加工业',
    'C14': '食品制造业',
    'C15': '酒、饮料和精制茶制造业',
    'C16': '烟草制品业',
    'C17': '纺织业',
    'C18': '纺织服装、服饰业',
    'C19': '皮革、毛皮、羽毛及其制品和制鞋业',
    'C20': '木材加工和木、竹、藤、棕、草制品业',
    'C21': '家具制造业',
    'C22': '造纸和纸制品业',
    'C23': '印刷和记录媒介复制业',
    'C24': '文教、工美、体育和娱乐用品制造业',
    'C25': '石油加工、炼焦和核燃料加工业',
    'C26': '化学原料和化学制品制造业',
    'C27': '医药制造业',
    'C28': '化学纤维制造业',
    'C29': '橡胶和塑料制品业',
    'C30': '非金属矿物制品业',
    'C31': '黑色金属冶炼和压延加工业',
    'C32': '有色金属冶炼和压延加工业',
    'C33': '金属制品业',
    'C34': '通用设备制造业',
    'C35': '专用设备制造业',
    'C36': '汽车制造业',
    'C37': '铁路、船舶、航空航天和其他运输设备制造业',
    'C38': '电气机械和器材制造业',
    'C39': '计算机、通信和其他电子设备制造业',
    'C40': '仪器仪表制造业',
    'C41': '其他制造业',
    'C42': '废弃资源综合利用业',
    'C43': '金属制品、机械和设备修理业',
    'D44': '电力、热力生产和供应业',
    'D45': '燃气生产和供应业',
    'D46': '水的生产和供应业',
    'E47': '房屋建筑业',
    'E48': '土木工程建筑业',
    'E49': '建筑安装业',
    'E50': '建筑装饰和其他建筑业',
    'F51': '批发业',
    'F52': '零售业',
    'G53': '铁路运输业',
    'G54': '道路运输业',
    'G55': '水上运输业',
    'G56': '航空运输业',
    'G57': '管道运输业',
    'G58': '装卸搬运和运输代理业',
    'G59': '仓储业',
    'G60': '邮政业',
    'H61': '住宿业',
    'H62': '餐饮业',
    'I63': '电信、广播电视和卫星传输服务',
    'I64': '互联网和相关服务',
    'I65': '软件和信息技术服务业',
    'J66': '货币金融服务',
    'J67': '资本市场服务',
    'J68': '保险业',
    'J69': '其他金融业',
    'K70': '房地产业',
    'L71': '租赁业',
    'L72': '商务服务业',
    'M73': '研究和试验发展',
    'M74': '专业技术服务业',
    'M75': '科技推广和应用服务业',
    'N76': '水利管理业',
    'N77': '生态保护和环境治理业',
    'N78': '公共设施管理业',
    'O79': '居民服务业',
    'O80': '机动车、电子产品和日用产品修理业',
    'O81': '其他服务业',
    'P82': '教育',
    'Q83': '卫生',
    'Q84': '社会工作',
    'R85': '新闻和出版业',
    'R86': '广播、电视、电影和影视录音制作业',
    'R87': '文化艺术业',
    'R88': '体育',
    'R89': '娱乐业',
    'S90': '综合',
}

## 国证一级行业分类
GZ_INDUSTRY_1 = {
    'C01': '能源',
    'C02': '原材料',
    'C03': '工业',
    'C04': '可选消费',
    'C05': '主要消费',
    'C06': '医药卫生',
    'C07': '金融地产',
    'C08': '信息技术',
    'C09': '电信业务',
    'C10': '公用事业'}
## 国证二级行业分类
GZ_INDUSTRY_2 = {
    'C0101': '能源',
    'C0201': '基础化工',
    'C0202': '基础材料',
    'C0301': '工业品',
    'C0302': '工业服务',
    'C0303': '运输',
    'C0401': '汽车与汽车零配件',
    'C0402': '耐用消费品',
    'C0403': '纺织服装与奢侈品',
    'C0404': '消费者服务',
    'C0405': '传媒',
    'C0406': '零售业',
    'C0501': '食品与主要用品零售',
    'C0502': '农牧渔产品',
    'C0503': '食品饮料',
    'C0504': '家庭与个人用品',
    'C0601': '医疗保健设备与服务',
    'C0602': '制药',
    'C0603': '生物科技',
    'C0701': '银行',
    'C0702': '综合金融',
    'C0703': '房地产',
    'C0801': '软件与互联网',
    'C0802': '技术硬件与设备',
    'C0803': '半导体',
    'C0901': '电信服务',
    'C0902': '通信设备及技术服务',
    'C1001': '公用事业',
}
## 国证三级行业分类
GZ_INDUSTRY_3 = {
    'C010101': '能源设备与服务',
    'C010102': '石油天然气',
    'C010103': '煤炭',
    'C010104': '可替代能源',
    'C020101': '化学原料',
    'C020102': '化学制品',
    'C020103': '农用化工',
    'C020104': '合成纤维',
    'C020201': '建筑材料',
    'C020202': '容器与包装',
    'C020203': '黑色金属',
    'C020204': '有色金属',
    'C020205': '非金属材料与制品',
    'C020206': '纸类与林业产品',
    'C030101': '航天航空',
    'C030102': '建筑产品',
    'C030103': '电气部件与设备',
    'C030104': '重型电气设备',
    'C030105': '通用机械',
    'C030106': '专用设备',
    'C030107': '工业集团企业',
    'C030201': '建筑与工程',
    'C030202': '工业贸易经销商',
    'C030203': '商业用品与服务',
    'C030301': '物流',
    'C030302': '航空运输',
    'C030303': '水上运输',
    'C030304': '陆运',
    'C030305': '交通基本设施',
    'C040101': '汽车零配件与设备',
    'C040102': '汽车',
    'C040201': '家用电器',
    'C040202': '耐用家居用品',
    'C040203': '休闲设备与用品',
    'C040301': '服装与配饰',
    'C040302': '纺织品',
    'C040401': '酒店餐饮与休闲',
    'C040402': '其他消费者服务',
    'C040501': '传媒',
    'C040601': '消费品经销商',
    'C040602': '网络零售',
    'C040603': '百货商店',
    'C040604': '专营零售',
    'C050101': '食品与主要用品零售',
    'C050201': '农牧渔产品',
    'C050301': '食品',
    'C050302': '饮料',
    'C050401': '家常用品',
    'C050402': '个人用品',
    'C060101': '医疗保健设备与用品',
    'C060102': '医疗保健提供商与服务',
    'C060201': '化学原料药',
    'C060202': '化学制剂',
    'C060203': '中药',
    'C060301': '生物科技',
    'C070101': '银行',
    'C070201': '证券',
    'C070202': '保险',
    'C070203': '投资信托',
    'C070204': '其他金融服务',
    'C070301': '房地产开发和管理',
    'C070302': '房地产服务',
    'C080101': '互联网软件与服务',
    'C080102': '信息技术服务',
    'C080103': '计算机软件',
    'C080201': '电脑与外围设备',
    'C080202': '电子设备及服务',
    'C080203': '电子元器件',
    'C080204': '光电子器件',
    'C080301': '半导体',
    'C090101': '电信运营',
    'C090102': '电信增值服务',
    'C090201': '通信设备',
    'C090202': '通信技术服务',
    'C100101': '电力公用事业',
    'C100102': '燃气公用事业',
    'C100103': '水公用事业',
    'C100104': '复合型公用事业',
}
