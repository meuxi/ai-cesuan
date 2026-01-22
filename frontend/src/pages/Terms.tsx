/**
 * 服务条款页面
 * 根据模板定制，适配 AI 占卜网站
 */

import { Link } from 'react-router-dom'
import { ArrowLeft, FileText, Shield, Users, Scale, CreditCard, AlertTriangle } from 'lucide-react'
import SEOHead from '@/components/SEOHead'

export default function TermsPage() {
    return (
        <>
            <SEOHead
                title="服务条款"
                description="AI占卜平台服务条款，了解使用我们服务的条件和规则"
                keywords="服务条款,使用条款,用户协议"
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
                        <div className="p-3 rounded-xl bg-primary/10">
                            <FileText className="w-8 h-8 text-primary" />
                        </div>
                        <div>
                            <h1 className="text-3xl font-bold text-foreground">服务条款</h1>
                            <p className="text-muted-foreground">最后更新：2024年12月</p>
                        </div>
                    </div>
                </div>

                {/* 条款内容 */}
                <div className="prose prose-sm dark:prose-invert max-w-none space-y-8">
                    {/* 1. 简介 */}
                    <section className="p-6 rounded-xl bg-card border border-border">
                        <h2 className="text-xl font-bold text-foreground flex items-center gap-2 mt-0">
                            <span className="w-8 h-8 rounded-full bg-primary/10 flex items-center justify-center text-primary text-sm font-bold">1</span>
                            简介
                        </h2>
                        <p className="text-muted-foreground">
                            欢迎使用 AI 占卜平台。通过访问或使用我们的网站和服务，您同意受这些服务条款的约束。
                            如果您不同意这些条款的任何部分，您不允许访问网站或使用我们的服务。
                        </p>
                    </section>

                    {/* 2. 服务说明与娱乐性质声明 */}
                    <section className="p-6 rounded-xl bg-card border border-border">
                        <h2 className="text-xl font-bold text-foreground flex items-center gap-2 mt-0">
                            <span className="w-8 h-8 rounded-full bg-primary/10 flex items-center justify-center text-primary text-sm font-bold">2</span>
                            服务说明与娱乐性质声明
                        </h2>
                        <p className="text-muted-foreground mb-4">
                            AI 占卜是一个基于人工智能的<strong>娱乐工具</strong>，提供基于传统文化元素的内容生成服务。我们的服务包括：
                        </p>
                        <ul className="list-disc list-inside text-muted-foreground space-y-1 mb-4">
                            <li>塔罗牌占卜（娱乐性质）</li>
                            <li>生辰八字分析（娱乐性质）</li>
                            <li>紫微斗数排盘（娱乐性质）</li>
                            <li>周公解梦（娱乐性质）</li>
                            <li>姓名测算与起名（娱乐性质）</li>
                            <li>梅花易数、六爻等传统术数（娱乐性质）</li>
                            <li>AI 智能问答</li>
                        </ul>
                        <div className="p-4 rounded-lg bg-amber-50 dark:bg-amber-900/20 border border-amber-200 dark:border-amber-800">
                            <h3 className="font-bold text-amber-800 dark:text-amber-200 flex items-center gap-2 mt-0">
                                <AlertTriangle className="w-5 h-5" />
                                重要声明
                            </h3>
                            <ul className="list-disc list-inside text-amber-700 dark:text-amber-300 space-y-1 text-sm">
                                <li>本服务<strong>仅供娱乐</strong>，所有分析结果不具备科学依据</li>
                                <li>分析结果不应作为任何医疗、健康、投资、婚姻、职业或其他重要决策的依据</li>
                                <li>我们不提供任何形式的预测、预言或命运指导</li>
                                <li>本服务内容属于传统文化知识的现代演绎，以文化科普和娱乐为目的</li>
                            </ul>
                        </div>
                    </section>

                    {/* 3. 用户责任 */}
                    <section className="p-6 rounded-xl bg-card border border-border">
                        <h2 className="text-xl font-bold text-foreground flex items-center gap-2 mt-0">
                            <span className="w-8 h-8 rounded-full bg-primary/10 flex items-center justify-center text-primary text-sm font-bold">3</span>
                            <Users className="w-5 h-5" />
                            用户责任
                        </h2>
                        <h3 className="font-semibold text-foreground mt-4">3.1 基本要求</h3>
                        <ul className="list-disc list-inside text-muted-foreground space-y-1">
                            <li>您必须年满 18 周岁才能使用我们的服务</li>
                            <li>未满 18 周岁的用户必须在父母或法定监护人的同意和监督下使用本服务</li>
                            <li>您负责维护您的账户和密码的机密性</li>
                            <li>您同意不会将我们的服务用于任何非法目的</li>
                        </ul>
                        <h3 className="font-semibold text-foreground mt-4">3.2 使用规范</h3>
                        <p className="text-muted-foreground mb-2">您同意：</p>
                        <ul className="list-disc list-inside text-muted-foreground space-y-1">
                            <li>提供准确的个人信息和出生信息</li>
                            <li>不会滥用或破坏我们的服务系统</li>
                            <li>不会侵犯他人的知识产权或隐私权</li>
                            <li>不会利用本服务传播迷信内容或从事封建迷信活动</li>
                            <li>不会将服务结果用于误导他人或进行虚假宣传</li>
                            <li>遵守所有适用的法律法规</li>
                        </ul>
                    </section>

                    {/* 4. 知识产权 */}
                    <section className="p-6 rounded-xl bg-card border border-border">
                        <h2 className="text-xl font-bold text-foreground flex items-center gap-2 mt-0">
                            <span className="w-8 h-8 rounded-full bg-primary/10 flex items-center justify-center text-primary text-sm font-bold">4</span>
                            知识产权
                        </h2>
                        <h3 className="font-semibold text-foreground mt-4">4.1 服务内容</h3>
                        <ul className="list-disc list-inside text-muted-foreground space-y-1">
                            <li>通过我们的服务生成的内容仅供您个人使用</li>
                            <li>您保留您提供的原始信息的权利</li>
                            <li>网站及其原创内容、功能和设计受国际知识产权法保护</li>
                        </ul>
                        <h3 className="font-semibold text-foreground mt-4">4.2 使用限制</h3>
                        <p className="text-muted-foreground mb-2">未经我们明确许可，您不得：</p>
                        <ul className="list-disc list-inside text-muted-foreground space-y-1">
                            <li>复制或分发我们的服务内容</li>
                            <li>修改或创建衍生作品</li>
                            <li>将我们的服务用于商业目的</li>
                            <li>将生成内容用于虚假宣传或误导他人</li>
                        </ul>
                    </section>

                    {/* 5. 免责声明 */}
                    <section className="p-6 rounded-xl bg-card border border-border">
                        <h2 className="text-xl font-bold text-foreground flex items-center gap-2 mt-0">
                            <span className="w-8 h-8 rounded-full bg-primary/10 flex items-center justify-center text-primary text-sm font-bold">5</span>
                            <Shield className="w-5 h-5" />
                            免责声明
                        </h2>
                        <h3 className="font-semibold text-foreground mt-4">5.1 服务提供</h3>
                        <ul className="list-disc list-inside text-muted-foreground space-y-1">
                            <li>我们的服务按"现状"和"可用状态"提供</li>
                            <li>我们不保证服务的准确性、完整性或实用性</li>
                            <li>分析结果仅供娱乐参考，不构成任何形式的专业建议</li>
                            <li>我们不对用户基于服务结果做出的任何决策负责</li>
                        </ul>
                        <h3 className="font-semibold text-foreground mt-4">5.2 责任限制</h3>
                        <p className="text-muted-foreground mb-2">在法律允许的最大范围内，我们不对以下情况负责：</p>
                        <ul className="list-disc list-inside text-muted-foreground space-y-1">
                            <li>使用或无法使用服务造成的任何直接、间接、附带、特殊、惩罚性或后果性损害</li>
                            <li>服务中断或数据丢失</li>
                            <li>因使用我们的分析结果导致的任何决策后果</li>
                            <li>任何第三方通过我们的服务获取的信息</li>
                        </ul>
                        <h3 className="font-semibold text-foreground mt-4">5.3 明确免责事项</h3>
                        <div className="p-4 rounded-lg bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800">
                            <p className="text-red-700 dark:text-red-300 text-sm mb-2">我们明确声明：</p>
                            <ul className="list-disc list-inside text-red-600 dark:text-red-400 space-y-1 text-sm">
                                <li>本服务<strong>不提供</strong>医疗诊断、健康建议或治疗方案</li>
                                <li>本服务<strong>不提供</strong>投资建议、财务规划或经济预测</li>
                                <li>本服务<strong>不提供</strong>心理咨询或心理治疗</li>
                                <li>本服务<strong>不能</strong>预测未来事件或改变个人命运</li>
                                <li>用户应对自己的决策和行为负完全责任</li>
                            </ul>
                        </div>
                    </section>

                    {/* 6. 付费服务 */}
                    <section className="p-6 rounded-xl bg-card border border-border">
                        <h2 className="text-xl font-bold text-foreground flex items-center gap-2 mt-0">
                            <span className="w-8 h-8 rounded-full bg-primary/10 flex items-center justify-center text-primary text-sm font-bold">6</span>
                            <CreditCard className="w-5 h-5" />
                            付费服务
                        </h2>
                        <h3 className="font-semibold text-foreground mt-4">6.1 定价和支付</h3>
                        <ul className="list-disc list-inside text-muted-foreground space-y-1">
                            <li>服务价格以网站显示为准</li>
                            <li>某些高级功能可能需要付费</li>
                            <li>我们保留调整价格的权利，价格变动前会提前通知</li>
                            <li>所有付款均通过安全的第三方支付处理商处理</li>
                        </ul>
                        <h3 className="font-semibold text-foreground mt-4">6.2 退款政策</h3>
                        <ul className="list-disc list-inside text-muted-foreground space-y-1">
                            <li>数字服务一经使用不支持退款</li>
                            <li>特殊情况下的退款需求将个案处理</li>
                            <li>退款申请需要在购买后 7 天内提出</li>
                        </ul>
                    </section>

                    {/* 7. 账户管理 */}
                    <section className="p-6 rounded-xl bg-card border border-border">
                        <h2 className="text-xl font-bold text-foreground flex items-center gap-2 mt-0">
                            <span className="w-8 h-8 rounded-full bg-primary/10 flex items-center justify-center text-primary text-sm font-bold">7</span>
                            账户管理
                        </h2>
                        <h3 className="font-semibold text-foreground mt-4">7.1 账户安全</h3>
                        <p className="text-muted-foreground mb-2">您负责：</p>
                        <ul className="list-disc list-inside text-muted-foreground space-y-1">
                            <li>保护您的账户信息</li>
                            <li>及时更新个人资料</li>
                            <li>报告任何未经授权的使用</li>
                            <li>确保不与他人共享账户</li>
                        </ul>
                        <h3 className="font-semibold text-foreground mt-4">7.2 账户终止</h3>
                        <p className="text-muted-foreground mb-2">我们可能会：</p>
                        <ul className="list-disc list-inside text-muted-foreground space-y-1">
                            <li>因违反条款暂停或终止账户</li>
                            <li>删除长期不活跃的账户</li>
                            <li>保留相关数据用于法律目的</li>
                        </ul>
                    </section>

                    {/* 8. 服务变更 */}
                    <section className="p-6 rounded-xl bg-card border border-border">
                        <h2 className="text-xl font-bold text-foreground flex items-center gap-2 mt-0">
                            <span className="w-8 h-8 rounded-full bg-primary/10 flex items-center justify-center text-primary text-sm font-bold">8</span>
                            服务变更
                        </h2>
                        <p className="text-muted-foreground mb-2">我们保留以下权利：</p>
                        <ul className="list-disc list-inside text-muted-foreground space-y-1">
                            <li>修改或终止服务的任何部分</li>
                            <li>更新服务条款（更新后会通知用户）</li>
                            <li>暂停或限制服务访问</li>
                            <li>调整服务功能和内容</li>
                        </ul>
                        <p className="text-muted-foreground mt-4">
                            重大变更将通过网站通知用户。继续使用服务即表示接受更新后的条款。
                        </p>
                    </section>

                    {/* 9. 未成年人保护 */}
                    <section className="p-6 rounded-xl bg-card border border-border">
                        <h2 className="text-xl font-bold text-foreground flex items-center gap-2 mt-0">
                            <span className="w-8 h-8 rounded-full bg-primary/10 flex items-center justify-center text-primary text-sm font-bold">9</span>
                            未成年人保护
                        </h2>
                        <p className="text-muted-foreground mb-2">我们重视未成年人的保护：</p>
                        <ul className="list-disc list-inside text-muted-foreground space-y-1">
                            <li>本服务主要面向成年人</li>
                            <li>未满18周岁的用户需在父母或监护人同意和监督下使用</li>
                            <li>我们不会故意收集未成年人的个人信息</li>
                            <li>如发现未经监护人同意收集了未成年人信息，我们将立即删除</li>
                        </ul>
                    </section>

                    {/* 10. 联系方式 */}
                    <section className="p-6 rounded-xl bg-card border border-border">
                        <h2 className="text-xl font-bold text-foreground flex items-center gap-2 mt-0">
                            <span className="w-8 h-8 rounded-full bg-primary/10 flex items-center justify-center text-primary text-sm font-bold">10</span>
                            联系方式
                        </h2>
                        <p className="text-muted-foreground">
                            如果您对这些条款有任何疑问，请联系我们：
                        </p>
                        <p className="text-foreground mt-2">
                            电子邮件：<a href="mailto:181593130@qq.com" className="text-primary hover:underline">181593130@qq.com</a>
                        </p>
                    </section>

                    {/* 条款接受 */}
                    <section className="p-6 rounded-xl bg-primary/5 border border-primary/20">
                        <h2 className="text-xl font-bold text-foreground flex items-center gap-2 mt-0">
                            <Scale className="w-5 h-5 text-primary" />
                            条款接受
                        </h2>
                        <p className="text-muted-foreground">
                            使用 AI 占卜即表示您确认已阅读、理解并同意这些服务条款。
                            您确认本服务<strong>仅供娱乐</strong>，不应作为任何重要决策的依据。
                        </p>
                    </section>

                    {/* 声明更新提示 */}
                    <div className="text-center text-xs text-muted-foreground p-4 bg-muted/50 rounded-lg">
                        <p>本服务条款可能会不定期更新，请定期查阅以了解最新内容。</p>
                        <p className="mt-1">继续使用本服务即表示您接受更新后的条款。</p>
                    </div>
                </div>
            </div>
        </>
    )
}
