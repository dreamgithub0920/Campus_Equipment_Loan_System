# MSE800 presentation script: shorter version for a 15-minute team slot

更新日期：2026 年 10 月 25 日。对应 `04_Presentation_15min.pptx` 的 12 页。

## 使用方法

- 顺序和分配不变：Xuerui Huang 第 1–4 页，Bin Wang 第 5–8 页，Yonghui Dai 第 9–12 页，每人一个 5 分钟时段。
- 本版面向非英语母语演讲者：句子更短，每行是一句；行尾可自然停顿，空行可稍作停顿。
- 中文提示和本说明不朗读。不要把 PPT 的表格、所有数字和备注来源全部读一遍。
- 5 分钟包含讲述、停顿、指向画面、换页和交接。Bin 的 2 分 15 秒演示也包含在内，可边操作边讲。
- 下表是时间分配，不是实测语速。建议按约每分钟 80–90 个英文词彩排；Bin 的演示操作需要单独计时。
- 如果提前结束，不必拖长单词填满 5 分钟；自然交接。是否必须严格满 15 分钟，以及问答是否计入，需要以老师要求为准。
- 会议示例、助手技术检查、真实个人经历和待开展的咨询保持区分。

## 缩短前后

| 演讲人 | 原版英文词数 | 本版英文词数 | 备注 |
| --- | ---: | ---: | --- |
| Xuerui Huang | 519 | 380 | 慢速讲述并保留停顿 |
| Bin Wang | 402 | 290 | 含边操作边讲的 GUI 演示 |
| Yonghui Dai | 503 | 376 | 慢速讲述并保留停顿 |

词数用于控制篇幅，并不保证实际演讲时长。PPT 备注和下文正文完全对应。

## 逐页时间分配

| 页 | 主题 | 演讲人 | 本页时段 | 全场时间 |
| --- | --- | --- | --- | --- |
| 1 | Campus Equipment Loan System | Xuerui Huang | 30 秒 | 00:00–00:30 |
| 2 | Equipment desk workflow | Xuerui Huang | 60 秒 | 00:30–01:30 |
| 3 | Requirements and priorities | Xuerui Huang | 90 秒 | 01:30–03:00 |
| 4 | Team, sprints and estimate | Xuerui Huang | 120 秒 | 03:00–05:00 |
| 5 | Object-oriented structure | Bin Wang | 90 秒 | 05:00–06:30 |
| 6 | Phone storage and older records | Bin Wang | 45 秒 | 06:30–07:15 |
| 7 | Live GUI demonstration | Bin Wang | 135 秒 | 07:15–09:30 |
| 8 | Design choices and limits | Bin Wang | 30 秒 | 09:30–10:00 |
| 9 | Technical verification | Yonghui Dai | 90 秒 | 10:00–11:30 |
| 10 | Cultural considerations and Te Tiriti | Yonghui Dai | 90 秒 | 11:30–13:00 |
| 11 | Reflection and next review | Yonghui Dai | 90 秒 | 13:00–14:30 |
| 12 | Current release and next steps | Yonghui Dai | 30 秒 | 14:30–15:00 |

## Slide 1: Campus Equipment Loan System

**Speaker:** Xuerui Huang  
**Time allocation:** 00:00–00:30 (30 seconds)

Good morning. We are Xuerui Huang, Bin Wang and Yonghui Dai.
Our project is the Campus Equipment Loan System.
I will introduce the requirements and plan.
Bin will show the design and demo.
Yonghui will discuss testing and reflection.

**操作提示（不朗读）：** 慢速介绍姓名和主题，30 秒左右换页。不要额外朗读封面的副标题。

## Slide 2: Equipment desk workflow

**Speaker:** Xuerui Huang  
**Time allocation:** 00:30–01:30 (60 seconds)

The system helps a campus desk manage five devices: a laptop, camera, projector, tablet and microphone.

The operator checks availability, records a loan, and later registers a return.
Each new loan needs a name or alias and a phone number.
Returned loans stay in the history.

The application runs on one computer and saves records locally.
It does not need a server.
Each device has a fixed ID to avoid confusion.
Different computers keep their own separate loan records.
The demonstration uses fictional borrower details.

**操作提示（不朗读）：** 慢速讲述；句号处自然停顿。指向设备清单和借还流程。此页结束时累计 1 分 30 秒。

## Slide 3: Requirements and priorities

**Speaker:** Xuerui Huang  
**Time allocation:** 01:30–03:00 (90 seconds)

The six user stories cover availability, borrowing, returns, history, saved records and Unicode names.

The core workflow and saved records are Must requirements.
History is a Should requirement, and it is included.
The operator can still read past loans after a return.
Saved records must remain when the application restarts.
Each story has a clear test.
For example, the system must reject a second loan for the same device.

New loans require a phone number with seven to fifteen digits.
Spaces and common phone symbols are allowed.
This checks the format only.
It cannot check who owns the number.
Online booking, accounts and payments are outside the current scope.

**操作提示（不朗读）：** 只解释讲稿中的重点，不逐行读表格，也不补充电话号码的全部格式规则。累计约 3:00。

## Slide 4: Team, sprints and estimate

**Speaker:** Xuerui Huang  
**Time allocation:** 03:00–05:00 (120 seconds)

The proposed roles are shown here.
I cover requirements, planning and the interface.
Bin covers objects, rules and integration.
Yonghui covers storage, testing and evidence.
Each member should also review another part.

The report uses a two-sprint planning example.
Sprint one covers inventory, borrowing and storage.
Sprint two covers returns, history and testing.
The estimates are twenty-three and thirty-one hours: fifty-four hours in total.
These are examples, not records of completed student meetings.

Later changes add the GUI, Windows support, two devices and phone contacts.
The plan adds twelve hours for review and adaptation.
This gives sixty-six hours overall.
The current estimate also allows each member to review another component.

At thirty dollars per hour, labour is one thousand nine hundred and eighty dollars.
With resources and contingency, the total estimate is two thousand two hundred and eleven New Zealand dollars.

Bin will now explain the design.

**操作提示（不朗读）：** 成本只读讲稿中的 labour 和 total，不逐项念表。估算保持为估算，会议示例保持为示例。累计约 5:00 交接给 Bin。

## Slide 5: Object-oriented structure

**Speaker:** Bin Wang  
**Time allocation:** 05:00–06:30 (90 seconds)

Thank you. The design has separate parts for the interface, rules and storage.

The GUI and terminal interface share one LoanService.
This keeps the borrowing rules consistent.
The interface displays the result and updates the tables after a successful action.
The service receives a repository object.
This is composition.
The repository saves and loads records in SQLite.
Equipment and Loan objects carry the data.

The service checks names, phone numbers and availability.
The database also prevents two active loans for one device.
Tablet and Microphone use the same Equipment model because their borrowing behaviour is the same.
The interface uses equipment IDs for borrowing and loan IDs for returns.

**操作提示（不朗读）：** 慢速讲述；句号处自然停顿。讲清两个界面共用服务、组合关系、服务校验和数据库约束。累计 6:30。

## Slide 6: Phone storage and older records

**Speaker:** Bin Wang  
**Time allocation:** 06:30–07:15 (45 seconds)

New loans require a phone number.
Older records may not have one.

The program adds the new database column automatically.
It keeps the earlier IDs, names and times.
A missing old phone appears as Not recorded.
It does not invent contacts.

I will now show the GUI.

**操作提示（不朗读）：** 慢速讲述；句号处自然停顿。解释旧记录升级，不清空数据库，不编造历史电话。累计 7:15，切到演示。

## Slide 7: Live GUI demonstration

**Speaker:** Bin Wang  
**Time allocation:** 07:15–09:30 (135 seconds)

This is a separate demo database.
I select Tablet and enter Demo A.

First, I leave the phone empty.
The system rejects the request.
Now I enter a fictional phone and record the loan.

The tablet shows On loan.
The borrow button is disabled while this tablet is on loan.
The history shows the borrower and phone.

I select this loan and return it.
The tablet is available again.
The returned record stays in history.

I close the window and reopen the same database.
The saved record is still here.
Returns use the Loan ID shown in the history.

**操作提示（不朗读）：** 本页 2:15 已包含边讲边操作。0–15 秒：选 Tablet，输入 Demo A；15–40 秒：空电话被拒，再填 0200000000 并借出；40–60 秒：展示 On loan 和历史；60–85 秒：选历史行归还；85–115 秒：关闭并重开同一数据库；115–135 秒：展示历史仍在，返回 PPT。实际操作时不必持续说话。

## Slide 8: Design choices and limits

**Speaker:** Bin Wang  
**Time allocation:** 09:30–10:00 (30 seconds)

Both interfaces share the same rules.
The system keeps returned loans in history.

This is a local prototype.
It has no shared server, login or encryption.

Yonghui will now discuss testing and the remaining work.

**操作提示（不朗读）：** 慢速讲述；句号处自然停顿。30 秒总结并交接。10:00 由 Yonghui 接手。

## Slide 9: Technical verification

**Speaker:** Yonghui Dai  
**Time allocation:** 10:00–11:30 (90 seconds)

Thank you. The recorded macOS checks passed twenty unit and GUI tests, plus twelve acceptance checks.
That includes twelve business and storage tests and eight GUI tests.

They cover borrowing, invalid input, duplicate loans, returns and saved history.
They also check phone contacts, both new devices and Unicode names.
Migration tests check that older records stay unchanged.
The GUI tests use real windows and controls with temporary databases.

These results came from assistant-run checks.
They do not show that students or a client accepted the product.

The Windows launcher is included, but it still needs a real Windows test.
The team should also test the extracted ZIP on the presentation computer.

**操作提示（不朗读）：** 20 项 unit/GUI 与另外 12 项 acceptance 分开说。Windows 仍为待实测。讲稿保留报告中 24 October 的已记录结果；本次 25 October 的重新解压复查也通过，但不冒充学生验收。

## Slide 10: Cultural considerations and Te Tiriti

**Speaker:** Yonghui Dai  
**Time allocation:** 11:30–13:00 (90 seconds)

The report considers partnership, participation and protection.

Partnership means seeking appropriate guidance.
Participation means giving relevant people a chance to influence the requirements.
Protection includes reviewing the information collected and stored.

Phone numbers make this important.
Before real use, the team needs to agree why contacts are needed, who can see them, and when to delete them.
The current demo uses fictional details.

The software preserves Unicode names and macrons.
This supports accurate text, but does not prove cultural suitability.
For example, a user should be able to ask why their phone is required.
Kaiārahi consultation is still open.
The prepared questions need appropriate advice and follow-up.
The team should record how advice changes the product.

**操作提示（不朗读）：** 慢速讲述；句号处自然停顿。用具体电话字段说明 protection；说明咨询仍待开展。累计 13:00。

## Slide 11: Reflection and next review

**Speaker:** Yonghui Dai  
**Time allocation:** 13:00–14:30 (90 seconds)

The current design gives us three points for reflection.

First, a small change can affect the whole system.
Adding a phone field affects the screen, rules, data model, database and tests.

Second, an upgrade should protect old records.
Tests should compare saved values and reopen the database.
A success message alone is not enough.

Third, team roles need shared understanding.
Each member should explain another component and review a complete borrowing path.
Personal reflections must use actual contributions and learning.
A dated review should name the people involved and link decisions to the source version.

The next steps are a presentation-machine check, client review and appropriate cultural guidance.
The reports should then record what actually happened.

**操作提示（不朗读）：** 慢速讲述；句号处自然停顿。反思使用分析语气，不声称未做过的团队活动。累计 14:30。

## Slide 12: Current release and next steps

**Speaker:** Yonghui Dai  
**Time allocation:** 14:30–15:00 (30 seconds)

The current release supports five devices, phone contacts, borrowing, returns and saved history.

The remaining work includes Windows testing, participant review and consultation.
The project is available on GitHub.

Thank you for listening.

**操作提示（不朗读）：** 结束和感谢。15 分钟是全场分配，不要求靠拖长单词填满。问答是否计入总时长仍以老师要求为准。

## 演示前准备

1. 完整解压当前 `02_Product.zip`，使用演示电脑上已验证可用的 Python/Tkinter。
2. Mac：`bash Start_GUI.command --db presentation_demo.db`。
   Windows：`Start_GUI.bat --db presentation_demo.db`。
3. 如果该文件已有彩排记录，改用新的文件名。不要删除或覆盖现有使用数据。
4. 提前打开 GUI 和用于重新启动的终端窗口，演示时不现场查找文件或安装软件。
5. 使用 `Demo A` 和虚构电话 `0200000000`，先演示空电话被拒绝，再填写电话。
6. 在第 7 页切换到真实 GUI；重启必须使用同一个数据库。
7. 如果 GUI 不能启动，保持同样的 2 分 15 秒时段，用第 7 页截图说明流程，并明确这是截图演示。
8. 第 8 页的归还记录截图用于解释历史保留。PPT 的截图来自临时演示数据，不含现有借用人的数据。

## 版本与技术证据

程序源版本：`d61c66ca11d2fd69c2bd40c005d3e4b53f65b100`。
当前文档中的技术结果来自 2026 年 10 月 24 日 Mac 上的助手执行：20 项 unittest（12 业务/存储＋8 GUI）及 12 项验收检查通过。
Windows 启动器尚未实机验证。文化咨询和个人反思须按后续实际参与补充。

## 彩排重点

1. 三个人连续彩排一次，并使用真正的电脑和 GUI。第一遍先求清楚，不求速度。
2. Xuerui 在第 3 页不逐项朗读全部规则；第 4 页不额外解释成本明细。
3. Bin 预先打开 GUI 和重启窗口，借还与重启时可以停顿，让观众看操作。
4. Yonghui 把测试数字分成两句说；文化部分使用本稿的短句，不临时加长解释。
5. 在约 5:00 和 10:00 交接。实际时间超出时，先减少临场发挥和重复说明，再决定是否进一步缩稿。
