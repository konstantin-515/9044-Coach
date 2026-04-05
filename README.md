# 9044 Coach

`9044-coach` 是一个面向 COMP2041 / COMP9044 复习场景设计的本地 skill。

它的目标不是单纯“聊天里给一道题”，而是尽量像一个真正能陪你刷题、记错题、反复回顾的备考教练：

- 参考本地 `lab` / `test` 资料库出题
- 生成符合课程风格的 `dash` / `grep -E` / `sed` / `awk` / text processing 练习
- 默认落一个可直接练习的工作目录
- 同时生成题面、数据、期望输出、测试脚本、学习笔记模板
- 在你有个人笔记时，优先参考你的复习重点

---

## 1. 这个 skill 解决什么问题

在 9044 复习里，最常见的痛点不是“没有资料”，而是：

- 原题看过了，不想只反复做原题
- 想练 `dash`、`grep -E`、regex、文本处理，但不想每次手动搭测试环境
- 想把练习、测试、错题笔记放在一个目录里
- 想让新题尽量贴近自己的薄弱点和笔记重点
- 想在复习前先看一眼自己归档练习里最常犯的错

这个 skill 就是为了解决这些问题：

1. 用本地题库总结出题型模式
2. 生成一套新的练习，而不是照搬原题
3. 自动创建一个可以直接练习的目录
4. 留出 `notebook.md` 方便你积累命令、易错点、反思
5. 在你想复习时，总结归档目录里的错因和高频提醒

---

## 2. 适合做什么

这个 skill 适合这些场景：

- “给我出一道 9044 风格的 shell 题”
- “给我一个可以直接练习的 test01 文件夹”
- “按期末风格出 2 到 3 道练习”
- “我想练 `grep -E` / regex / pipeline / directory compare”
- “帮我做一个专项 drill”
- “帮我批改 `solution.sh`”
- “参考我的笔记再出题”

不适合的事情：

- 直接复读学校原题
- 假装生成的是官方考试题
- 出和课程风格无关的竞赛算法题
- 把练习目录做成复杂工程而不是轻量刷题目录

---

## 3. 默认生成什么

如果用户没有特别说明，这个 skill 默认会：

- 生成 `1` 个练习
- 难度偏 `exam-style`
- 题型优先为 `dash shell + grep -E + text processing`
- 默认不直接给完整答案
- 默认生成一个可直接练习的目录，而不是只在对话里贴题目

默认目录建议生成在：

```text
exercises/testNN/
```

例如：

```text
exercises/test01/
exercises/test02/
```

每次只生成一个目录，不再同时生成“日期版目录”和“slug 版目录”。

完成后的练习默认建议从 `exercises/` 归档到：

```text
archives/<topic>/testNN/
```

例如：

```text
archives/re/test01/
archives/shell/test02/
archives/python/test03/
```

---

## 4. 练习目录结构

默认结构：

```text
testNN/
  README.md
  notebook.md
  solution.sh 或 solution.py
  data/
  expected/
  tests/
```

各文件职责：

- `README.md`
  中文题面、输入输出规则、路径说明、运行方式、考点、常见错误
- `notebook.md`
  你的个人学习笔记模板，用来记录命令、易错点、复盘
- `solution.sh` / `solution.py`
  你真正要写答案的文件
- `data/`
  样例输入、边界输入、表格类数据
- `expected/`
  对应的期望输出
- `tests/`
  测试脚本，以及失败时保留的输出产物

---

## 5. 生成题目的风格

这个 skill 当前默认偏向这些内容：

- `dash` / POSIX `sh`
- `grep -E`
- `sed`
- `awk`
- `sort`
- `uniq`
- `cut`
- `tr`
- `find`
- 结构化文本解析
- 目录与文件比较
- 小型 Python 文本处理

它会尽量避免：

- Bash-only 特性
- 与课程无关的高复杂度算法题
- 需要庞大依赖或复杂 setup 的工程题

---

## 6. 知识来源与优先级

这个 skill 主要使用这些来源：

- `references/knowledge-base/lab_output/`
- `references/knowledge-base/test_output/`
- `references/knowledge-base/sample_data/`
- `references/user-notes/md/`
- `references/user-notes/pdf/`

为了减少 token 消耗、提高命中速度，它优先参考：

- `references/topic-index.md`
- `references/question-patterns.md`
- `references/output-templates.md`
- `references/data-shapes.md`
- `references/workspace-rules.md`
- `references/question-quality-checklist.md`

当同时有题库和你自己的笔记时，推荐优先级是：

1. 你当前这次请求里明确说的重点
2. 你的 Markdown 笔记
3. `references/` 下的压缩索引
4. 你的 PDF 笔记
5. 详细知识库副本

说明：

- Markdown 笔记优先于 PDF
- 如果 PDF 不方便直接读内容，可以只把 PDF 文件名/主题当线索，不能凭空编内容

---

## 7. 我的笔记怎么放

如果你想让这个 skill 参考你自己的总结，可以把资料放到：

- `references/user-notes/md/`
- `references/user-notes/pdf/`

建议：

- 自己写的总结尽量放 `md/`
- 课程 PDF 或整理过的 PDF 笔记放 `pdf/`

例如：

```text
references/user-notes/md/grep-notes.md
references/user-notes/md/regex-mistakes.md
references/user-notes/pdf/week05-summary.pdf
references/user-notes/pdf/final-review.pdf
```

之后你可以直接说：

- “参考我的笔记再给我出题”
- “优先按我 pdf 笔记里的重点出题”
- “结合我的错题笔记出一个 regex drill”

---

## 8. Windows + WSL + dash 的默认工作流

因为你是在 Windows 上学习，但练习的是 `dash`，这个 skill 默认会把 README 写成适合 WSL 的形式。

`README.md` 里应该明确给出：

- Windows 绝对路径
- WSL 绝对路径
- 可直接复制的 `cd` 命令

例如：

```text
Windows 路径：F:\Codex\9044-skill\exercises\test01
WSL 路径：/mnt/f/Codex/9044-skill/exercises/test01
进入目录：
cd /mnt/f/Codex/9044-skill/exercises/test01
```

如果是 shell 题，`solution.sh` 占位文件也会默认写上类似注释：

```sh
#!/bin/dash
# 在 Windows 上可以这样运行：
# 1. 在 PowerShell 中启动 WSL
# 2. cd 到这个练习目录
# 3. 执行：dash solution.sh < data/sample01_input.txt
# 4. 测试：dash tests/run_tests.sh
#
# 在下面写你的答案。
```

---

## 9. 测试脚本应该长什么样

测试脚本不应该只输出“过/不过”，而应该尽量告诉你为什么错。

理想的输出顺序：

1. `PASS` / `FAIL`
2. 一句人话原因
3. 必要时给行数/换行等摘要
4. 最后才给短 diff

例如它应该能指出：

- 行数不一致
- 排序错误
- 去重逻辑错误
- 内容其实对了，但末尾换行缺失
- 程序退出码非 0

为了方便调试，失败用例的实际输出建议保存在稳定路径，例如：

```text
tests/.artifacts/sample.actual.txt
tests/.artifacts/edge.actual.txt
```

这样你就可以反复比对自己的输出和期望输出。

---

## 10. 归档模式

这个 skill 现在也支持“归档已完成练习”。

目标是把：

- `exercises/`

保持成“正在做的区域”，而把：

- `archives/`

当成“已经做完、按主题归档的区域”。

### 归档后结构

```text
exercises/
  test04/
  test05/

archives/
  re/
    test01/
  shell/
    test02/
  python/
    test03/
  misc/
    test06/
```

### 支持的归档输入

- 单个：`test01`
- 范围：`test01-03`
- 组合：`test01,test03-05`

### 自动主题判断

如果你不指定目标文件夹，skill 会自动判断归档到哪里。

它会优先参考：

- `README.md`
- `notebook.md`
- 题目的语言类型，例如 `solution.sh` 或 `solution.py`
- 题目里出现的关键词，比如 `regex`、`grep`、`sed`、`awk`、`pipeline`、`shell`、`git`、`python`

默认会尽量归到这些短主题目录：

- `re`
- `grep`
- `sed`
- `awk`
- `pipeline`
- `shell`
- `files`
- `git`
- `python`
- `misc`

如果自动判断不够有把握，就归到 `misc/`，而不是乱猜。

### 归档示例

你可以直接说：

- “请帮我归档 test01”
- “请帮我归档 test01-03”
- “请帮我把 test01-03 归档”

如果你想手动指定，也可以说：

- “请帮我把 test01-03 归档到 re 文件夹下”

### 归档规则

- 归档对你来说是“移动”，但内部实现更稳的方式应当是：先复制、再校验、最后删除源目录
- 原来的 `exercises/testNN` 会被移走
- 目标目录不存在时会自动创建
- 如果 `archives/<topic>/testNN` 已经存在，不会静默覆盖
- 如果请求里有不存在的 test，会明确告诉你哪些没找到
- 归档时应忽略低价值临时文件，例如 `tests/.artifacts/` 和 `__pycache__/`
- 如果复制成功但删除失败，应该明确告诉你“归档副本已完整，但清理源目录失败”，而不是直接抛 traceback
- 如果遇到权限问题，后续清理应优先走更高权限，并尽量避免带 profile 的 shell 启动噪音

---

## 11. 错因总结模式

这个 skill 现在也支持“按归档笔记总结错因”。

它适合这些请求：

- “我想复习一下之前的错因”
- “总结一下归档里的 notebook”
- “帮我看看我最常错什么”
- “按归档笔记给我做一份复习总结”

它会优先扫描：

- `archives/<topic>/<testNN>/notebook.md`
- `archives/<topic>/<testNN>/metadata.json`

然后把这些栏目汇总出来：

- `我卡住的点`
- `我做错的点`
- `需要记住的命令/选项`
- `下次再做这题时要提醒自己的话`

默认输出文件：

```text
archives/_summaries/mistake-summary.md
archives/_summaries/mistake-summary.json
```

如果你只想看一个主题，也可以按主题输出：

```text
archives/_summaries/mistake-summary-re.md
archives/_summaries/mistake-summary-re.json
```

总结内容会尽量包括：

- 总共扫描了多少份归档笔记
- 哪些主题最常出现
- 高频卡点和高频错误
- 最常需要回顾的命令/选项
- 按主题分组的复习提醒
- 一小段下一步复习建议

如果当前还没有归档笔记，skill 也会照样生成一份“空状态总结”，提醒你先归档哪些练习。

---

## 12. notebook.md 是干什么的

`notebook.md` 不是题解，而是你自己的复习记录。

建议记录这些内容：

- 日期
- 题目
- 我一开始怎么想
- 我卡住在哪里
- 我犯了什么错
- 这题涉及哪些命令/选项
- 哪些例子值得以后再看
- 下次再做这题要提醒自己的话

像下面这些就很适合记进去：

- `grep -o` 是提取匹配部分，不是输出整行
- `grep -E` 用扩展正则，少写很多反斜杠
- `sort -u` 和 `sort | uniq` 的区别
- `awk` 默认按空白分列时会不会吃掉多余空格

---

## 13. 支持的模式

这个 skill 当前支持这些模式：

- `question`：只出题
- `drill`：短小专项练习
- `mock-exam`：小型模拟卷
- `workspace`：生成完整练习目录
- `archive`：归档已完成练习
- `mistake-summary`：汇总归档笔记里的错因
- `review`：复习某类题型
- `hint`：给提示
- `solution`：给思路或完整解
- `checker`：批改你的答案

通常最推荐的是 `workspace`，因为它最符合你“直接开练”的需求。

---

## 14. subagent 分工

当用户明确要求使用 subagent / delegation 时，推荐分工：

- 主 agent：负责定题、写 `README.md`、决定目录结构、整合最终目录
- subagent 1：负责 `data/` 和 `expected/`
- subagent 2：负责 `tests/`

如果用户没有明确要求 subagent，则保持同样的职责划分，但由单 agent 完成。

注意平台限制：

- 只有用户明确提出 subagent / delegation / parallel agent work 时，才真的起 subagent
- 不能默认偷偷开 subagent

---

## 15. 设计原则

这个 skill 的核心原则：

- 尽量贴近本地课程风格
- 不直接复制原题
- 样例要能手算验证
- 边界测试要能真实暴露错误
- 目录生成后要开箱即用
- 优先练习价值，而不是花哨设定
- 当你有个人笔记时，题目应尽量围绕你的复习重点

---

## 16. 已知说明

- `references/knowledge-base/sample_data/test05/` 下应优先使用 `compare_directory1/` 和 `compare_directory2/`
- 同级旧的 `directory1` / `directory2` 顶层残留文件应忽略
- 旧目录 `../shell-exam-coach/` 已废弃，后续应只维护当前这个 skill

---

## 17. 推荐使用方式

比较推荐的调用方式：

- “用 9044-coach 给我生成一个 shell pipeline 练习文件夹”
- “用 9044-coach 给我一个 `grep -E` 专项练习目录”
- “用 9044-coach 给我出 2 道期末风格题，不要答案”
- “参考我的笔记再给我生成 test02”
- “用 9044-coach 帮我检查这个 solution.sh 还有哪些边界没覆盖”
- “我想复习一下之前的错因”
- “请帮我总结归档 notebook 里的高频错误”
- “主 agent 出题，1 个 subagent 出数据，1 个 subagent 出测试脚本”

---

## 18. 维护这个 skill 时先看哪里

如果以后你还要继续改这个 skill，建议优先看：

- `SKILL.md`：主规则
- `references/workspace-rules.md`：练习目录生成规则
- `references/archive-rules.md`：归档规则
- `references/mistake-summary-rules.md`：错因总结规则
- `references/output-templates.md`：README / notebook / 测试脚本模板
- `references/question-quality-checklist.md`：质量门禁
- `references/source-map.md`：知识来源说明

如果只是加你自己的知识点或总结，优先改：

- `references/user-notes/md/`
- `references/user-notes/pdf/`
