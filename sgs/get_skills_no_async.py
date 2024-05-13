# -*- encoding:utf-8 -*-
import asyncio
import concurrent.futures
import time
import requests
from sgs import models
import re
import random
import aiohttp
fa_url = 'https://wiki.biligame.com/'
se = ['sgs/', 'sgsol/', 'msgs/']

homepage = '首页'
user_list = [
    'Mozilla / 5.0(WindowsNT10.0;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 93.0.4577.82Safari / 537.36Edg / 93.0.961.52',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0',
    'Mozilla / 5.0(Windows NT 10.0;Win64;x64;rv: 89.0) Gecko / 20100101Firefox / 89.0'
]


def get_rolename(ser):
    new_role_patten = re.compile(
        r'<script type="text/javascript">var titles = "(?P<rolename>.*?)";var hasInput = "";</script>', re.S)
    new_resp = requests.get(fa_url + ser + homepage).text
    role_names = re.findall(new_role_patten, new_resp)[0].split(',')
    # role_names = ['SP关羽', 'SP太史慈', 'SP姜维', 'SP孙尚香', 'SP庞德', 'SP庞统', 'SP徐庶', 'SP蔡文姬', 'SP贾诩',
    #               'SP赵云',
    #               'SP马超', 'SP黄月英', '丁原', '丁奉', '丁尚涴', '万年公主', '丘力居', '严夫人', '严畯', '严白虎',
    #               '严颜',
    #               '乐周妃', '乐大乔', '乐小乔', '乐就', '乐綝', '乐蔡文姬', '乐进', '于吉', '于禁', '伊籍', '伏完',
    #               '伏皇后',
    #               '何太后', '何晏', '何进', '傅肜傅佥', '兀突骨', '全惠解', '全琮', '公孙修', '公孙度', '公孙渊',
    #               '公孙瓒',
    #               '关兴张苞', '关宁', '关平', '关索', '关羽', '关银屏', '典韦', '冯妤', '冯方', '冯熙', '凌统', '刘协',
    #               '刘备', '刘宏', '刘宠骆俊', '刘封', '刘巴', '刘徽', '刘晔', '刘永', '刘焉', '刘理', '刘琦', '刘禅',
    #               '刘繇',
    #               '刘虞', '刘表', '刘谌', '刘辟', '刘辩', '华佗', '华歆', '华雄', '卑弥呼', '南华老仙', '卞喜',
    #               '卞夫人',
    #               '卢弈', '卢植', '卧龙诸葛', '卫温诸葛直', '司马徽', '司马懿', '司马朗', '吉平', '向朗', '吕凯',
    #               '吕岱',
    #               '吕布', '吕旷吕翔', '吕玲绮', '吕范', '吕蒙', '吕虔', '吴兰', '吴国太', '吴懿', '吴班', '吴苋',
    #               '吴范',
    #               '周不疑', '周仓', '周善', '周夷', '周妃', '周宣', '周泰', '周瑜', '周鲂', '唐咨', '唐姬', '士燮',
    #               '夏侯令女', '夏侯惇', '夏侯杰', '夏侯楙', '夏侯氏', '夏侯渊', '夏侯霸', '大乔', '大乔小乔', '太史慈',
    #               '姜维', '孔融', '孙乾', '孙亮', '孙休', '孙坚', '孙寒华', '孙尚香', '孙权', '孙桓', '孙狼', '孙瑜',
    #               '孙登',
    #               '孙皓', '孙策', '孙綝', '孙翊', '孙翎鸾', '孙茹', '孙资刘放', '孙鲁班', '孙鲁育', '孟优', '孟节',
    #               '孟获',
    #               '孟达', '宗预', '小乔', '尹夫人', '岑昏', '崔琰毛玠', '左慈', '庞会', '庞山民', '庞德', '庞德公',
    #               '庞统',
    #               '廖化', '张任', '张勋', '张奋', '张媱', '张嫙', '张宁', '张宝', '张嶷', '张恭', '张昌蒲', '张星彩',
    #               '张春华', '张昭张纮', '张曼成', '张松', '张梁', '张楚', '张横', '张济', '张温', '张琪瑛', '张瑾云',
    #               '张绣',
    #               '张虎', '张角', '张让', '张辽', '张邈', '张郃', '张闿', '张飞', '张鲁', '徐庶', '徐晃', '徐氏',
    #               '徐盛',
    #               '徐荣', '忙牙长', '戏志才', '文聘', '星张春华', '星曹仁', '星董卓', '星袁术', '星袁绍', '是仪',
    #               '曹丕',
    #               '曹仁', '曹休', '曹冲', '曹华', '曹叡', '曹婴', '曹安民', '曹宪', '曹嵩', '曹彰', '曹性', '曹操',
    #               '曹昂',
    #               '曹植', '曹洪', '曹爽', '曹真', '曹纯', '曹节', '曹轶', '曹金玉', '曹髦', '朱儁', '朱建平', '朱桓',
    #               '朱治',
    #               '朱灵', '朱然', '李严', '李傕', '李傕郭汜', '李儒', '李典', '李婉', '李异谢旌', '李肃', '李采薇',
    #               '杜夔',
    #               '杜夫人', '杜畿', '杜预', '杨仪', '杨婉', '杨弘', '杨彪', '柏灵筠', '桓范', '桥蕤', '梁兴', '樊玉凤',
    #               '樊稠', '步练师', '步骘', '武安国', '武诸葛亮', '武陆逊', '段巧笑', '段煨', '毌丘俭', '沙摩柯',
    #               '沮授',
    #               '法正', '淳于琼', '滕公主', '滕胤', '滕芳兰', '满宠', '潘凤', '潘淑', '潘濬', '潘璋马忠', '灵雎',
    #               '牛辅',
    #               '牛金', '王允', '王双', '王基', '王威', '王平', '王异', '王悦', '王昶', '王朗', '王桃', '王濬',
    #               '王烈',
    #               '王粲', '王荣', '甄姬', '甘夫人', '甘夫人糜夫人', '甘宁', '田丰', '田尚衣', '留赞', '皇甫嵩', '祖茂',
    #               '祝融', '神关羽', '神刘备', '神司马懿', '神吕布', '神吕蒙', '神周瑜', '神姜维', '神张角', '神张辽',
    #               '神张飞', '神曹操', '神甘宁', '神许褚', '神诸葛亮', '神赵云', '神邓艾', '神陆逊', '神马超', '祢衡',
    #               '秦宓',
    #               '秦宜禄', '秦朗', '程昱', '程普', '程秉', '穆顺', '童渊', '笮融', '简雍', '管亥', '管宁', '管辂',
    #               '糜夫人',
    #               '糜竺', '糜芳傅士仁', '纪灵', '羊祜', '胡昭', '胡班', '胡车儿', '胡金定', '臧霸', '芮姬', '花鬘',
    #               '苏飞',
    #               '荀彧', '荀攸', '荀谌', '葛玄', '董允', '董卓', '董承', '董昭', '董白', '董绾', '董翓', '董贵人',
    #               '蒋干',
    #               '蒋琬费祎', '蒋钦', '蒯祺', '蒯良蒯越', '蒲元', '蔡夫人', '蔡文姬', '蔡瑁张允', '蔡邕', '蔡阳',
    #               '薛灵芸',
    #               '薛综', '虞翻', '袁姬', '袁术', '袁绍', '袁谭袁尚袁熙', '裴元绍', '许劭', '许攸', '许褚', '许贡',
    #               '许靖',
    #               '诸葛亮', '诸葛尚', '诸葛恪', '诸葛果', '诸葛梦雪', '诸葛瑾', '诸葛瞻', '诸葛若雪', '诸葛诞',
    #               '谋司马懿',
    #               '谋周瑜', '谋鲁肃', '谢灵毓', '谯周', '貂蝉', '贺齐', '贾充', '贾诩', '赵云', '赵俨', '赵嫣', '赵忠',
    #               '赵昂', '赵直', '赵统赵广', '赵襄', '蹋顿', '轲比能', '辛宪英', '辛毗', '邓艾', '邓芝', '邢道荣',
    #               '邹氏',
    #               '郑浑', '郝昭', '郝萌', '郤正', '郭嘉', '郭图逢纪', '郭汜', '郭淮', '郭照', '郭皇后', '钟会', '钟繇',
    #               '阎柔', '阚泽', '阮瑀', '阮籍', '陆凯', '陆抗', '陆绩', '陆逊', '陆郁生', '陈到', '陈宫', '陈式',
    #               '陈武董袭', '陈泰', '陈珪', '陈琳', '陈登', '陈矫', '陈群', '陶谦', '雷薄', '雷铜', '霍峻', '韩当',
    #               '韩浩史涣', '韩遂', '韩馥', '韩龙', '顾雍', '颜良文丑', '马云騄', '马伶俐', '马岱', '马忠', '马日磾',
    #               '马腾', '马谡', '马超', '骆统', '高翔', '高览', '高顺', '魏延', '鲁肃', '鲍三娘', '麴义', '黄忠',
    #               '黄承彦',
    #               '黄月英', '黄权', '黄皓', '黄盖', '黄祖']
    return role_names


def get_skills(ser):
    skills_pattern = re.compile(
        r'<span id="refreshContainer"><script type="text/javascript">var titles = "(?P<skill_names>.*?)";var hasInput = "";</script>')
    skill_page_resp = requests.get(fa_url + ser + '技能图鉴').text
    skills = re.findall(skills_pattern, skill_page_resp)[0].split(',')
    # skills = ['七哀', '七星', '三头', '三顾', '三首', '下书', '不屈', '专对', '业仇', '业炎', '严教', '举义', '举荐',
    #           '举讹', '义从', '义绝', '义舍', '义襄', '乐泉', '九伐', '乱击', '乱战', '乱武', '争擎', '交锋', '亦算',
    #           '享乐', '仁德', '仁心', '仁政', '仇决', '仇海', '仇讨', '介绫', '从势', '从谏/张绣', '从谏/童渊', '仓储',
    #           '仙授', '伉厉', '伏枥', '伏诛', '伏间', '伏骑', '传术', '伤逝', '伪帝/袁术', '伪帝/袁术(国战)', '伪诚',
    #           '伪谠', '伺攻', '伺盗', '佐定', '佐谏', '余威', '佛宗', '作威', '侵暴', '俐影', '修文', '倾势', '倾国',
    #           '倾城', '倾袭', '偏宠', '催进', '傲势', '傲才', '儒贤', '元嫡', '先率', '先辅', '光噬', '克己', '八阵',
    #           '公清', '共修', '共护', '兴乱', '兴作', '兴学', '兴棹', '兴汉', '兴火', '兴衰', '兵略', '典财', '内伐',
    #           '再起', '军略', '冢骨', '冲虚', '冲阵', '决堰', '决死', '决讨', '凌人', '凌芳', '凤魄', '凶疑', '凶算',
    #           '凶镬', '击虚', '击逆', '凿险', '列侯', '刚烈', '利傍', '利熏', '利驭', '别君', '制蛮/关索', '制蛮/马谡',
    #           '制衡/孙权', '制衡/神司马懿', '制霸', '刺北', '割圆', '力激', '劝守', '劝谏', '功獒', '助势', '劫营',
    #           '劲坚', '势举', '勇决', '勇略', '勇进', '勘集', '勤国', '勤学', '勤慎', '勤王', '化归', '化萍', '化身',
    #           '匡弼', '匿伏', '十计', '千幻', '千驹', '华衣', '协守', '单骑', '卜筮', '卜算', '占梦', '危盟', '危迫',
    #           '去疾', '双刃', '双璧', '双雄', '反间', '反馈', '受责', '变装', '叛弑', '叠嶂', '司天', '司敌', '吉境',
    #           '同心', '同援', '同礼', '名士', '命戒', '咆哮/关兴张苞', '咆哮/夏侯霸', '咆哮/张飞', '和洽', '咒缚',
    #           '哀尘', '品第', '啖酪', '善身', '四论', '困奋', '固政', '国色', '图兴', '图南', '图射', '圮秩', '地法',
    #           '墨守', '壮胆', '壮魄', '复学', '复难', '夕颜', '夙守', '大雾', '天义', '天任', '天则', '天劫', '天匠',
    #           '天命', '天妒/戏志才', '天妒/郭嘉', '天机', '天覆', '天辩', '天运', '天香/大乔小乔', '天香/小乔', '失守',
    #           '失诏', '夺锐', '奇制', '奇径', '奇才', '奇策', '奇袭', '奇谋', '奉迎', '奋励', '奋命', '奋威/甘宁',
    #           '奋威/贺齐', '奋激', '奋迅', '奋钺', '奋音/吴范', '奋音/留赞', '奔矢', '奔袭', '奢葬', '奸雄/曹婴',
    #           '奸雄/曹操', '好施', '如意', '妄缘', '妆戎', '妙弦', '姊希', '威临', '威虏', '威重', '娴静', '婆娑',
    #           '婵娟', '媦婉', '媵予', '存嗣', '存畏', '孤扼', '守成', '守玺', '安国', '安境', '安恤', '安辽',
    #           '完杀/神司马懿', '完杀/贾诩', '宗室', '定叛', '定基', '定措', '宝梳', '审时', '宴诛', '宵袭', '宽释',
    #           '寄春', '寄篱', '寅君', '密诏', '密运', '寇旌', '寇略', '寒英', '寝情', '寤寐', '寸目', '寻嫉', '封乡',
    #           '将息', '将略', '将驰', '尊位', '尚义', '尽瘁', '尽节', '展骥', '屯军', '屯江', '屯田', '峻刑', '崇义',
    #           '崇望', '崖柴', '崩坏/董卓', '崩坏/董卓（国战）', '崩坏/诸葛诞', '巡使', '巧变', '巧说', '巨象', '巨贾',
    #           '布施', '帷幕', '帼武', '干蛊', '平寇', '平袭', '平襄', '平辽', '幸宠', '幽栖', '应势', '应时', '度势',
    #           '庸肆', '延祸', '开济', '异兆', '异勇', '异教', '异色', '弃子', '弓骑', '引兵', '引裾', '引路', '弘德',
    #           '弘援', '弥笃', '强峙', '强袭', '强识', '归命', '归心', '归离', '当先/关索', '当先/廖化', '彩妆', '彩翼',
    #           '彰才', '影兵', '往烈', '征南', '征荣', '征辟', '御关', '御心', '御策', '德劭', '德化', '德释', '心幽',
    #           '忍戒', '志继', '忘隙', '忠勇', '忠壮', '忠节', '忠鉴', '忧恤', '忿肆', '怀子', '怀异', '怀柔', '怀橘',
    #           '怃戎', '怒嗔', '怒涛', '思辩', '怠宴', '急援', '急攻', '急救', '急袭/邓艾', '急袭/邓艾（国战）', '怨语',
    #           '恂恂/唐咨', '恂恂/李典', '恃才', '恃纵', '恢拓', '恩怨', '恩遇', '恪守', '息兵', '悍勇', '悖逆', '悟道',
    #           '悯泽', '悲愤', '悲歌', '情势', '惊澜', '惠民', '惴恐', '惴栗', '惶恐', '愆正', '慈孝', '慈悲', '慎断',
    #           '慎行', '慧淑', '慷忾', '成略', '战孤', '战意', '战绝', '战缘', '戚乱', '戡难', '截刀', '截辎', '手谈',
    #           '才思', '才瑕', '才识', '托献', '执笏', '扫围', '扶援', '扶汉', '承赏', '把盏', '抗歌', '抚宁', '抚悼',
    #           '抚蛮', '抚黎', '护关/王悦', '护关/王桃', '护援', '护驾', '拆械', '拒战', '拓域', '招祸', '拜假', '拜印',
    #           '拥嫡', '拥嬖', '择才', '持节', '指誓', '挈挟', '挑衅/SP姜维', '挑衅/夏侯霸', '挑衅/姜维', '挡灾', '挫锐',
    #           '挽危', '捐甲', '据守', '掌戎', '排异', '掠命', '掠城', '掣政', '推演', '掳掠', '揖让', '援护', '摇佩',
    #           '摧克', '摧决', '摧坚', '摧心', '摧锐', '撷翠', '撷芳', '擎北', '擢吏', '攻坚', '攻心/界吕蒙',
    #           '攻心/神吕蒙', '攻心/葛玄', '放权', '放逐/曹丕', '放逐/神司马懿', '敏思', '救援', '救陷', '散文', '散谣',
    #           '数合', '数荐', '整论', '文灿', '斗阵', '斩涛', '斩腕', '断发', '断念', '断粮', '断绁', '断肠', '断腕',
    #           '新生', '方统', '旋略', '旋风', '无前', '无双/吕布', '无双/吕玲绮', '无双/神吕布', '无节', '无言', '无谋',
    #           '日彗', '昊宠', '明任', '明伐', '明势', '明哲', '明慧', '明策', '明鉴', '易数', '星舞', '昭文', '昭汉',
    #           '智哲', '智愚', '智迟', '暖惠', '暗涌', '暗箭', '暗织', '暴凌', '暴虐', '替身', '望归', '望族', '望橹',
    #           '朝凤', '札符', '机巧', '机捷', '杀绝', '权计', '权谋', '极奢', '极略', '枕戈', '枪舞', '枭姬/SP孙尚香',
    #           '枭姬/孙尚香', '梁燕', '梦解', '榱椽', '横征', '横江', '横骛', '樵拾', '止啼', '止息', '正序', '正订',
    #           '武圣/SP关羽', '武圣/关兴张苞', '武圣/关索', '武圣/关羽', '武娘', '武神', '武继', '武缘', '武魂', '死谏',
    #           '殃众', '殉别', '殉节', '残玺', '残肆', '残蚀', '殚心', '毒逝', '氓情', '气傲', '求援', '汇灵', '沉勇',
    #           '沙舞', '没欲', '法器', '法恩', '法箓', '泛音', '泣别', '洛神', '活墨/胡昭', '活墨/钟繇', '活气', '流年',
    #           '流矢', '流离/大乔', '流离/大乔小乔', '流转', '浮海', '浮萍', '涅槃', '涉猎', '涕泣', '涯角', '淑慎',
    #           '清严', '清侧', '清俭', '清剿', '清谈', '渐专', '渐营', '溃击', '溃蟒', '溃诛', '溃阵', '滔乱', '漂萍',
    #           '潜心', '潜袭', '潜龙', '激将/刘备', '激将/刘禅', '激峭', '激昂', '激词', '火计', '灭计', '灵慧', '灵犀',
    #           '灵箜', '炜烈', '点化', '炼化', '烈刃', '烈医', '烈弓', '焚城', '焚心', '焦尾', '熊扰', '燃殇', '燕尔',
    #           '燕语', '父荫', '父魂', '狂才', '狂斧', '狂暴', '狂风', '狂骨', '狐魅', '狡黠', '狩骊', '独往', '独锋',
    #           '狷狭', '狼灭', '狼袭', '献图', '献州', '玉殒', '玉碎', '玲珑', '琴音', '琼英', '甘露', '甚贤', '生妒',
    #           '生息', '画策', '疑城', '疠火', '瘴气', '登楼', '皙秀', '盗书', '盗戟', '盟谋', '直言/葛玄', '直言/虞翻',
    #           '直谏', '相面', '相鼠', '盻睇', '省身', '看破/卧龙诸葛', '看破/姜维', '真仪', '眩惑', '督粮', '矜功',
    #           '矜谨', '矢北', '矢志', '知否', '矫诏', '短兵/丁奉', '短兵/贺齐', '破军', '破势', '破垣', '破锐', '砺锋',
    #           '硝引', '硝焰', '示烈', '礼下', '礼让', '礼赂', '祈禳', '神威/吕玲绮', '神威/吕玲绮（国战）', '神愤',
    #           '神智', '神裁', '神速/夏侯渊', '神速/夏侯霸', '祸水', '祸首', '禁酒', '福绵', '离宫', '离间', '私掠',
    #           '秉壹', '秉正', '秉纪', '秉节', '秘计', '称好', '称象', '移驾', '穆穆', '空城', '穿云', '穿心', '突袭',
    #           '窃听', '立军', '立牧', '竭忠', '竭缘', '笔伐', '筑围', '筹策', '简亮', '箜声', '米道', '粮绝', '粮营',
    #           '精弓', '精策', '系力', '索粮', '红颜', '约俭', '纵傀', '纵势', '纵反', '纵玄', '纵适', '织纴', '经合',
    #           '经造', '结姻', '结营', '绝地', '绝境', '绝情', '绝策', '统业', '统围', '统观', '绡刃', '绡舞', '绥抚',
    #           '继椒', '绮琴/乐大乔', '绮琴/乐小乔', '绮胄', '绽火', '缓释', '缔盟', '缜略', '缠怨', '缮甲', '罪论',
    #           '羽化', '翊正', '翊赞', '耀武', '耽意', '聆乐', '联对', '肃军', '肆军', '肉林', '股算', '胆守', '胆迎',
    #           '背水', '腹谋', '腹鳞', '膂力', '自固', '自守', '自牧', '自立', '至微', '舌剑', '舍宴', '良助', '良姻',
    #           '良秀', '节命', '节应', '节烈', '节行', '节钺', '花火', '芳妒', '芳魂', '芸香', '若愚', '苦肉',
    #           '英姿/周瑜', '英姿/孙策', '英姿/孙翊', '英姿/葛玄', '英姿/贺齐', '英谋', '英魂/孙坚', '英魂/孙策',
    #           '英魂/孙翊', '荐杰', '荐言', '荐降', '莲佑', '营图', '营说', '落宠', '落英', '落雁', '蒺藜', '蕙质',
    #           '薮影', '藿溪', '虎啸', '虚猲', '蚕食', '蛊惑', '蛮嗣', '蛮智', '蛮裔/孟优', '蛮裔/花鬘', '蜜饴', '融火',
    #           '螽集', '血卫', '血裔', '血诏', '行殇/曹丕', '行殇/曹婴', '补益', '表召', '衰劫', '袭阵', '裂围', '裂胆',
    #           '裸衣', '襄戍', '覆斗', '观微', '观星/姜维', '观星/葛玄', '观星/诸葛亮', '观月', '观潮', '解围', '解术',
    #           '解烦', '解阵', '言政', '誓仇', '许身', '论道', '讽言', '设伏', '设学', '评荐', '识命', '诈降', '诏缚',
    #           '诗仙', '诗怨', '诛佞', '诛害', '询疠', '诫训', '诱战', '诱敌', '诱言', '说盟', '调度', '谋断', '谋溃',
    #           '谋诛', '谋逆', '谋逞', '谏国', '谏征', '谏诤', '谗逆', '谛听', '谦节', '谦逊', '谦雅', '谮构', '谮毁',
    #           '豪首', '豹变', '贞烈', '贞特', '贞良', '负重', '贤望', '贤淑', '贪狈', '贲育', '贿生', '资援', '资粮',
    #           '赏誉', '赠刀', '趫猛', '踏寂', '踞营', '蹙国', '轶祖', '轻幔', '辟境', '辟撰', '辟田', '过论', '运柩',
    #           '返乡', '返势', '进谏', '进趋', '远谟', '违忤', '连枝', '连环', '连破', '连舟', '连营', '连计', '连诛',
    #           '追击', '追德', '追忆', '追猎', '追袭', '追还', '送丧', '逆乱', '逆击', '逊贤', '逐寇', '途绝', '通博',
    #           '通辽', '逢亮', '遁世', '遗志', '遗礼', '遗计', '遣信', '避乱', '避祸', '邀名', '邀弈', '郡兵', '配器',
    #           '酒仙', '酒池', '酒诗', '酒遁', '醇醪', '醮影', '金睛', '钝袭', '铁骑', '铃音', '铤险', '铸刃', '铸币',
    #           '链祸', '锋势', '锋略', '锋矢', '锐战', '锦绘', '镇军', '镇南', '镇卫', '镇行', '镇锋', '镇骨', '长姬',
    #           '长驱', '闪袭', '闭境', '闭月', '问卦', '问计', '间书', '间计', '闺秀', '阴兵', '附敌', '陈情', '陈见',
    #           '除疠', '险卫', '险进', '陷嗣', '陷筑', '陷阵', '隅泣', '随势', '随征', '随认', '隐世', '隐士', '隐逸',
    #           '隘守', '雄乱', '雄幕', '雄异', '雄莽', '集众', '集军', '集智/神司马懿', '集智/陆抗', '集智/黄月英',
    #           '雉盗', '雪恨', '雷击', '震泽', '霜笳', '霞泪', '青刃', '青囊', '青荒', '鞬出', '顺世', '颂威', '颂蜀',
    #           '颂词', '预言', '风影', '飞军', '飞影', '飞白', '饰非', '馈珠', '马术/SP关羽', '马术/SP庞德', '马术/庞德',
    #           '马术/贺齐', '马术/马云騄', '马术/马岱', '马术/马腾', '马术/马超', '驰应', '驱虎', '驳言', '骁果', '骁隽',
    #           '骄妄', '骄恣', '骄矜', '骊马', '骨疽', '鬻爵', '鬼助', '鬼才/司马懿', '鬼才/神司马懿', '鬼道',
    #           '魂姿/孙策', '魂姿/孙翊', '魂殇', '魄袭', '魅步', '鸟翔', '鸡肋', '鸣鸾', '鸩毒', '鸿举', '鹤翼', '鹰扬',
    #           '黄天', '默识', '黠慧', '黠策', '黩武', '鼓舌', '龙吟', '龙宫', '龙怒', '龙渊', '龙胆/SP赵云',
    #           '龙胆/童渊', '龙胆/赵云', '龙诵', '龙魂']
    return skills


def get_skill_detail(ser, skill_name):
    skill_detail_pattern = re.compile(r'''<th style="width: 100px;">描述\n</th>\n<td>(?P<skde>.*?)\n</td>''', re.S)
    skill_detail_type_pattern = re.compile(r'''<tr>\n<th>类型\n</th>.*?</tr>''', re.S)
    skill_detail_type_pattern2 = re.compile(r'''<font color="white">(?P<sktp>.*?)</font>''', re.S)
    skill_belong_pattern = re.compile(r'''所属武将：(?P<skbt>.*?)</div>''', re.S)
    server = ''
    if ser == 'msgs/': server = '移动版'
    if ser == 'sgsol/': server = 'online'
    if ser == 'sgs/': server = '十周年'

    header = {'User-Agent': random.choice(user_list)}
    skill_detail_c=requests.get(fa_url + ser + skill_name,headers=header)
    skill_detail_resp= skill_detail_c.text
    raw_skill_detail = re.search(skill_detail_pattern, skill_detail_resp).group('skde')
    skill_detail_type = re.search(skill_detail_type_pattern, skill_detail_resp)
    if skill_detail_type is not None:
        skill_detail_type=skill_detail_type.group()
    else:
        skill_detail_type=''
    skill_detail_type = re.findall(skill_detail_type_pattern2, skill_detail_type)
    skill_detail = re.sub(r'<.*?>', '', raw_skill_detail)
    skill_belong = re.search(skill_belong_pattern, skill_detail_resp).group('skbt')

    tmp=(skill_name.split('/')[0], skill_belong, skill_detail, ','.join(skill_detail_type))
    obj = models.Skills_Table(skill_name=tmp[0], skill_belong=tmp[1], skill_detail=tmp[2], skill_type=tmp[3],
                               skill_server=server)
    obj.save()
    time.sleep(0.5)
    # except:
    #     print(server,skill_name, '--------------------------------')


def get_sk(ser):
    sk_lst = get_skills(ser)
    for i in range(min(20, len(sk_lst))):
        get_skill_detail(ser, sk_lst[i])


def main(ser):
    # asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    get_sk(ser)

def thread_pool():
    t1 = time.time()

    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        for i in range(3):
            executor.submit(main, se[i])
    t2=time.time()
    print(t2-t1)
    print(60)
    # 14.728772401809692
    # 60