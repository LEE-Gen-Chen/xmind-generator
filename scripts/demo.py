#!/usr/bin/env python3
"""
Demo: regenerate the AI副业 knowledge map with the new xmindgen library.

This demonstrates the clean API — all the original content,
without the bugs in gen_xmind_beautify_v2.py (which had wrong variable
names m1c→m1_children, worker reassignment bug, etc.)
"""

import sys
import os

# Add parent to path for local development
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from xmindgen import save, Topic

OUTPUT = os.path.join(os.path.dirname(__file__), "demo_output.xmind")

# ─── Helper to create styled branches ─────────────────────────────────────────
def make_branch(title, color):
    t = Topic(title)
    t._style = color   # stored temporarily; used below
    return t

# ─── Root ─────────────────────────────────────────────────────────────────────
root = Topic("🚀 AI副业全局规划知识图谱")

# ─── Branch 1: 市场分析 (#1A6B5C) ─────────────────────────────────────────────
m1 = root.add_child("📊 市场分析")
pest = m1.add_child("🗺️ PEST宏观分析")
pest.add_child("政治：AI教育获国家政策扶持/银发经济纳入十四五")
pest.add_child("经济：居民消费分化/兴趣消费规模3852亿(+10%)")
pest.add_child("社会：60岁以上人口超3亿/数字鸿沟催生银发需求")
pest.add_child("技术：大模型实用化(GPT-4o/Claude3.5/文心4/通义2.5)")

porter = m1.add_child("⚔️ 波特五力分析")
porter.add_child("行业内竞争→剧烈分化：K12红海 vs 银发AI蓝海")
porter.add_child("潜在进入者→威胁高：字节/腾讯/阿里随时可切入")
porter.add_child("替代品→威胁中：免费内容分流付费课程")
porter.add_child("供应商议价→能力低：内容创作者高度分散")
porter.add_child("买家议价→能力强：信息透明/比价容易")

m1.add_child("🚫 红海市场：K12编程课/成人AI泛课/视频剪辑课/闲鱼无货源")
m1.add_child("🌊 蓝海市场：中老年AI工具课/职场人AI提效/大学生副业工具包")
m1.add_child("🎯 差异化策略：人群/内容/交付/渠道四维差异化")

timeline_m1 = m1.add_child("📆 180天执行时间轴")
timeline_m1.add_child("1-30天：选赛道/测MVP/跑通第一笔付费")
timeline_m1.add_child("31-60天：打磨核心产品/私域沉淀100-500用户")
timeline_m1.add_child("61-120天：规模化获客/月收入破万")
timeline_m1.add_child("121-180天：矩阵化运营/建立壁垒")

# ─── Branch 2: 客群画像 (#D4600A) ─────────────────────────────────────────────
m2 = root.add_child("👥 客群画像")
m2.add_child("🏙️ 城市家长：30-42岁/本科学历/焦虑驱动/愿付2000-8000元训练营")
m2.add_child("🎓 大学生：18-24岁/就业焦虑/愿付9.9-999元系统课")

worker = m2.add_child("💼 打工人三层")
w_low = worker.add_child("🔴 低收入层 · <5000元/月")
w_low.add_child("推荐：短视频搬运/问卷试玩/数据标注/简单线上任务")
w_low.add_child("触达：快手/抖音极速版/微信群任务发布")
w_low.add_child("要点：防骗教育优先/避免押金和刷单")

w_mid = worker.add_child("🟡 中收入层 · 5000-15000元/月")
w_mid.add_child("推荐：AI+Excel/PPT/文案代做/小红书账号/知乎好物")
w_mid.add_child("触达：微信朋友圈/小红书/即刻/脉脉")
w_mid.add_child("要点：时间管理/可落地项目/社群互相激励")

w_high = worker.add_child("🟢 高收入层 · >15000元/月")
w_high.add_child("推荐：知识付费/培训/顾问/社群/投资型副业")
w_high.add_child("触达：公众号/视频号/播客/行业会议")
w_high.add_child("要点：优质人脉/高效项目/资产增值")

m2.add_child("👴 中老年银发群体：50-70岁/数字鸿沟/子女是实际付款人")

# ─── Branch 3: 行业财报 (#C0392B) ─────────────────────────────────────────────
m3 = root.add_child("📈 行业财报")
m3.add_child("🤖 AI教育：好未来+33.7%/新东方+13.6%/科大讯飞+18.79%")
m3.add_child("🌅 银发经济：规模5.4万亿(2023)/预计2027年接近10万亿/3亿老年人")
m3.add_child("📚 职业教育：开课吧破产/潭州教育破产/技能培训从证书→就业导向")

# ─── Branch 4: 产品矩阵 (#7B2D8B) ─────────────────────────────────────────────
m4 = root.add_child("📦 产品矩阵")
m4.add_child("💰 定价：引流层0-29元/基础层99-299元/进阶层499-999元/高阶级1999-4999元")
m4.add_child("📡 渠道：私域(微信)/内容(抖音小红书)/平台(知识星球)/分销(合伙人)")
m4.add_child("🎯 获客SOP：钩子设计+私信转化+朋友圈发售+数据指标")
m4.add_child("🔄 转化SOP：信任建立+痛点放大+下单障碍消除+追单策略")
m4.add_child("📦 交付SOP：录播课/训练营/私教/超预期交付")
m4.add_child("🔁 复购SOP：定期关怀+新品预告+升级转化+口碑裂变")

# ─── Branch 5: GitHub资源 (#0E7C7B) ────────────────────────────────────────────
m5 = root.add_child("⭐ GitHub资源")
m5.add_child("🔧 easychen/cookiecutter-applet：小程序+AI工具项目模板")
m5.add_child("💰 AI-Money-Hunter：AI副业项目聚合/工具+教程+案例")
m5.add_child("🌐 indiehackers-videos：独立开发者盈利访谈/商业案例库")
m5.add_child("🔗 LangChain-Chinese：LLM应用开发/企业培训/SAAS产品")
m5.add_child("🛠️ AnythingLLM：本地私有化AI知识库/企业部署服务")

# ─── Branch 6: 发展时间轴 (#B8860B) ────────────────────────────────────────────
m6 = root.add_child("📅 发展时间轴")
m6.add_child("2022Q1：ChatGPT发布/AI科普需求爆发/知识付费第一波红利")
m6.add_child("2022Q3：Midjourney火爆/AI绘画课热卖/第一批AI博主暴富")
m6.add_child("2023Q1：GPT-4发布/大模型竞争加剧/价格战开始")
m6.add_child("2024Q3：AI应用层创业潮/垂直行业AI落地/细分赛道机会显现")
m6.add_child("🎯 入场时机：AI视频/数据分析→快速增长期；AI Agent→早期布局期")

# ─── Branch 7: 产业全景 (#1A5276) ────────────────────────────────────────────
m7 = root.add_child("🔗 产业全景")
m7.add_child("⬆️ 上游：大模型(OpenAI/Anthropic/百度/字节)/算力/数据/开源生态")
m7.add_child("➡️ 中游：工具层(Notion/Canva/Office AI)/行业层/平台层(Agent/知识库)")
m7.add_child("⬇️ 下游：内容创作者/独立开发者/企业服务")
m7.add_child("💎 价值链：最高=应用层创新/私域资产/品牌；低=信息差/搬运型内容")

# ─── Cross-reference Relationships ─────────────────────────────────────────────
root.add_child("").add_relationship(m3.id, "市场→财报")
root.add_child("").add_relationship(m5.id, "工具→市场")
root.add_child("").add_relationship(m6.id, "时机→战略")
root.add_child("").add_relationship(m7.id, "产业→产品")

# ─── Save with branch colors ───────────────────────────────────────────────────
STYLES = {
    m1.id: ("#1A6B5C", "#FFFFFF"),
    m2.id: ("#D4600A", "#FFFFFF"),
    m3.id: ("#C0392B", "#FFFFFF"),
    m4.id: ("#7B2D8B", "#FFFFFF"),
    m5.id: ("#0E7C7B", "#FFFFFF"),
    m6.id: ("#B8860B", "#FFFFFF"),
    m7.id: ("#1A5276", "#FFFFFF"),
    w_low.id:  ("#E74C3C", "#FFFFFF"),
    w_mid.id:  ("#F1C40F", "#1A1A1A"),
    w_high.id: ("#27AE60", "#FFFFFF"),
}

os.makedirs(os.path.dirname(OUTPUT) or ".", exist_ok=True)
root.save(OUTPUT, styles=STYLES)

size = os.path.getsize(OUTPUT)
print(f"✅ Saved: {OUTPUT}")
print(f"   File size: {size:,} bytes")
print(f"   Root: {root.title}")
print(f"   Branches: {len(root._children)}")
print(f"   Relationships: {sum(len(t._relationships) for t in root._children)}")
