# Product backlog


| Story | Requirement and acceptance | Priority / value | Scenario lead | Sprint | Evidence |
| --- | --- | --- | --- | --- | --- |
| US01 | As an operator, I want to see equipment availability so that I can respond to a loan request. Acceptance: Laptop, Camera, Projector, Tablet and Microphone each show a unique ID, name and correct Available or On loan status. | Must: Enables loan decisions | Xuerui Huang + Yonghui Dai | 1 | Implemented; AT01 passed |
| US02 | As an operator, I want to record a loan so that equipment use is tracked. Acceptance: A valid device ID, alias and required phone contact create one active loan. Reject unavailable/unknown devices, invalid aliases and missing/invalid phones without adding a record. Phone input contains 7-15 digits; spaces, hyphens, parentheses and one leading + are allowed (maximum 30 characters). | Must: Core workflow; prevents conflicts | Bin Wang + Xuerui Huang | 1 | Implemented; AT02-AT04 passed |
| US03 | As an operator, I want to register a return so that the device can be lent again. Acceptance: Returning an active loan records a timestamp and restores availability. Reject unknown or already returned loans; keep the history. | Must: Completes the loan lifecycle | Bin Wang | 2 | Implemented; AT05-AT06 passed |
| US04 | As an operator, I want loan history so that I can check previous and current use. Acceptance: Show loan ID, device, alias, phone, borrowing time and active/returned status. Old records without a phone show Not recorded. Explain when no records exist. | Should: Supports accountability | Xuerui Huang + Yonghui Dai | 2 | Implemented; AT07 passed |
| US05 | As an operator, I want saved records to survive a restart so that loan information is not lost. Acceptance: Reopening the same database preserves history and availability without duplicating the five seed devices. Automatically upgrade the earlier schema without deleting loans or inventing phone contacts. | Must: Prevents loss of records | Yonghui Dai | 1-2 | Implemented; AT08 passed |
| US06 | As a user with macrons or other Unicode characters in my alias, I want them preserved so that my alias is represented accurately. Acceptance: Save and retrieve a fictional alias such as Māia unchanged, including after restart. Do not request ethnicity; collect only the phone contact required by US02 alongside the alias. | Must: Supports respectful text handling | Xuerui Huang + Yonghui Dai | 1-2 | Implemented; AT09 passed |

CF04: online booking deferred; requires new date/conflict/access requirements and a revised estimate. No baseline commitment.


## Current release extension - 24 October 2026

The project owner requested Tablet and Microphone (fixed IDs 4 and 5) and a required
borrower phone contact. The current release implements these changes in
the GUI, CLI, service and SQLite repository. They were added after the recorded
GitHub baseline and the original written sprint example. The Project Report
sections 3 and 3.1 now contain these same current requirements.

Current technical evidence: US01/US02/US03 additionally map to AT11 (new devices);
US02/US04/US05 map to AT12 (phone validation and persistence). The unit suite
also checks preservation of legacy records during schema migration. 
