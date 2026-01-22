/**
 * 免责声明页面
 * 包含信息准确性免责、外部链接责任声明、版权声明、用户责任条款
 */

import { Link } from 'react-router-dom'
import { ArrowLeft, Shield, AlertTriangle, Link2, Copyright, Users, Scale, Info } from 'lucide-react'
import SEOHead from '@/components/SEOHead'

export default function DisclaimerPage() {
    return (
        <>
            <SEOHead
                title="免责声明"
                description="AI占卜平台免责声明，了解服务的娱乐性质和使用限制"
                keywords="免责声明,娱乐声明,使用须知"
            />
            <div className="space-y-8 pb-12">
                {/* 返回导航 */}
                <Link
                    to="/"
                    className="inline-flex items-center gap-2 text-sm text-muted-foreground hover:text-foreground transition-colors"
                >
                    <ArrowLeft className="w-4 h-4" />
                    返回首页
                </Link>

                {/* 页面标题 */}
                <div className="space-y-4">
                    <div className="flex items-center gap-3">
                        <div className="p-3 rounded-xl bg-amber-500/10">
                            <Shield className="w-8 h-8 text-amber-500" />
                        </div>
                        <div>
                            <h1 className="text-3xl font-bold text-foreground">免责声明</h1>
                            <p className="text-muted-foreground">最后更新：2024年12月</p>
                        </div>
                    </div>
                </div>

                {/* 重要提示横幅 */}
                <div className="p-6 rounded-xl bg-gradient-to-r from-amber-50 to-orange-50 dark:from-amber-900/30 dark:to-orange-900/30 border border-amber-200 dark:border-amber-800">
                    <div className="flex items-start gap-4">
                        <AlertTriangle className="w-8 h-8 text-amber-500 flex-shrink-0 mt-1" />
                        <div>
                            <h2 className="text-xl font-bold text-amber-800 dark:text-amber-200 mb-2">
                                重要：娱乐性质声明
                            </h2>
                            <p className="text-amber-700 dark:text-amber-300">
                                AI 占卜平台提供的所有服务、分析结果和内容<strong>仅供娱乐和文化研究目的</strong>。
                                我们的服务基于传统文化元素，结合人工智能技术生成内容，<strong>不具备任何科学依据</strong>，
                                不能也不应被视为对未来的预测或对现实的准确描述。
                            </p>
                        </div>
                    </div>
                </div>

                {/* 免责声明内容 */}
                <div className="prose prose-sm dark:prose-invert max-w-none space-y-8">
                    {/* 1. 信息准确性免责 */}
                    <section className="p-6 rounded-xl bg-card border border-border">
                        <h2 className="text-xl font-bold text-foreground flex items-center gap-2 mt-0">
                            <Info className="w-6 h-6 text-blue-500" />
                            信息准确性免责
                        </h2>
                        <div className="space-y-4 text-muted-foreground">
                            <p>
                                本网站提供的所有信息、分析结果和建议均基于人工智能算法和传统文化数据库生成，
                                <strong>不保证其准确性、完整性、可靠性或适用性</strong>。
                            </p>
                            <div className="p-4 rounded-lg bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800">
                                <h4 className="font-semibold text-blue-800 dark:text-blue-200 mb-2">具体说明：</h4>
                                <ul className="list-disc list-inside text-blue-700 dark:text-blue-300 space-y-1 text-sm">
                                    <li>塔罗牌占卜结果为随机生成的娱乐内容</li>
                                    <li>生辰八字分析基于传统历法推算，仅供文化参考</li>
                                    <li>紫微斗数排盘为传统术数的数字化呈现</li>
                                    <li>周公解梦内容来源于传统典籍，不具备心理学意义</li>
                                    <li>姓名测算基于传统五格数理，属于民俗文化范畴</li>
                                    <li>所有 AI 生成的解读内容可能存在偏差或不准确之处</li>
                                </ul>
                            </div>
                            <p className="text-sm">
                                用户应自行判断和评估所获取信息的价值和适用性。
                                我们不对任何因依赖本网站信息而导致的损失或损害承担责任。
                            </p>
                        </div>
                    </section>

                    {/* 2. 不构成专业建议 */}
                    <section className="p-6 rounded-xl bg-card border border-border">
                        <h2 className="text-xl font-bold text-foreground flex items-center gap-2 mt-0">
                            <AlertTriangle className="w-6 h-6 text-red-500" />
                            不构成专业建议
                        </h2>
                        <div className="p-4 rounded-lg bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 mb-4">
                            <p className="text-red-700 dark:text-red-300 font-semibold mb-2">
                                本网站内容不构成以下任何形式的专业建议：
                            </p>
                            <div className="grid gap-2 md:grid-cols-2">
                                {[
                                    { icon: '🏥', text: '医疗诊断或健康建议' },
                                    { icon: '💰', text: '投资建议或财务规划' },
                                    { icon: '⚖️', text: '法律意见或法律咨询' },
                                    { icon: '💑', text: '婚姻指导或情感咨询' },
                                    { icon: '🧠', text: '心理咨询或心理治疗' },
                                    { icon: '💼', text: '职业规划或就业指导' },
                                    { icon: '🎓', text: '教育规划或升学建议' },
                                    { icon: '🏠', text: '房产投资或购房决策' }
                                ].map((item, index) => (
                                    <div key={index} className="flex items-center gap-2 p-2 bg-red-100/50 dark:bg-red-900/30 rounded">
                                        <span>{item.icon}</span>
                                        <span className="text-sm text-red-600 dark:text-red-400">{item.text}</span>
                                    </div>
                                ))}
                            </div>
                        </div>
                        <p className="text-muted-foreground">
                            如需上述领域的专业帮助，请咨询具有相关资质的专业人士。
                            <strong>切勿将本网站内容作为任何重要决策的依据。</strong>
                        </p>
                    </section>

                    {/* 3. 外部链接责任声明 */}
                    <section className="p-6 rounded-xl bg-card border border-border">
                        <h2 className="text-xl font-bold text-foreground flex items-center gap-2 mt-0">
                            <Link2 className="w-6 h-6 text-purple-500" />
                            外部链接责任声明
                        </h2>
                        <div className="space-y-4 text-muted-foreground">
                            <p>
                                本网站可能包含指向第三方网站或服务的链接。这些链接仅为方便用户而提供。
                            </p>
                            <ul className="list-disc list-inside space-y-1">
                                <li>我们不控制第三方网站的内容、隐私政策或做法</li>
                                <li>我们不对第三方网站的准确性、合法性或适当性负责</li>
                                <li>访问外部链接的风险由用户自行承担</li>
                                <li>我们建议用户在离开本网站时查阅目标网站的条款和隐私政策</li>
                            </ul>
                            <p className="text-sm">
                                包含外部链接并不意味着我们认可该网站或其内容，也不代表我们与该网站存在任何关联。
                            </p>
                        </div>
                    </section>

                    {/* 4. 版权声明 */}
                    <section className="p-6 rounded-xl bg-card border border-border">
                        <h2 className="text-xl font-bold text-foreground flex items-center gap-2 mt-0">
                            <Copyright className="w-6 h-6 text-green-500" />
                            版权声明
                        </h2>
                        <div className="space-y-4 text-muted-foreground">
                            <p>
                                本网站的所有原创内容、设计、图形、界面、代码和其他知识产权均受法律保护。
                            </p>
                            <div className="p-4 rounded-lg bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800">
                                <h4 className="font-semibold text-green-800 dark:text-green-200 mb-2">使用限制：</h4>
                                <ul className="list-disc list-inside text-green-700 dark:text-green-300 space-y-1 text-sm">
                                    <li>未经书面许可，禁止复制、修改、分发本网站内容</li>
                                    <li>禁止将本网站内容用于商业目的</li>
                                    <li>禁止创建基于本网站的衍生作品</li>
                                    <li>禁止使用自动化工具批量抓取网站内容</li>
                                </ul>
                            </div>
                            <p className="text-sm">
                                部分内容可能来源于公共领域的传统文化资料，这些内容的原始版权归属于公共领域或原作者。
                            </p>
                        </div>
                    </section>

                    {/* 5. 用户责任条款 */}
                    <section className="p-6 rounded-xl bg-card border border-border">
                        <h2 className="text-xl font-bold text-foreground flex items-center gap-2 mt-0">
                            <Users className="w-6 h-6 text-orange-500" />
                            用户责任条款
                        </h2>
                        <div className="space-y-4 text-muted-foreground">
                            <p>使用本网站服务，即表示您同意承担以下责任：</p>
                            <div className="grid gap-3">
                                {[
                                    {
                                        title: '理性看待分析结果',
                                        desc: '将所有分析结果视为娱乐内容，不作为实际决策依据'
                                    },
                                    {
                                        title: '自主决策责任',
                                        desc: '您对基于本网站内容做出的任何决策承担完全责任'
                                    },
                                    {
                                        title: '合法使用服务',
                                        desc: '不得将服务用于非法目的或传播迷信内容'
                                    },
                                    {
                                        title: '保护个人信息',
                                        desc: '妥善保管账户信息，对账户活动负责'
                                    },
                                    {
                                        title: '遵守使用规范',
                                        desc: '不得滥用、攻击或干扰本网站的正常运行'
                                    }
                                ].map((item, index) => (
                                    <div key={index} className="p-4 rounded-lg bg-muted/50 flex gap-4">
                                        <div className="w-8 h-8 rounded-full bg-orange-500/10 flex items-center justify-center flex-shrink-0">
                                            <span className="text-orange-500 font-bold">{index + 1}</span>
                                        </div>
                                        <div>
                                            <h4 className="font-semibold text-foreground">{item.title}</h4>
                                            <p className="text-sm text-muted-foreground">{item.desc}</p>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>
                    </section>

                    {/* 6. 服务可用性 */}
                    <section className="p-6 rounded-xl bg-card border border-border">
                        <h2 className="text-xl font-bold text-foreground flex items-center gap-2 mt-0">
                            <Scale className="w-6 h-6 text-indigo-500" />
                            服务可用性与责任限制
                        </h2>
                        <div className="space-y-4 text-muted-foreground">
                            <p>我们致力于提供稳定的服务，但：</p>
                            <ul className="list-disc list-inside space-y-1">
                                <li>我们不保证服务的持续可用性或无中断运行</li>
                                <li>我们可能因维护、升级或其他原因暂停服务</li>
                                <li>我们不对服务中断造成的任何损失负责</li>
                                <li>我们保留随时修改、暂停或终止服务的权利</li>
                            </ul>
                            <div className="p-4 rounded-lg bg-indigo-50 dark:bg-indigo-900/20 border border-indigo-200 dark:border-indigo-800">
                                <p className="text-indigo-700 dark:text-indigo-300 text-sm">
                                    <strong>责任上限：</strong>在法律允许的最大范围内，我们对任何直接、间接、
                                    附带、特殊、惩罚性或后果性损害不承担责任，无论这些损害是否可预见。
                                </p>
                            </div>
                        </div>
                    </section>

                    {/* 7. 声明更新 */}
                    <section className="p-6 rounded-xl bg-card border border-border">
                        <h2 className="text-xl font-bold text-foreground flex items-center gap-2 mt-0">
                            <Shield className="w-6 h-6 text-primary" />
                            声明更新
                        </h2>
                        <p className="text-muted-foreground">
                            本免责声明可能会不定期更新，以反映服务变化或法律要求。
                            更新后的声明将在本页面发布，并标注最新更新日期。
                            继续使用本网站服务即表示您接受更新后的免责声明。
                        </p>
                        <p className="text-muted-foreground mt-4">
                            我们建议您定期查阅本页面，以了解最新的免责声明内容。
                        </p>
                    </section>

                    {/* 联系方式 */}
                    <section className="p-6 rounded-xl bg-primary/5 border border-primary/20">
                        <h2 className="text-xl font-bold text-foreground mt-0">联系我们</h2>
                        <p className="text-muted-foreground">
                            如果您对本免责声明有任何疑问，请联系我们：
                        </p>
                        <p className="text-foreground mt-2">
                            电子邮件：<a href="mailto:181593130@qq.com" className="text-primary hover:underline">181593130@qq.com</a>
                        </p>
                    </section>

                    {/* 最终提示 */}
                    <div className="text-center p-6 bg-gradient-to-r from-amber-50 to-orange-50 dark:from-amber-900/20 dark:to-orange-900/20 rounded-xl border border-amber-200 dark:border-amber-800">
                        <AlertTriangle className="w-12 h-12 text-amber-500 mx-auto mb-4" />
                        <p className="text-lg font-bold text-amber-800 dark:text-amber-200 mb-2">
                            请记住
                        </p>
                        <p className="text-amber-700 dark:text-amber-300">
                            本网站所有内容仅供娱乐与文化研究，不具备科学依据。<br />
                            <strong>命运掌握在您自己手中，请勿迷信。</strong>
                        </p>
                    </div>
                </div>
            </div>
        </>
    )
}
