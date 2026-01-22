/**
 * 隐私政策页面
 * 根据模板定制，适配 AI 占卜网站
 */

import { Link } from 'react-router-dom'
import { ArrowLeft, Lock, Shield, Database, Cookie, UserCheck, Bell, Mail } from 'lucide-react'
import SEOHead from '@/components/SEOHead'

export default function PrivacyPage() {
    return (
        <>
            <SEOHead
                title="隐私政策"
                description="AI占卜平台隐私政策，了解我们如何收集、使用和保护您的个人信息"
                keywords="隐私政策,隐私保护,个人信息"
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
                            <Lock className="w-8 h-8 text-primary" />
                        </div>
                        <div>
                            <h1 className="text-3xl font-bold text-foreground">隐私政策</h1>
                            <p className="text-muted-foreground">最后更新：2024年12月</p>
                        </div>
                    </div>
                </div>

                {/* 重要声明横幅 */}
                <div className="p-4 rounded-xl bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800">
                    <p className="text-blue-700 dark:text-blue-300 text-sm">
                        <Shield className="inline-block w-4 h-4 mr-2" />
                        <strong>重要声明：</strong>AI 占卜是一款娱乐性质的工具，所有分析结果仅供娱乐参考，不具备科学依据，不应作为任何重要决策的依据。
                    </p>
                </div>

                {/* 政策内容 */}
                <div className="prose prose-sm dark:prose-invert max-w-none space-y-8">
                    {/* 1. 简介 */}
                    <section className="p-6 rounded-xl bg-card border border-border">
                        <h2 className="text-xl font-bold text-foreground flex items-center gap-2 mt-0">
                            <span className="w-8 h-8 rounded-full bg-primary/10 flex items-center justify-center text-primary text-sm font-bold">1</span>
                            简介
                        </h2>
                        <p className="text-muted-foreground">
                            AI 占卜致力于保护您的隐私。本隐私政策说明了我们在您访问我们的网站或使用我们的服务时如何收集、使用、披露和保护您的信息。
                        </p>
                    </section>

                    {/* 2. 信息收集与最小化原则 */}
                    <section className="p-6 rounded-xl bg-card border border-border">
                        <h2 className="text-xl font-bold text-foreground flex items-center gap-2 mt-0">
                            <span className="w-8 h-8 rounded-full bg-primary/10 flex items-center justify-center text-primary text-sm font-bold">2</span>
                            <Database className="w-5 h-5" />
                            信息收集与最小化原则
                        </h2>
                        <p className="text-muted-foreground mb-4">
                            我们严格遵循<strong>数据最小化原则</strong>，仅收集提供服务所必需的信息：
                        </p>
                        <div className="grid gap-4 md:grid-cols-2">
                            <div className="p-4 rounded-lg bg-muted/50">
                                <h4 className="font-semibold text-foreground mb-2">基本信息</h4>
                                <ul className="list-disc list-inside text-muted-foreground space-y-1 text-sm">
                                    <li>姓名、性别等基本信息</li>
                                    <li>出生信息（出生年月日时）</li>
                                    <li>电子邮件地址（可选）</li>
                                </ul>
                            </div>
                            <div className="p-4 rounded-lg bg-muted/50">
                                <h4 className="font-semibold text-foreground mb-2">技术信息</h4>
                                <ul className="list-disc list-inside text-muted-foreground space-y-1 text-sm">
                                    <li>IP 地址和设备信息</li>
                                    <li>浏览器类型和版本</li>
                                    <li>服务使用数据</li>
                                </ul>
                            </div>
                        </div>
                        <div className="mt-4 p-4 rounded-lg bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800">
                            <h4 className="font-semibold text-green-800 dark:text-green-200 mb-2 flex items-center gap-2">
                                <Lock className="w-4 h-4" />
                                密码安全
                            </h4>
                            <ul className="list-disc list-inside text-green-700 dark:text-green-300 space-y-1 text-sm">
                                <li>密码经过加密哈希处理存储</li>
                                <li>传输过程使用 HTTPS 加密</li>
                                <li>我们从不以明文形式存储密码</li>
                                <li>工作人员无法查看您的原始密码</li>
                            </ul>
                        </div>
                    </section>

                    {/* 3. 信息使用 */}
                    <section className="p-6 rounded-xl bg-card border border-border">
                        <h2 className="text-xl font-bold text-foreground flex items-center gap-2 mt-0">
                            <span className="w-8 h-8 rounded-full bg-primary/10 flex items-center justify-center text-primary text-sm font-bold">3</span>
                            信息使用
                        </h2>
                        <p className="text-muted-foreground mb-2">我们使用收集的信息用于：</p>
                        <ul className="list-disc list-inside text-muted-foreground space-y-1">
                            <li>提供基于传统文化的娱乐性分析服务</li>
                            <li>处理用户登录和身份验证</li>
                            <li>分析用户来源和网站流量</li>
                            <li>发送服务通知和更新</li>
                            <li>改进我们的服务质量</li>
                        </ul>
                    </section>

                    {/* 4. 数据存储和安全 */}
                    <section className="p-6 rounded-xl bg-card border border-border">
                        <h2 className="text-xl font-bold text-foreground flex items-center gap-2 mt-0">
                            <span className="w-8 h-8 rounded-full bg-primary/10 flex items-center justify-center text-primary text-sm font-bold">4</span>
                            <Shield className="w-5 h-5" />
                            数据存储和安全
                        </h2>
                        <p className="text-muted-foreground mb-4">
                            您的数据存储在符合行业标准的安全平台上。我们实施全面的技术和组织措施：
                        </p>
                        <div className="grid gap-3 md:grid-cols-2">
                            {[
                                'SSL/TLS 加密传输',
                                '密码单向哈希存储',
                                '定期安全审计',
                                '严格访问控制',
                                '数据备份方案',
                                '数据匿名化处理'
                            ].map((item, index) => (
                                <div key={index} className="flex items-center gap-2 p-3 rounded-lg bg-muted/50">
                                    <div className="w-2 h-2 rounded-full bg-green-500" />
                                    <span className="text-sm text-muted-foreground">{item}</span>
                                </div>
                            ))}
                        </div>
                    </section>

                    {/* 5. 用户数据保护与授权同意 */}
                    <section className="p-6 rounded-xl bg-card border border-border">
                        <h2 className="text-xl font-bold text-foreground flex items-center gap-2 mt-0">
                            <span className="w-8 h-8 rounded-full bg-primary/10 flex items-center justify-center text-primary text-sm font-bold">5</span>
                            <UserCheck className="w-5 h-5" />
                            用户数据保护与授权同意
                        </h2>
                        <p className="text-muted-foreground mb-2">我们向用户保证：</p>
                        <ul className="list-disc list-inside text-muted-foreground space-y-1 mb-4">
                            <li>您的个人信息<strong>不会被出售或披露</strong>给第三方</li>
                            <li>我们仅在获得您明确同意后使用您的数据</li>
                            <li>您可以随时撤回同意并要求删除您的数据</li>
                            <li>我们使用匿名化数据来改进服务</li>
                            <li>所有数据传输都经过加密处理</li>
                        </ul>
                        <div className="p-4 rounded-lg bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800">
                            <h4 className="font-semibold text-blue-800 dark:text-blue-200 mb-2">授权同意</h4>
                            <ul className="list-disc list-inside text-blue-700 dark:text-blue-300 space-y-1 text-sm">
                                <li>首次使用时，我们会通过明确的方式获取您的同意</li>
                                <li>您可以随时在设置中查看和修改您的隐私偏好</li>
                                <li>我们不会使用预先勾选的同意选项或隐藏的同意条款</li>
                            </ul>
                        </div>
                    </section>

                    {/* 6. 您的权利 */}
                    <section className="p-6 rounded-xl bg-card border border-border">
                        <h2 className="text-xl font-bold text-foreground flex items-center gap-2 mt-0">
                            <span className="w-8 h-8 rounded-full bg-primary/10 flex items-center justify-center text-primary text-sm font-bold">6</span>
                            您的权利
                        </h2>
                        <p className="text-muted-foreground mb-2">您有权：</p>
                        <div className="grid gap-2 md:grid-cols-2">
                            {[
                                '访问我们持有的您的个人信息',
                                '要求更正您的个人信息',
                                '要求删除您的个人信息',
                                '反对处理您的个人信息',
                                '要求限制处理您的个人信息',
                                '要求传输您的个人信息',
                                '要求删除您的分析记录'
                            ].map((right, index) => (
                                <div key={index} className="flex items-start gap-2 p-2">
                                    <div className="w-5 h-5 rounded-full bg-primary/10 flex items-center justify-center flex-shrink-0 mt-0.5">
                                        <span className="text-xs text-primary">✓</span>
                                    </div>
                                    <span className="text-sm text-muted-foreground">{right}</span>
                                </div>
                            ))}
                        </div>
                    </section>

                    {/* 7. 数据保留 */}
                    <section className="p-6 rounded-xl bg-card border border-border">
                        <h2 className="text-xl font-bold text-foreground flex items-center gap-2 mt-0">
                            <span className="w-8 h-8 rounded-full bg-primary/10 flex items-center justify-center text-primary text-sm font-bold">7</span>
                            数据保留
                        </h2>
                        <p className="text-muted-foreground">
                            我们仅在必要时间内保留您的个人信息和分析数据，以提供服务并履行本隐私政策中描述的目的。
                            我们还将在必要范围内保留和使用这些信息，以遵守法律义务、解决争议并执行我们的协议。
                        </p>
                    </section>

                    {/* 8. Cookie 使用 */}
                    <section className="p-6 rounded-xl bg-card border border-border">
                        <h2 className="text-xl font-bold text-foreground flex items-center gap-2 mt-0">
                            <span className="w-8 h-8 rounded-full bg-primary/10 flex items-center justify-center text-primary text-sm font-bold">8</span>
                            <Cookie className="w-5 h-5" />
                            Cookie 使用
                        </h2>
                        <p className="text-muted-foreground mb-2">我们使用 Cookie 和类似技术来：</p>
                        <ul className="list-disc list-inside text-muted-foreground space-y-1 mb-4">
                            <li>保持您的登录状态</li>
                            <li>记住您的偏好设置</li>
                            <li>分析网站使用情况</li>
                            <li>提供个性化体验</li>
                        </ul>
                        <p className="text-sm text-muted-foreground/80">
                            您可以通过浏览器设置控制 Cookie，但这可能会影响某些服务功能。
                        </p>
                    </section>

                    {/* 9. 未成年人保护 */}
                    <section className="p-6 rounded-xl bg-card border border-border">
                        <h2 className="text-xl font-bold text-foreground flex items-center gap-2 mt-0">
                            <span className="w-8 h-8 rounded-full bg-primary/10 flex items-center justify-center text-primary text-sm font-bold">9</span>
                            未成年人保护
                        </h2>
                        <p className="text-muted-foreground">
                            我们的服务不面向18岁以下的未成年人。我们不会故意收集未成年人的个人信息。
                            如果您是父母或监护人，发现您的孩子未经您的同意向我们提供了个人信息，请立即联系我们，我们将采取措施删除相关信息。
                        </p>
                    </section>

                    {/* 10. 政策更新 */}
                    <section className="p-6 rounded-xl bg-card border border-border">
                        <h2 className="text-xl font-bold text-foreground flex items-center gap-2 mt-0">
                            <span className="w-8 h-8 rounded-full bg-primary/10 flex items-center justify-center text-primary text-sm font-bold">10</span>
                            <Bell className="w-5 h-5" />
                            政策更新
                        </h2>
                        <p className="text-muted-foreground mb-2">
                            我们定期审查并更新本隐私政策。重大变更时，我们会：
                        </p>
                        <ul className="list-disc list-inside text-muted-foreground space-y-1">
                            <li>在网站显著位置发布通知</li>
                            <li>通过您提供的电子邮件发送通知</li>
                            <li>在应用内推送通知</li>
                        </ul>
                        <p className="text-muted-foreground mt-4">
                            继续使用我们的服务即表示您接受更新后的政策。
                        </p>
                    </section>

                    {/* 11. 联系我们 */}
                    <section className="p-6 rounded-xl bg-card border border-border">
                        <h2 className="text-xl font-bold text-foreground flex items-center gap-2 mt-0">
                            <span className="w-8 h-8 rounded-full bg-primary/10 flex items-center justify-center text-primary text-sm font-bold">11</span>
                            <Mail className="w-5 h-5" />
                            联系我们
                        </h2>
                        <p className="text-muted-foreground">
                            如果您对本隐私政策有任何疑问、意见或请求，请联系我们：
                        </p>
                        <p className="text-foreground mt-2">
                            电子邮件：<a href="mailto:181593130@qq.com" className="text-primary hover:underline">181593130@qq.com</a>
                        </p>
                    </section>

                    {/* 声明更新提示 */}
                    <div className="text-center text-xs text-muted-foreground p-4 bg-muted/50 rounded-lg">
                        <p>本隐私政策可能会不定期更新，请定期查阅以了解最新内容。</p>
                        <p className="mt-1">继续使用本服务即表示您接受更新后的政策。</p>
                    </div>
                </div>
            </div>
        </>
    )
}
