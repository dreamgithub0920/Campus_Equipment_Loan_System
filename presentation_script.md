# MSE800 presentation script: 15 minutes, 5 minutes per speaker

更新日期：2026 年 10 月 25 日。对应 `04_Presentation_15min.pptx` 的 12 页。

## 使用说明

- 演讲顺序：Xuerui Huang（第 1–4 页）、Bin Wang（第 5–8 页）、Yonghui Dai（第 9–12 页）。
- 每人 5 分钟，合计 15 分钟。Bin 的 2 分 15 秒现场演示包含在其 5 分钟之内。
- 下表时间包含换页、操作和交接。英文正文用于演讲，中文提示不朗读。
- 页数与时间已经分配，实际语速仍需彩排校准。建议每人在 4 分 45 秒左右完成主要内容，保留交接余量。
- 学生个人经历、团队会议和咨询只能按实际情况表述。本文区分原课堂示例与当前实际技术成果。
- 这份安排不额外预留问答时间；若老师要求问答也计入 15 分钟，需要相应压缩正文。

## 逐页时间表

| 页 | 主题 | 演讲人 | 本页时长 | 全场时间 |
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
**Time:** 00:00–00:30 (30 seconds)

Good morning. We are Xuerui Huang, Bin Wang and Yonghui Dai. Our project is the Campus Equipment Loan System. It is a desktop application for a campus equipment desk. I will explain the requirements and planning. Bin will explain the design and demonstrate the product. Yonghui will discuss testing, cultural considerations and reflection.

**操作提示（不朗读）：** 封面；介绍姓名和分工。30 秒时换第 2 页。

## Slide 2: Equipment desk workflow

**Speaker:** Xuerui Huang  
**Time:** 00:30–01:30 (60 seconds)

The operator needs to answer a simple question: which device can someone borrow now? The system manages five devices: a laptop, camera, projector, tablet and microphone. The operator checks availability, records a loan, and later registers a return.

Each new loan includes a borrower name or alias and a phone contact. When the item comes back, the system keeps the record instead of deleting it. This helps the operator review both current and earlier borrowing.

The application runs locally with SQLite storage. It does not need a server or internet connection for normal use. Different computers keep separate records. We use fictional names and phone numbers in the demonstration.

**操作提示（不朗读）：** 指向设备清单和借还流程。此页结束时累计 1 分 30 秒。

## Slide 3: Requirements and priorities

**Speaker:** Xuerui Huang  
**Time:** 01:30–03:00 (90 seconds)

We organise the requirements into six user stories. The first is viewing equipment and its availability. The second is borrowing an available item with a name and phone. The third is returning an active loan. The fourth is reviewing history. The fifth is preserving records after a restart. The sixth is preserving Unicode characters in names, including macrons.

The core workflow and data preservation are Must requirements. History is a Should requirement, and the current product includes it. Each story has an observable acceptance criterion. For example, a duplicate borrowing request must leave the number of loans unchanged.

The phone is required for new loans. Its format allows seven to fifteen digits, with spaces, hyphens, parentheses and one leading plus. This checks the format only. It cannot confirm that a phone exists or belongs to the borrower. Online booking, accounts and payments remain outside the current scope.

**操作提示（不朗读）：** 不必逐字读表；重点解释 Must/Should 和电话规则。累计 3 分钟。

## Slide 4: Team, sprints and estimate

**Speaker:** Xuerui Huang  
**Time:** 03:00–05:00 (120 seconds)

The proposed division of work follows the main parts of the system. My role covers requirements, coordination and the interface. Bin's role covers domain objects, business rules and integration. Yonghui's role covers persistence, testing and evidence. Everyone should also review another component so that understanding does not depend on one person.

The report describes a baseline classroom case with two sprints. Sprint one focuses on inventory, borrowing and the storage foundation. Sprint two focuses on returns, history, integration and acceptance. Their estimates are twenty-three and thirty-one hours, giving fifty-four hours in total. These are written planning examples, rather than records of completed student meetings.

The later requests add the desktop interface, Windows startup support, two devices and a required phone contact. We keep those changes separate from the earlier case. The revised planning model adds twelve hours, suggested as four hours per member for adaptation and review. The current estimate is therefore sixty-six hours.

At thirty New Zealand dollars per hour, labour is one thousand nine hundred and eighty dollars. Adding thirty dollars for resources and a ten-percent contingency gives two thousand two hundred and eleven dollars. This is an estimate, not a record of payments or actual student hours. Bin will now explain the design and demonstrate the application.

**操作提示（不朗读）：** 保留估算和示例状态，不把计划说成已完成经历。可在 4:45 左右结束并交接；5:00 由 Bin 接手。

## Slide 5: Object-oriented structure

**Speaker:** Bin Wang  
**Time:** 05:00–06:30 (90 seconds)

Thank you. The design separates presentation, business rules and storage. LoanApp in gui.py displays the desktop interface. The original app.py provides a terminal interface. Both use the same LoanService, so changing the interface does not create a second set of borrowing rules.

LoanService receives an EquipmentRepository object through its constructor. This is composition. The service checks requests, while the repository handles SQLite queries and saved records. Equipment and Loan are data classes that carry information between these components.

For borrowing, the service checks the name and phone, finds the equipment and rejects an item that is already on loan. A database index also prevents two active loans for the same device. The service provides a readable message, and the database protects the stored rule. Tablet and Microphone use the existing Equipment model because they follow the same borrowing behaviour as the other devices.

**操作提示（不朗读）：** 讲清两个界面共用服务、组合关系、服务校验和数据库约束。累计 6:30。

## Slide 6: Phone storage and older records

**Speaker:** Bin Wang  
**Time:** 06:30–07:15 (45 seconds)

The phone change reaches every layer: input, validation, the Loan object, database storage and displayed history. New loans require a phone contact.

Older databases need a different treatment. The repository adds the borrower_phone column automatically. Existing identifiers, names and timestamps remain unchanged. A historical record without a phone shows Not recorded. The program keeps that gap visible instead of creating information that the borrower never supplied. I will now show the workflow in the GUI.

**操作提示（不朗读）：** 解释旧记录升级，不清空数据库，不编造历史电话。累计 7:15，切到演示。

## Slide 7: Live GUI demonstration

**Speaker:** Bin Wang  
**Time:** 07:15–09:30 (135 seconds)

This is a separate demonstration database. The inventory contains five devices. I am scrolling to Tablet and Microphone, then selecting Tablet.

I enter Demo A and first leave the phone empty. The program rejects the request. Now I enter the fictional contact zero two zero, followed by seven zeros, and record the loan.

The history shows a Loan ID, the name and the phone. The tablet now shows On loan, and its borrowing button is disabled.

I select that active loan and return it. The tablet becomes available again. The returned record and phone stay in history.

I will close the window and reopen the same database. The saved record remains. Returns use the loan record, because a loan ID can differ from the equipment ID.

**操作提示（不朗读）：** 本页 2 分 15 秒包含鼠标操作和重启时间。0–15 秒：选 Tablet；15–35 秒：空电话被拒并填写 0200000000；35–55 秒：借用并展示记录；55–80 秒：归还；80–115 秒：关闭并用同一命令重开；115–135 秒：确认历史。保持演示数据库一致。累计 9:30，返回 PPT。

## Slide 8: Design choices and limits

**Speaker:** Bin Wang  
**Time:** 09:30–10:00 (30 seconds)

These choices keep the project small enough to explain and test. Both interfaces share the same rules, and returns preserve history. The current product supports one workstation. It has no shared server, login or database encryption. Real campus use would need further controls and review. Yonghui will now explain our technical evidence and the remaining work.

**操作提示（不朗读）：** 30 秒总结并交接。10:00 由 Yonghui 接手。

## Slide 9: Technical verification

**Speaker:** Yonghui Dai  
**Time:** 10:00–11:30 (90 seconds)

Thank you. The current technical verification includes twelve business and storage checks, eight GUI checks, and twelve acceptance checks. All passed in the recorded assistant execution on macOS on the twenty-fourth of October. The GUI checks create real Tk widgets rather than checking only the business service.

The checks cover availability, borrowing, invalid input, duplicate protection, return, filtering, restart and Unicode names. They also exercise the required phone and the two additional devices. Migration checks compare older records before and after upgrading, including their identifiers and timestamps.

These observations support the tested software version. They do not establish that the three students personally ran the checks, or that a client accepted the product. Windows startup support is included, but a real Windows run is still needed. If the environment skips GUI checks because Tkinter or a desktop display is missing, that does not verify the interface on that computer.

**操作提示（不朗读）：** 区分 20 项 unittest（12 业务＋8 GUI）与另 12 项验收；不要说已在 Windows 实测。累计 11:30。

## Slide 10: Cultural considerations and Te Tiriti

**Speaker:** Yonghui Dai  
**Time:** 11:30–13:00 (90 seconds)

The report considers partnership, participation and protection. Partnership means seeking appropriate guidance before treating cultural decisions as settled. Participation means allowing relevant people to influence the requirements and review the interface. Protection includes examining what information the project collects and how it keeps that information.

The new phone requirement makes that discussion more specific. The prototype stores contacts locally without login or encryption. Before real use, the team needs agreement on why a contact is necessary, who can access it, and how long it should remain. Our demonstration uses fictional details.

The software preserves Unicode names, including macrons. That is a useful technical property, but it cannot establish cultural suitability. No actual Kaiārahi consultation or community approval is claimed. The prepared briefing asks about participation, language, contact collection and acceptance criteria. Those review questions remain open until the appropriate people contribute.

**操作提示（不朗读）：** 用具体电话字段说明 protection；说明咨询仍待开展。累计 13:00。

## Slide 11: Reflection and next review

**Speaker:** Yonghui Dai  
**Time:** 13:00–14:30 (90 seconds)

The case and current implementation give us several points to examine. A small change, such as requiring a phone, affects the screen, service, data model, database and tests. A requirement therefore needs to connect to each affected component and to an observable result.

Migration provides another example. A new column should not damage earlier loans or make missing contacts appear complete. Tests need to compare stored values and reopen the database, rather than rely only on a success message.

For teamwork, assigned roles and equal estimated hours are only a starting point. Each member should explain another component, review a complete borrowing path and record any unresolved question. Personal reflections should use actual contributions and learning rather than repeat the written scenario as an experience.

The next technical step is checking the extracted release on the presentation computer. The next participation steps are confirming the tutor's client arrangement and the appropriate advisory route, then recording how that input affects the project.

**操作提示（不朗读）：** 反思使用分析语气，不声称未做过的团队活动。累计 14:30。

## Slide 12: Current release and next steps

**Speaker:** Yonghui Dai  
**Time:** 14:30–15:00 (30 seconds)

To finish, the current release demonstrates five devices, required phone contacts, borrowing, returns and saved history through a desktop interface. The code and documents are available in the project repository. The remaining work includes Windows verification, participant review and the appropriate consultation. Thank you for listening. We are ready for your questions.

**操作提示（不朗读）：** 15:00 结束。若老师把问答计入 15 分钟，请相应缩短正文；当前安排不额外包含问答。

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
