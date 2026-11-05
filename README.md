<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=6,11,20&height=220&section=header&text=HR%20Assist&fontSize=72&fontColor=ffffff&animation=fadeIn&fontAlignY=36&desc=AI-powered%20HR%20Management%20over%20MCP&descAlignY=58&descSize=20" width="100%" alt="HR Assist banner" />

<a href="https://github.com/rushikreddie/HR-Management-System">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=22&duration=3000&pause=900&color=A78BFA&center=true&vCenter=true&width=720&lines=Onboard+employees+with+one+prompt;Manage+leaves%2C+meetings+and+tickets;Send+emails+straight+from+your+AI+assistant;Built+on+the+Model+Context+Protocol+%F0%9F%9A%80" alt="Typing animation" />
</a>

<br/>

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![MCP](https://img.shields.io/badge/Model%20Context%20Protocol-Server-8A2BE2?style=for-the-badge)
![Pydantic](https://img.shields.io/badge/Pydantic-v2-E92063?style=for-the-badge&logo=pydantic&logoColor=white)
![SMTP](https://img.shields.io/badge/Email-SMTP%20%2F%20Gmail-EA4335?style=for-the-badge&logo=gmail&logoColor=white)
![Status](https://img.shields.io/badge/Status-Active-22c55e?style=for-the-badge)

**Talk to your HR system in plain English.**
HR Assist exposes employee, leave, meeting, ticket and email operations as [MCP](https://modelcontextprotocol.io) tools, so any MCP-compatible AI client can run HR workflows for you.

</div>

---

## ✨ Features

<table>
<tr>
<td width="50%" valign="top">

### 👥 Employee Management
- Add employees with auto-generated IDs (`E001`, `E002`, ...)
- Fuzzy name search to look up employee details
- Manager hierarchy and direct-report lookup

### 🌴 Leave Management
- Check leave balance
- Apply for leave on one or more dates
- View full leave history

</td>
<td width="50%" valign="top">

### 📅 Meeting Scheduler
- Schedule meetings with **conflict detection**
- List upcoming meetings, sorted by date
- Cancel by date and (optional) topic

### 🎫 IT / Equipment Tickets
- Raise tickets for laptops, ID cards and more
- Update status: `Open`, `In Progress`, `Closed`, `Rejected`
- Filter tickets by employee and status

</td>
</tr>
<tr>
<td colspan="2" valign="top">

### 📧 Email Automation &nbsp;·&nbsp; 🧭 Guided Onboarding
Send plain-text or HTML emails (with attachments) through SMTP, and trigger the built-in **`onboard_new_employee`** prompt that walks the AI through a complete onboarding checklist.

</td>
</tr>
</table>

---

## 🏗️ Architecture

```text
 ┌──────────┐     ┌──────────────────┐   stdio   ┌───────────────────────┐
 │   User   │ ──▶ │  MCP Client (AI) │ ◀───────▶ │  HR Assist MCP Server │
 └──────────┘     └──────────────────┘           │       server.py       │
                                                 └───────────┬───────────┘
        ┌───────────────┬───────────────┬────────────────────┼───────────────┐
        ▼               ▼               ▼                    ▼               ▼
 ┌─────────────┐ ┌─────────────┐ ┌──────────────┐   ┌───────────────┐ ┌─────────────┐
 │  Employee   │ │    Leave    │ │   Meeting    │   │    Ticket     │ │ EmailSender │
 │  Manager    │ │   Manager   │ │   Manager    │   │    Manager    │ │  emails.py  │
 └─────────────┘ └─────────────┘ └──────────────┘   └───────────────┘ └──────┬──────┘
        ▲               ▲               ▲                    ▲               │ SMTP
        └───────────────┴───────┬───────┴────────────────────┘               ▼
                                │                                     ┌─────────────┐
                       seed_services() dummy data                     │ Gmail / SMTP│
                                                                      └─────────────┘
```

---

## 🧰 MCP Tools

| Tool | What it does | Key arguments |
|------|--------------|---------------|
| `add_employee` | Create a new employee | `emp_name`, `manager_id?`, `email?` |
| `get_employee_details` | Find an employee by (fuzzy) name | `name` |
| `email_sender` | Send an email | `subject`, `body`, `to_emails` |
| `create_ticket` | Raise an equipment / IT ticket | `emp_id`, `item`, `reason` |
| `update_ticket_status` | Change a ticket's status | `ticket_id`, `status` |
| `list_tickets` | List tickets for an employee | `employee_id`, `status` |
| `schedule_meeting` | Book a meeting (conflict-checked) | `employee_id`, `meeting_datetime`, `topic` |
| `get_meetings` | List an employee's meetings | `employee_id` |
| `cancel_meeting` | Cancel a meeting | `employee_id`, `meeting_datetime`, `topic` |
| `get_employee_leave_balance` | Remaining leave days | `emp_id` |
| `apply_leave` | Apply for leave dates | `emp_id`, `leave_dates` |
| `get_leave_history` | Past leave records | `emp_id` |

### 💬 Built-in Prompt

**`onboard_new_employee(employee_name, manager_name)`** guides the assistant through:

1. ➕ Add the employee to the HRMS
2. 📧 Send a welcome email (`employee_name@abc.com`)
3. 📨 Notify the manager
4. 🎫 Raise tickets for laptop, ID card and other equipment
5. 📅 Schedule an intro meeting with the manager

---

## 📁 Project Structure

```text
HR-Management-System/
└── hr_assist/
    ├── __init__.py              # package entry point
    ├── main.py                  # simple runner
    ├── server.py                # 🚀 MCP server (tools + prompt)
    ├── emails.py                # SMTP email sender
    ├── utils.py                 # seed_services(): realistic dummy data
    ├── .env                     # SMTP credentials (not committed)
    └── hrms/
        ├── __init__.py
        ├── schemas.py           # Pydantic models (Employee, Leave, Meeting, Ticket)
        ├── employee_manager.py  # employees, managers, fuzzy search
        ├── leave_manager.py     # balances, applications, history
        ├── meeting_manager.py   # schedule / list / cancel
        └── ticket_manager.py    # create / update / list tickets
```

---

## 🚀 Getting Started

### 1. Clone

```bash
git clone https://github.com/rushikreddie/HR-Management-System.git
cd HR-Management-System
```

### 2. Install dependencies

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install mcp pydantic python-dotenv
```

### 3. Configure email

Create a `.env` file inside the `hr_assist/` folder (next to `server.py`):

```env
SMTP_EMAIL=your_address@gmail.com
SMTP_APP_PASSWORD=your_16_char_google_app_password
```

> 💡 For Gmail, enable 2-Step Verification and generate an **App Password**. Your normal password will not work.
> 🔒 Never commit `.env`. Add it to `.gitignore`.

### 4. Run the server

```bash
cd hr_assist
python server.py
```

The server speaks MCP over **stdio**, so it is normally launched by an MCP client rather than used directly.

### 5. Connect an MCP client

Add this to your client's MCP configuration (for example Claude Desktop):

```json
{
  "mcpServers": {
    "hr-assist": {
      "command": "python",
      "args": ["/absolute/path/to/HR-Management-System/hr_assist/server.py"],
      "cwd": "/absolute/path/to/HR-Management-System/hr_assist"
    }
  }
}
```

---

## 🎬 Example Conversations

> **You:** Onboard Priya Nair, her manager is David Wilson.
> **Assistant:** Adds Priya, emails her, notifies David, raises laptop and ID card tickets, and schedules an intro meeting. ✅

> **You:** How many leave days does E004 have left?
> **Assistant:** `E004 has 12 leave days remaining.`

> **You:** Book a 1:1 for E003 tomorrow at 3pm about Q4 planning.
> **Assistant:** `Meeting scheduled for E003 on 2026-11-06T15:00:00 about 'Q4 planning'.`

---

## 🧪 Demo Data

On startup, `seed_services()` fills the in-memory managers with realistic sample data so you can try everything right away:

| Data | Seeded |
|------|--------|
| 👥 Employees | 8, across a 3-level reporting hierarchy |
| 🌴 Leave | Random balances (5-20 days) plus recent history |
| 📅 Meetings | 2-6 upcoming meetings per employee |
| 🎫 Tickets | 8-15 tickets with mixed statuses |

---

## 🛣️ Roadmap

- [ ] 💾 Persistent storage (SQLite / PostgreSQL) instead of in-memory
- [ ] 🔐 Role-based access control
- [ ] 📚 RAG over HR policy documents (MCP resources)
- [ ] 🗓️ Calendar integration (Google / Outlook)
- [ ] 🧪 Unit tests and CI pipeline
- [ ] 🐳 Docker support

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Protocol | Model Context Protocol (MCP) |
| Language | Python |
| Validation | Pydantic v2 |
| Email | `smtplib` + `EmailMessage` (STARTTLS / SSL) |
| Config | `python-dotenv` |

---

## 🤝 Contributing

Contributions, issues and feature requests are welcome!

1. Fork the repo
2. Create your branch: `git checkout -b feature/amazing-feature`
3. Commit: `git commit -m "Add amazing feature"`
4. Push: `git push origin feature/amazing-feature`
5. Open a Pull Request

---

<div align="center">

### 👨‍💻 Author

**Nalla Rushik Reddy**
AI / ML Engineer · Hyderabad, India

[![GitHub](https://img.shields.io/badge/GitHub-rushikreddie-181717?style=for-the-badge&logo=github)](https://github.com/rushikreddie)

⭐ **If you found this useful, give it a star!** ⭐

<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=6,11,20&height=120&section=footer" width="100%" alt="footer" />

</div>
