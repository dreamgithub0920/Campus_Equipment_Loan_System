# Product backlog


| Story | Requirement and acceptance | Priority / value | Scenario lead | Sprint | Evidence |
| --- | --- | --- | --- | --- | --- |
| US01 | As an operator, I want to see equipment availability so that I can respond to a loan request. Acceptance: Each item shows a unique ID, name and correct Available or On loan status. | Must: Enables loan decisions | Xuerui Huang + Yonghui Dai | 1 | Implemented; AT01 passed 
| US02 | As an operator, I want to record a loan so that equipment use is tracked. Acceptance: A valid device ID and alias create one active loan. Reject unavailable or unknown devices and blank, overlong or non-printable aliases without adding a record. | Must: Core workflow; prevents conflicts | Bin Wang + Xuerui Huang | 1 | Implemented; AT02-AT04 passed 
| US03 | As an operator, I want to register a return so that the device can be lent again. Acceptance: Returning an active loan records a timestamp and restores availability. Reject unknown or already returned loans; keep the history. | Must: Completes the loan lifecycle | Bin Wang | 2 | Implemented; AT05-AT06 passed
| US04 | As an operator, I want loan history so that I can check previous and current use. Acceptance: Show loan ID, device, alias, borrowing time and active/returned status. Explain when no records exist. | Should: Supports accountability | Xuerui Huang + Yonghui Dai | 2 | Implemented; AT07 passed 
| US05 | As an operator, I want saved records to survive a restart so that loan information is not lost. Acceptance: Reopening the same database preserves history and availability without duplicating the seed equipment. | Must: Prevents loss of records | Yonghui Dai | 1-2 | Implemented; AT08 passed 
| US06 | As a user with macrons or other Unicode characters in my alias, I want them preserved so that my alias is represented accurately. Acceptance: Save and retrieve a fictional alias such as Māia unchanged, including after restart. Do not request ethnicity or contact details. | Must: Supports respectful text handling | Xuerui Huang + Yonghui Dai | 1-2 | Implemented; AT09 passed 

CF04: online booking deferred; requires new date/conflict/access requirements and a revised estimate. No baseline commitment.
