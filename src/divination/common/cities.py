"""
中国城市数据

包含中国所有地级市、直辖市、特别行政区，用于出生地点智能输入

数据来源：MingAI src/lib/cities.ts
"""
from typing import Dict, List, Optional, TypedDict


class CityInfo(TypedDict):
    """城市信息"""
    name: str       # 城市名称
    province: str   # 所属省份
    full_name: str  # 完整显示名称


# 中国城市列表 (293个地级市 + 4个直辖市 + 特别行政区)
CHINA_CITIES: List[CityInfo] = [
    # 直辖市
    {'name': '北京市', 'province': '北京', 'full_name': '北京市'},
    {'name': '天津市', 'province': '天津', 'full_name': '天津市'},
    {'name': '上海市', 'province': '上海', 'full_name': '上海市'},
    {'name': '重庆市', 'province': '重庆', 'full_name': '重庆市'},
    # 河北省
    {'name': '石家庄', 'province': '河北', 'full_name': '河北省石家庄市'},
    {'name': '唐山', 'province': '河北', 'full_name': '河北省唐山市'},
    {'name': '秦皇岛', 'province': '河北', 'full_name': '河北省秦皇岛市'},
    {'name': '邯郸', 'province': '河北', 'full_name': '河北省邯郸市'},
    {'name': '邢台', 'province': '河北', 'full_name': '河北省邢台市'},
    {'name': '保定', 'province': '河北', 'full_name': '河北省保定市'},
    {'name': '张家口', 'province': '河北', 'full_name': '河北省张家口市'},
    {'name': '承德', 'province': '河北', 'full_name': '河北省承德市'},
    {'name': '沧州', 'province': '河北', 'full_name': '河北省沧州市'},
    {'name': '廊坊', 'province': '河北', 'full_name': '河北省廊坊市'},
    {'name': '衡水', 'province': '河北', 'full_name': '河北省衡水市'},
    # 山西省
    {'name': '太原', 'province': '山西', 'full_name': '山西省太原市'},
    {'name': '大同', 'province': '山西', 'full_name': '山西省大同市'},
    {'name': '阳泉', 'province': '山西', 'full_name': '山西省阳泉市'},
    {'name': '长治', 'province': '山西', 'full_name': '山西省长治市'},
    {'name': '晋城', 'province': '山西', 'full_name': '山西省晋城市'},
    {'name': '朔州', 'province': '山西', 'full_name': '山西省朔州市'},
    {'name': '晋中', 'province': '山西', 'full_name': '山西省晋中市'},
    {'name': '运城', 'province': '山西', 'full_name': '山西省运城市'},
    {'name': '忻州', 'province': '山西', 'full_name': '山西省忻州市'},
    {'name': '临汾', 'province': '山西', 'full_name': '山西省临汾市'},
    {'name': '吕梁', 'province': '山西', 'full_name': '山西省吕梁市'},
    # 内蒙古
    {'name': '呼和浩特', 'province': '内蒙古', 'full_name': '内蒙古呼和浩特市'},
    {'name': '包头', 'province': '内蒙古', 'full_name': '内蒙古包头市'},
    {'name': '乌海', 'province': '内蒙古', 'full_name': '内蒙古乌海市'},
    {'name': '赤峰', 'province': '内蒙古', 'full_name': '内蒙古赤峰市'},
    {'name': '通辽', 'province': '内蒙古', 'full_name': '内蒙古通辽市'},
    {'name': '鄂尔多斯', 'province': '内蒙古', 'full_name': '内蒙古鄂尔多斯市'},
    {'name': '呼伦贝尔', 'province': '内蒙古', 'full_name': '内蒙古呼伦贝尔市'},
    {'name': '巴彦淖尔', 'province': '内蒙古', 'full_name': '内蒙古巴彦淖尔市'},
    {'name': '乌兰察布', 'province': '内蒙古', 'full_name': '内蒙古乌兰察布市'},
    # 辽宁省
    {'name': '沈阳', 'province': '辽宁', 'full_name': '辽宁省沈阳市'},
    {'name': '大连', 'province': '辽宁', 'full_name': '辽宁省大连市'},
    {'name': '鞍山', 'province': '辽宁', 'full_name': '辽宁省鞍山市'},
    {'name': '抚顺', 'province': '辽宁', 'full_name': '辽宁省抚顺市'},
    {'name': '本溪', 'province': '辽宁', 'full_name': '辽宁省本溪市'},
    {'name': '丹东', 'province': '辽宁', 'full_name': '辽宁省丹东市'},
    {'name': '锦州', 'province': '辽宁', 'full_name': '辽宁省锦州市'},
    {'name': '营口', 'province': '辽宁', 'full_name': '辽宁省营口市'},
    {'name': '阜新', 'province': '辽宁', 'full_name': '辽宁省阜新市'},
    {'name': '辽阳', 'province': '辽宁', 'full_name': '辽宁省辽阳市'},
    {'name': '盘锦', 'province': '辽宁', 'full_name': '辽宁省盘锦市'},
    {'name': '铁岭', 'province': '辽宁', 'full_name': '辽宁省铁岭市'},
    {'name': '朝阳', 'province': '辽宁', 'full_name': '辽宁省朝阳市'},
    {'name': '葫芦岛', 'province': '辽宁', 'full_name': '辽宁省葫芦岛市'},
    # 吉林省
    {'name': '长春', 'province': '吉林', 'full_name': '吉林省长春市'},
    {'name': '吉林市', 'province': '吉林', 'full_name': '吉林省吉林市'},
    {'name': '四平', 'province': '吉林', 'full_name': '吉林省四平市'},
    {'name': '辽源', 'province': '吉林', 'full_name': '吉林省辽源市'},
    {'name': '通化', 'province': '吉林', 'full_name': '吉林省通化市'},
    {'name': '白山', 'province': '吉林', 'full_name': '吉林省白山市'},
    {'name': '松原', 'province': '吉林', 'full_name': '吉林省松原市'},
    {'name': '白城', 'province': '吉林', 'full_name': '吉林省白城市'},
    # 黑龙江省
    {'name': '哈尔滨', 'province': '黑龙江', 'full_name': '黑龙江省哈尔滨市'},
    {'name': '齐齐哈尔', 'province': '黑龙江', 'full_name': '黑龙江省齐齐哈尔市'},
    {'name': '鸡西', 'province': '黑龙江', 'full_name': '黑龙江省鸡西市'},
    {'name': '鹤岗', 'province': '黑龙江', 'full_name': '黑龙江省鹤岗市'},
    {'name': '双鸭山', 'province': '黑龙江', 'full_name': '黑龙江省双鸭山市'},
    {'name': '大庆', 'province': '黑龙江', 'full_name': '黑龙江省大庆市'},
    {'name': '伊春', 'province': '黑龙江', 'full_name': '黑龙江省伊春市'},
    {'name': '佳木斯', 'province': '黑龙江', 'full_name': '黑龙江省佳木斯市'},
    {'name': '七台河', 'province': '黑龙江', 'full_name': '黑龙江省七台河市'},
    {'name': '牡丹江', 'province': '黑龙江', 'full_name': '黑龙江省牡丹江市'},
    {'name': '黑河', 'province': '黑龙江', 'full_name': '黑龙江省黑河市'},
    {'name': '绥化', 'province': '黑龙江', 'full_name': '黑龙江省绥化市'},
    # 江苏省
    {'name': '南京', 'province': '江苏', 'full_name': '江苏省南京市'},
    {'name': '无锡', 'province': '江苏', 'full_name': '江苏省无锡市'},
    {'name': '徐州', 'province': '江苏', 'full_name': '江苏省徐州市'},
    {'name': '常州', 'province': '江苏', 'full_name': '江苏省常州市'},
    {'name': '苏州', 'province': '江苏', 'full_name': '江苏省苏州市'},
    {'name': '南通', 'province': '江苏', 'full_name': '江苏省南通市'},
    {'name': '连云港', 'province': '江苏', 'full_name': '江苏省连云港市'},
    {'name': '淮安', 'province': '江苏', 'full_name': '江苏省淮安市'},
    {'name': '盐城', 'province': '江苏', 'full_name': '江苏省盐城市'},
    {'name': '扬州', 'province': '江苏', 'full_name': '江苏省扬州市'},
    {'name': '镇江', 'province': '江苏', 'full_name': '江苏省镇江市'},
    {'name': '泰州', 'province': '江苏', 'full_name': '江苏省泰州市'},
    {'name': '宿迁', 'province': '江苏', 'full_name': '江苏省宿迁市'},
    # 浙江省
    {'name': '杭州', 'province': '浙江', 'full_name': '浙江省杭州市'},
    {'name': '宁波', 'province': '浙江', 'full_name': '浙江省宁波市'},
    {'name': '温州', 'province': '浙江', 'full_name': '浙江省温州市'},
    {'name': '嘉兴', 'province': '浙江', 'full_name': '浙江省嘉兴市'},
    {'name': '湖州', 'province': '浙江', 'full_name': '浙江省湖州市'},
    {'name': '绍兴', 'province': '浙江', 'full_name': '浙江省绍兴市'},
    {'name': '金华', 'province': '浙江', 'full_name': '浙江省金华市'},
    {'name': '衢州', 'province': '浙江', 'full_name': '浙江省衢州市'},
    {'name': '舟山', 'province': '浙江', 'full_name': '浙江省舟山市'},
    {'name': '台州', 'province': '浙江', 'full_name': '浙江省台州市'},
    {'name': '丽水', 'province': '浙江', 'full_name': '浙江省丽水市'},
    # 安徽省
    {'name': '合肥', 'province': '安徽', 'full_name': '安徽省合肥市'},
    {'name': '芜湖', 'province': '安徽', 'full_name': '安徽省芜湖市'},
    {'name': '蚌埠', 'province': '安徽', 'full_name': '安徽省蚌埠市'},
    {'name': '淮南', 'province': '安徽', 'full_name': '安徽省淮南市'},
    {'name': '马鞍山', 'province': '安徽', 'full_name': '安徽省马鞍山市'},
    {'name': '淮北', 'province': '安徽', 'full_name': '安徽省淮北市'},
    {'name': '铜陵', 'province': '安徽', 'full_name': '安徽省铜陵市'},
    {'name': '安庆', 'province': '安徽', 'full_name': '安徽省安庆市'},
    {'name': '黄山', 'province': '安徽', 'full_name': '安徽省黄山市'},
    {'name': '阜阳', 'province': '安徽', 'full_name': '安徽省阜阳市'},
    {'name': '宿州', 'province': '安徽', 'full_name': '安徽省宿州市'},
    {'name': '滁州', 'province': '安徽', 'full_name': '安徽省滁州市'},
    {'name': '六安', 'province': '安徽', 'full_name': '安徽省六安市'},
    {'name': '宣城', 'province': '安徽', 'full_name': '安徽省宣城市'},
    {'name': '池州', 'province': '安徽', 'full_name': '安徽省池州市'},
    {'name': '亳州', 'province': '安徽', 'full_name': '安徽省亳州市'},
    # 福建省
    {'name': '福州', 'province': '福建', 'full_name': '福建省福州市'},
    {'name': '厦门', 'province': '福建', 'full_name': '福建省厦门市'},
    {'name': '莆田', 'province': '福建', 'full_name': '福建省莆田市'},
    {'name': '三明', 'province': '福建', 'full_name': '福建省三明市'},
    {'name': '泉州', 'province': '福建', 'full_name': '福建省泉州市'},
    {'name': '漳州', 'province': '福建', 'full_name': '福建省漳州市'},
    {'name': '南平', 'province': '福建', 'full_name': '福建省南平市'},
    {'name': '龙岩', 'province': '福建', 'full_name': '福建省龙岩市'},
    {'name': '宁德', 'province': '福建', 'full_name': '福建省宁德市'},
    # 江西省
    {'name': '南昌', 'province': '江西', 'full_name': '江西省南昌市'},
    {'name': '景德镇', 'province': '江西', 'full_name': '江西省景德镇市'},
    {'name': '萍乡', 'province': '江西', 'full_name': '江西省萍乡市'},
    {'name': '九江', 'province': '江西', 'full_name': '江西省九江市'},
    {'name': '新余', 'province': '江西', 'full_name': '江西省新余市'},
    {'name': '鹰潭', 'province': '江西', 'full_name': '江西省鹰潭市'},
    {'name': '赣州', 'province': '江西', 'full_name': '江西省赣州市'},
    {'name': '吉安', 'province': '江西', 'full_name': '江西省吉安市'},
    {'name': '宜春', 'province': '江西', 'full_name': '江西省宜春市'},
    {'name': '抚州', 'province': '江西', 'full_name': '江西省抚州市'},
    {'name': '上饶', 'province': '江西', 'full_name': '江西省上饶市'},
    # 山东省
    {'name': '济南', 'province': '山东', 'full_name': '山东省济南市'},
    {'name': '青岛', 'province': '山东', 'full_name': '山东省青岛市'},
    {'name': '淄博', 'province': '山东', 'full_name': '山东省淄博市'},
    {'name': '枣庄', 'province': '山东', 'full_name': '山东省枣庄市'},
    {'name': '东营', 'province': '山东', 'full_name': '山东省东营市'},
    {'name': '烟台', 'province': '山东', 'full_name': '山东省烟台市'},
    {'name': '潍坊', 'province': '山东', 'full_name': '山东省潍坊市'},
    {'name': '济宁', 'province': '山东', 'full_name': '山东省济宁市'},
    {'name': '泰安', 'province': '山东', 'full_name': '山东省泰安市'},
    {'name': '威海', 'province': '山东', 'full_name': '山东省威海市'},
    {'name': '日照', 'province': '山东', 'full_name': '山东省日照市'},
    {'name': '临沂', 'province': '山东', 'full_name': '山东省临沂市'},
    {'name': '德州', 'province': '山东', 'full_name': '山东省德州市'},
    {'name': '聊城', 'province': '山东', 'full_name': '山东省聊城市'},
    {'name': '滨州', 'province': '山东', 'full_name': '山东省滨州市'},
    {'name': '菏泽', 'province': '山东', 'full_name': '山东省菏泽市'},
    # 河南省
    {'name': '郑州', 'province': '河南', 'full_name': '河南省郑州市'},
    {'name': '开封', 'province': '河南', 'full_name': '河南省开封市'},
    {'name': '洛阳', 'province': '河南', 'full_name': '河南省洛阳市'},
    {'name': '平顶山', 'province': '河南', 'full_name': '河南省平顶山市'},
    {'name': '安阳', 'province': '河南', 'full_name': '河南省安阳市'},
    {'name': '鹤壁', 'province': '河南', 'full_name': '河南省鹤壁市'},
    {'name': '新乡', 'province': '河南', 'full_name': '河南省新乡市'},
    {'name': '焦作', 'province': '河南', 'full_name': '河南省焦作市'},
    {'name': '濮阳', 'province': '河南', 'full_name': '河南省濮阳市'},
    {'name': '许昌', 'province': '河南', 'full_name': '河南省许昌市'},
    {'name': '漯河', 'province': '河南', 'full_name': '河南省漯河市'},
    {'name': '三门峡', 'province': '河南', 'full_name': '河南省三门峡市'},
    {'name': '南阳', 'province': '河南', 'full_name': '河南省南阳市'},
    {'name': '商丘', 'province': '河南', 'full_name': '河南省商丘市'},
    {'name': '信阳', 'province': '河南', 'full_name': '河南省信阳市'},
    {'name': '周口', 'province': '河南', 'full_name': '河南省周口市'},
    {'name': '驻马店', 'province': '河南', 'full_name': '河南省驻马店市'},
    # 湖北省
    {'name': '武汉', 'province': '湖北', 'full_name': '湖北省武汉市'},
    {'name': '黄石', 'province': '湖北', 'full_name': '湖北省黄石市'},
    {'name': '十堰', 'province': '湖北', 'full_name': '湖北省十堰市'},
    {'name': '宜昌', 'province': '湖北', 'full_name': '湖北省宜昌市'},
    {'name': '襄阳', 'province': '湖北', 'full_name': '湖北省襄阳市'},
    {'name': '鄂州', 'province': '湖北', 'full_name': '湖北省鄂州市'},
    {'name': '荆门', 'province': '湖北', 'full_name': '湖北省荆门市'},
    {'name': '孝感', 'province': '湖北', 'full_name': '湖北省孝感市'},
    {'name': '荆州', 'province': '湖北', 'full_name': '湖北省荆州市'},
    {'name': '黄冈', 'province': '湖北', 'full_name': '湖北省黄冈市'},
    {'name': '咸宁', 'province': '湖北', 'full_name': '湖北省咸宁市'},
    {'name': '随州', 'province': '湖北', 'full_name': '湖北省随州市'},
    # 湖南省
    {'name': '长沙', 'province': '湖南', 'full_name': '湖南省长沙市'},
    {'name': '株洲', 'province': '湖南', 'full_name': '湖南省株洲市'},
    {'name': '湘潭', 'province': '湖南', 'full_name': '湖南省湘潭市'},
    {'name': '衡阳', 'province': '湖南', 'full_name': '湖南省衡阳市'},
    {'name': '邵阳', 'province': '湖南', 'full_name': '湖南省邵阳市'},
    {'name': '岳阳', 'province': '湖南', 'full_name': '湖南省岳阳市'},
    {'name': '常德', 'province': '湖南', 'full_name': '湖南省常德市'},
    {'name': '张家界', 'province': '湖南', 'full_name': '湖南省张家界市'},
    {'name': '益阳', 'province': '湖南', 'full_name': '湖南省益阳市'},
    {'name': '郴州', 'province': '湖南', 'full_name': '湖南省郴州市'},
    {'name': '永州', 'province': '湖南', 'full_name': '湖南省永州市'},
    {'name': '怀化', 'province': '湖南', 'full_name': '湖南省怀化市'},
    {'name': '娄底', 'province': '湖南', 'full_name': '湖南省娄底市'},
    # 广东省
    {'name': '广州', 'province': '广东', 'full_name': '广东省广州市'},
    {'name': '韶关', 'province': '广东', 'full_name': '广东省韶关市'},
    {'name': '深圳', 'province': '广东', 'full_name': '广东省深圳市'},
    {'name': '珠海', 'province': '广东', 'full_name': '广东省珠海市'},
    {'name': '汕头', 'province': '广东', 'full_name': '广东省汕头市'},
    {'name': '佛山', 'province': '广东', 'full_name': '广东省佛山市'},
    {'name': '江门', 'province': '广东', 'full_name': '广东省江门市'},
    {'name': '湛江', 'province': '广东', 'full_name': '广东省湛江市'},
    {'name': '茂名', 'province': '广东', 'full_name': '广东省茂名市'},
    {'name': '肇庆', 'province': '广东', 'full_name': '广东省肇庆市'},
    {'name': '惠州', 'province': '广东', 'full_name': '广东省惠州市'},
    {'name': '梅州', 'province': '广东', 'full_name': '广东省梅州市'},
    {'name': '汕尾', 'province': '广东', 'full_name': '广东省汕尾市'},
    {'name': '河源', 'province': '广东', 'full_name': '广东省河源市'},
    {'name': '阳江', 'province': '广东', 'full_name': '广东省阳江市'},
    {'name': '清远', 'province': '广东', 'full_name': '广东省清远市'},
    {'name': '东莞', 'province': '广东', 'full_name': '广东省东莞市'},
    {'name': '中山', 'province': '广东', 'full_name': '广东省中山市'},
    {'name': '潮州', 'province': '广东', 'full_name': '广东省潮州市'},
    {'name': '揭阳', 'province': '广东', 'full_name': '广东省揭阳市'},
    {'name': '云浮', 'province': '广东', 'full_name': '广东省云浮市'},
    # 广西
    {'name': '南宁', 'province': '广西', 'full_name': '广西南宁市'},
    {'name': '柳州', 'province': '广西', 'full_name': '广西柳州市'},
    {'name': '桂林', 'province': '广西', 'full_name': '广西桂林市'},
    {'name': '梧州', 'province': '广西', 'full_name': '广西梧州市'},
    {'name': '北海', 'province': '广西', 'full_name': '广西北海市'},
    {'name': '防城港', 'province': '广西', 'full_name': '广西防城港市'},
    {'name': '钦州', 'province': '广西', 'full_name': '广西钦州市'},
    {'name': '贵港', 'province': '广西', 'full_name': '广西贵港市'},
    {'name': '玉林', 'province': '广西', 'full_name': '广西玉林市'},
    {'name': '百色', 'province': '广西', 'full_name': '广西百色市'},
    {'name': '贺州', 'province': '广西', 'full_name': '广西贺州市'},
    {'name': '河池', 'province': '广西', 'full_name': '广西河池市'},
    {'name': '来宾', 'province': '广西', 'full_name': '广西来宾市'},
    {'name': '崇左', 'province': '广西', 'full_name': '广西崇左市'},
    # 海南省
    {'name': '海口', 'province': '海南', 'full_name': '海南省海口市'},
    {'name': '三亚', 'province': '海南', 'full_name': '海南省三亚市'},
    {'name': '三沙', 'province': '海南', 'full_name': '海南省三沙市'},
    {'name': '儋州', 'province': '海南', 'full_name': '海南省儋州市'},
    # 四川省
    {'name': '成都', 'province': '四川', 'full_name': '四川省成都市'},
    {'name': '自贡', 'province': '四川', 'full_name': '四川省自贡市'},
    {'name': '攀枝花', 'province': '四川', 'full_name': '四川省攀枝花市'},
    {'name': '泸州', 'province': '四川', 'full_name': '四川省泸州市'},
    {'name': '德阳', 'province': '四川', 'full_name': '四川省德阳市'},
    {'name': '绵阳', 'province': '四川', 'full_name': '四川省绵阳市'},
    {'name': '广元', 'province': '四川', 'full_name': '四川省广元市'},
    {'name': '遂宁', 'province': '四川', 'full_name': '四川省遂宁市'},
    {'name': '内江', 'province': '四川', 'full_name': '四川省内江市'},
    {'name': '乐山', 'province': '四川', 'full_name': '四川省乐山市'},
    {'name': '南充', 'province': '四川', 'full_name': '四川省南充市'},
    {'name': '眉山', 'province': '四川', 'full_name': '四川省眉山市'},
    {'name': '宜宾', 'province': '四川', 'full_name': '四川省宜宾市'},
    {'name': '广安', 'province': '四川', 'full_name': '四川省广安市'},
    {'name': '达州', 'province': '四川', 'full_name': '四川省达州市'},
    {'name': '雅安', 'province': '四川', 'full_name': '四川省雅安市'},
    {'name': '巴中', 'province': '四川', 'full_name': '四川省巴中市'},
    {'name': '资阳', 'province': '四川', 'full_name': '四川省资阳市'},
    # 贵州省
    {'name': '贵阳', 'province': '贵州', 'full_name': '贵州省贵阳市'},
    {'name': '六盘水', 'province': '贵州', 'full_name': '贵州省六盘水市'},
    {'name': '遵义', 'province': '贵州', 'full_name': '贵州省遵义市'},
    {'name': '安顺', 'province': '贵州', 'full_name': '贵州省安顺市'},
    {'name': '毕节', 'province': '贵州', 'full_name': '贵州省毕节市'},
    {'name': '铜仁', 'province': '贵州', 'full_name': '贵州省铜仁市'},
    # 云南省
    {'name': '昆明', 'province': '云南', 'full_name': '云南省昆明市'},
    {'name': '曲靖', 'province': '云南', 'full_name': '云南省曲靖市'},
    {'name': '玉溪', 'province': '云南', 'full_name': '云南省玉溪市'},
    {'name': '保山', 'province': '云南', 'full_name': '云南省保山市'},
    {'name': '昭通', 'province': '云南', 'full_name': '云南省昭通市'},
    {'name': '丽江', 'province': '云南', 'full_name': '云南省丽江市'},
    {'name': '普洱', 'province': '云南', 'full_name': '云南省普洱市'},
    {'name': '临沧', 'province': '云南', 'full_name': '云南省临沧市'},
    # 西藏
    {'name': '拉萨', 'province': '西藏', 'full_name': '西藏拉萨市'},
    {'name': '日喀则', 'province': '西藏', 'full_name': '西藏日喀则市'},
    {'name': '昌都', 'province': '西藏', 'full_name': '西藏昌都市'},
    {'name': '林芝', 'province': '西藏', 'full_name': '西藏林芝市'},
    {'name': '山南', 'province': '西藏', 'full_name': '西藏山南市'},
    {'name': '那曲', 'province': '西藏', 'full_name': '西藏那曲市'},
    # 陕西省
    {'name': '西安', 'province': '陕西', 'full_name': '陕西省西安市'},
    {'name': '铜川', 'province': '陕西', 'full_name': '陕西省铜川市'},
    {'name': '宝鸡', 'province': '陕西', 'full_name': '陕西省宝鸡市'},
    {'name': '咸阳', 'province': '陕西', 'full_name': '陕西省咸阳市'},
    {'name': '渭南', 'province': '陕西', 'full_name': '陕西省渭南市'},
    {'name': '延安', 'province': '陕西', 'full_name': '陕西省延安市'},
    {'name': '汉中', 'province': '陕西', 'full_name': '陕西省汉中市'},
    {'name': '榆林', 'province': '陕西', 'full_name': '陕西省榆林市'},
    {'name': '安康', 'province': '陕西', 'full_name': '陕西省安康市'},
    {'name': '商洛', 'province': '陕西', 'full_name': '陕西省商洛市'},
    # 甘肃省
    {'name': '兰州', 'province': '甘肃', 'full_name': '甘肃省兰州市'},
    {'name': '嘉峪关', 'province': '甘肃', 'full_name': '甘肃省嘉峪关市'},
    {'name': '金昌', 'province': '甘肃', 'full_name': '甘肃省金昌市'},
    {'name': '白银', 'province': '甘肃', 'full_name': '甘肃省白银市'},
    {'name': '天水', 'province': '甘肃', 'full_name': '甘肃省天水市'},
    {'name': '武威', 'province': '甘肃', 'full_name': '甘肃省武威市'},
    {'name': '张掖', 'province': '甘肃', 'full_name': '甘肃省张掖市'},
    {'name': '平凉', 'province': '甘肃', 'full_name': '甘肃省平凉市'},
    {'name': '酒泉', 'province': '甘肃', 'full_name': '甘肃省酒泉市'},
    {'name': '庆阳', 'province': '甘肃', 'full_name': '甘肃省庆阳市'},
    {'name': '定西', 'province': '甘肃', 'full_name': '甘肃省定西市'},
    {'name': '陇南', 'province': '甘肃', 'full_name': '甘肃省陇南市'},
    # 青海省
    {'name': '西宁', 'province': '青海', 'full_name': '青海省西宁市'},
    {'name': '海东', 'province': '青海', 'full_name': '青海省海东市'},
    # 宁夏
    {'name': '银川', 'province': '宁夏', 'full_name': '宁夏银川市'},
    {'name': '石嘴山', 'province': '宁夏', 'full_name': '宁夏石嘴山市'},
    {'name': '吴忠', 'province': '宁夏', 'full_name': '宁夏吴忠市'},
    {'name': '固原', 'province': '宁夏', 'full_name': '宁夏固原市'},
    {'name': '中卫', 'province': '宁夏', 'full_name': '宁夏中卫市'},
    # 新疆
    {'name': '乌鲁木齐', 'province': '新疆', 'full_name': '新疆乌鲁木齐市'},
    {'name': '克拉玛依', 'province': '新疆', 'full_name': '新疆克拉玛依市'},
    {'name': '吐鲁番', 'province': '新疆', 'full_name': '新疆吐鲁番市'},
    {'name': '哈密', 'province': '新疆', 'full_name': '新疆哈密市'},
    # 特别行政区
    {'name': '香港', 'province': '香港', 'full_name': '香港特别行政区'},
    {'name': '澳门', 'province': '澳门', 'full_name': '澳门特别行政区'},
    # 台湾省
    {'name': '台北', 'province': '台湾', 'full_name': '台湾省台北市'},
    {'name': '新北', 'province': '台湾', 'full_name': '台湾省新北市'},
    {'name': '桃园', 'province': '台湾', 'full_name': '台湾省桃园市'},
    {'name': '台中', 'province': '台湾', 'full_name': '台湾省台中市'},
    {'name': '台南', 'province': '台湾', 'full_name': '台湾省台南市'},
    {'name': '高雄', 'province': '台湾', 'full_name': '台湾省高雄市'},
]


# 省份列表
PROVINCES = [
    '北京', '天津', '上海', '重庆',
    '河北', '山西', '内蒙古', '辽宁', '吉林', '黑龙江',
    '江苏', '浙江', '安徽', '福建', '江西', '山东',
    '河南', '湖北', '湖南', '广东', '广西', '海南',
    '四川', '贵州', '云南', '西藏', '陕西', '甘肃',
    '青海', '宁夏', '新疆', '香港', '澳门', '台湾',
]


def search_cities(query: str, limit: int = 10) -> List[CityInfo]:
    """
    搜索城市
    
    Args:
        query: 搜索关键词
        limit: 最大返回数量
        
    Returns:
        匹配的城市列表
    """
    if not query or not query.strip():
        return []
    
    normalized = query.strip().lower()
    
    results = [
        city for city in CHINA_CITIES
        if normalized in city['name'].lower()
        or normalized in city['province'].lower()
        or normalized in city['full_name'].lower()
    ]
    
    return results[:limit]


def get_cities_by_province(province: str) -> List[CityInfo]:
    """
    获取指定省份的所有城市
    
    Args:
        province: 省份名称
        
    Returns:
        该省份的城市列表
    """
    return [city for city in CHINA_CITIES if city['province'] == province]


def get_city_by_name(name: str) -> Optional[CityInfo]:
    """
    根据城市名获取城市信息
    
    Args:
        name: 城市名称
        
    Returns:
        城市信息，未找到返回None
    """
    for city in CHINA_CITIES:
        if city['name'] == name:
            return city
    return None


# 导出
__all__ = [
    'CityInfo',
    'CHINA_CITIES',
    'PROVINCES',
    'search_cities',
    'get_cities_by_province',
    'get_city_by_name',
]
