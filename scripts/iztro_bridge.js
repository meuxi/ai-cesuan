/**
 * iztro 桥接服务
 * 提供准确的紫微斗数计算，供Python后端调用
 * 
 * 使用方式：
 * node iztro_bridge.js '{"year":1990,"month":5,"day":15,"hour":10,"gender":"male"}'
 */

const { astro } = require('iztro');

// 时辰映射（小时 -> 时辰索引）
const HOUR_TO_INDEX = {
    0: 0, 1: 1, 2: 1, 3: 2, 4: 2, 5: 3, 6: 3, 7: 4, 8: 4, 9: 5, 10: 5, 11: 6,
    12: 6, 13: 7, 14: 7, 15: 8, 16: 8, 17: 9, 18: 9, 19: 10, 20: 10, 21: 11, 22: 11, 23: 12
};

// 四化对照表
const MUTAGEN_MAP = {
    '甲': { lu: '廉贞', quan: '破军', ke: '武曲', ji: '太阳' },
    '乙': { lu: '天机', quan: '天梁', ke: '紫微', ji: '太阴' },
    '丙': { lu: '天同', quan: '天机', ke: '文昌', ji: '廉贞' },
    '丁': { lu: '太阴', quan: '天同', ke: '天机', ji: '巨门' },
    '戊': { lu: '贪狼', quan: '太阴', ke: '右弼', ji: '天机' },
    '己': { lu: '武曲', quan: '贪狼', ke: '天梁', ji: '文曲' },
    '庚': { lu: '太阳', quan: '武曲', ke: '太阴', ji: '天同' },
    '辛': { lu: '巨门', quan: '太阳', ke: '文曲', ji: '文昌' },
    '壬': { lu: '天梁', quan: '紫微', ke: '左辅', ji: '武曲' },
    '癸': { lu: '破军', quan: '巨门', ke: '太阴', ji: '贪狼' }
};

function calculate(input) {
    try {
        const { year, month, day, hour, gender, language = 'zh-CN' } = input;

        // 格式化日期
        const dateStr = `${year}-${String(month).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
        const hourIndex = HOUR_TO_INDEX[hour] || 0;
        const genderCN = gender === 'male' ? '男' : '女';

        // 创建命盘
        const astrolabe = astro.bySolar(dateStr, hourIndex, genderCN, false, language);

        if (!astrolabe) {
            throw new Error('创建命盘失败');
        }

        // 提取四柱
        const rawDates = astrolabe.rawDates;
        const fourPillars = {
            year: {
                stem: rawDates?.chineseDate?.yearly?.[0] || '',
                branch: rawDates?.chineseDate?.yearly?.[1] || ''
            },
            month: {
                stem: rawDates?.chineseDate?.monthly?.[0] || '',
                branch: rawDates?.chineseDate?.monthly?.[1] || ''
            },
            day: {
                stem: rawDates?.chineseDate?.daily?.[0] || '',
                branch: rawDates?.chineseDate?.daily?.[1] || ''
            },
            hour: {
                stem: rawDates?.chineseDate?.hourly?.[0] || '',
                branch: rawDates?.chineseDate?.hourly?.[1] || ''
            }
        };

        // 提取宫位
        const palaces = (astrolabe.palaces || []).map((palace, index) => {
            // 提取主星
            const majorStars = (palace.majorStars || []).map(star => ({
                name: star.name || '',
                brightness: star.brightness || '',
                type: 'major',
                mutagen: star.mutagen ? [star.mutagen] : []
            }));

            // 提取辅星
            const minorStars = (palace.minorStars || []).map(star => ({
                name: star.name || '',
                brightness: '',
                type: star.type || 'minor',
                mutagen: star.mutagen ? [star.mutagen] : []
            }));

            // 提取杂曜
            const adjectiveStars = (palace.adjectiveStars || []).map(star => ({
                name: star.name || '',
                brightness: '',
                type: 'auxiliary',
                mutagen: []
            }));

            return {
                name: palace.name || '',
                index: index,
                position: index,
                earthlyBranch: palace.earthlyBranch || '',
                heavenlyStem: palace.heavenlyStem || '',
                majorStars: majorStars,
                minorStars: [...minorStars, ...adjectiveStars],
                isBodyPalace: palace.isBodyPalace || false,
                extras: {
                    changsheng12: palace.changsheng12 || null,
                    boshi12: palace.boshi12 || null,
                    jiangqian12: palace.jiangqian12 || null,
                    suiqian12: palace.suiqian12 || null,
                    ages: palace.ages || null
                }
            };
        });

        // 提取农历日期
        const lunarDate = {
            year: rawDates?.lunarDate?.lunarYear || 0,
            month: rawDates?.lunarDate?.lunarMonth || 0,
            day: rawDates?.lunarDate?.lunarDay || 0,
            isLeapMonth: rawDates?.lunarDate?.isLeap || false
        };

        // 提取四化信息
        const yearStem = fourPillars.year.stem;
        const mutagenInfo = {
            natal: MUTAGEN_MAP[yearStem] || { lu: '', quan: '', ke: '', ji: '' },
            combined: {}
        };

        // 计算运限信息（当前日期时间）
        const now = new Date();
        const currentYear = now.getFullYear();
        const currentMonth = now.getMonth() + 1;
        const currentDay = now.getDate();
        const currentHour = now.getHours();
        const currentDateStr = `${currentYear}-${String(currentMonth).padStart(2, '0')}-${String(currentDay).padStart(2, '0')}`;
        const currentHourIndex = HOUR_TO_INDEX[currentHour] || 0;
        
        let horoscopeData = null;
        try {
            // 使用精确时间获取完整运限（大限/小限/流年/流月/流日/流时）
            const horoscope = astrolabe.horoscope(currentDateStr, currentHourIndex);
            if (horoscope) {
                horoscopeData = {
                    lunarDate: horoscope.lunarDate || null,
                    solarDate: horoscope.solarDate || currentDateStr,
                    // 大限
                    decadal: horoscope.decadal ? {
                        index: horoscope.decadal.index,
                        name: horoscope.decadal.name,
                        heavenlyStem: horoscope.decadal.heavenlyStem,
                        earthlyBranch: horoscope.decadal.earthlyBranch,
                        range: horoscope.decadal.range || [],
                        palaceNames: horoscope.decadal.palaceNames || [],
                        mutagen: horoscope.decadal.mutagen || [],
                        stars: horoscope.decadal.stars || []
                    } : null,
                    // 小限
                    age: horoscope.age ? {
                        index: horoscope.age.index,
                        nominalAge: horoscope.age.nominalAge
                    } : null,
                    // 流年
                    yearly: horoscope.yearly ? {
                        index: horoscope.yearly.index,
                        name: horoscope.yearly.name,
                        heavenlyStem: horoscope.yearly.heavenlyStem,
                        earthlyBranch: horoscope.yearly.earthlyBranch,
                        palaceNames: horoscope.yearly.palaceNames || [],
                        mutagen: horoscope.yearly.mutagen || [],
                        stars: horoscope.yearly.stars || []
                    } : null,
                    // 流月
                    monthly: horoscope.monthly ? {
                        index: horoscope.monthly.index,
                        name: horoscope.monthly.name,
                        heavenlyStem: horoscope.monthly.heavenlyStem,
                        earthlyBranch: horoscope.monthly.earthlyBranch,
                        palaceNames: horoscope.monthly.palaceNames || [],
                        mutagen: horoscope.monthly.mutagen || [],
                        stars: horoscope.monthly.stars || []
                    } : null,
                    // 流日
                    daily: horoscope.daily ? {
                        index: horoscope.daily.index,
                        name: horoscope.daily.name,
                        heavenlyStem: horoscope.daily.heavenlyStem,
                        earthlyBranch: horoscope.daily.earthlyBranch,
                        palaceNames: horoscope.daily.palaceNames || [],
                        mutagen: horoscope.daily.mutagen || [],
                        stars: horoscope.daily.stars || []
                    } : null,
                    // 流时
                    hourly: horoscope.hourly ? {
                        index: horoscope.hourly.index,
                        name: horoscope.hourly.name,
                        heavenlyStem: horoscope.hourly.heavenlyStem,
                        earthlyBranch: horoscope.hourly.earthlyBranch,
                        palaceNames: horoscope.hourly.palaceNames || [],
                        mutagen: horoscope.hourly.mutagen || [],
                        stars: horoscope.hourly.stars || []
                    } : null
                };
            }
        } catch (e) {
            // 运限计算失败不影响主流程
            console.error('运限计算失败:', e.message);
        }

        // 构建返回结果
        const result = {
            success: true,
            basicInfo: {
                zodiac: astrolabe.zodiac || '',
                constellation: astrolabe.sign || '',
                fourPillars: fourPillars,
                fiveElement: astrolabe.fiveElementsClass || '',
                soul: String(astrolabe.soul || ''),
                body: String(astrolabe.body || '')
            },
            solarDate: dateStr,
            lunarDate: lunarDate,
            palaces: palaces,
            mutagenInfo: mutagenInfo,
            horoscope: horoscopeData,
            gender: gender,
            birthYear: year,
            language: language
        };

        return result;

    } catch (error) {
        return {
            success: false,
            error: error.message || '计算失败'
        };
    }
}

// 主入口
if (require.main === module) {
    const args = process.argv.slice(2);

    if (args.length === 0) {
        console.error(JSON.stringify({ success: false, error: '缺少输入参数' }));
        process.exit(1);
    }

    try {
        const input = JSON.parse(args[0]);
        const result = calculate(input);
        console.log(JSON.stringify(result));
    } catch (e) {
        console.error(JSON.stringify({ success: false, error: `解析输入失败: ${e.message}` }));
        process.exit(1);
    }
}

module.exports = { calculate };
