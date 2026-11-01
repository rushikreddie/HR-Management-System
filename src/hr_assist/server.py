from mcp.server.mcpserver import MCPServer
from typing import List, Dict , Optional,Any
from hrms import *
from hrms.schemas import TicketCreate, MeetingCreate, EmployeeCreate, MeetingCancelRequest,LeaveApplyRequest,datetime,TicketStatusUpdate
from utils import seed_services
from emails import EmailSender
import os
from dotenv import load_dotenv

_ = load_dotenv()

emailer = EmailSender(
        smtp_server="smtp.gmail.com",
        port=587,
        username=os.getenv("SMTP_EMAIL"),
        password=os.getenv("SMTP_APP_PASSWORD"),
        use_tls=True
    )

mcp = MCPServer("hr-assist")

employee_manager = EmployeeManager()
leave_manager = LeaveManager()
meeting_manager = MeetingManager()
ticket_manager = TicketManager()

seed_services(employee_manager,leave_manager,meeting_manager,ticket_manager)

#tools
#resources(knowledge)
#prompt


@mcp.tool()
def add_employee(emp_name: str, manager_id: Optional[str] = None, email: Optional[str] = None) -> str:
    emp = EmployeeCreate(
        emp_id = employee_manager.get_next_emp_id(),
        name = emp_name,
        manager_id = manager_id,
        email= email
    )
    employee_manager.add_employee(emp)
    return f" Employee {emp_name} added Successfully"

@mcp.tool()
def get_employee_details(name: str) -> Dict[str, Any]:
    """
    Get employee details
    :param name:
    :return:
    """
    matches = employee_manager.search_employee_by_name(name)
    if len(matches) == 0:
        raise ValueError(f"No employee with this name exists")

    emp_id = matches[0]
    return employee_manager.get_employee_details(emp_id)


@mcp.tool()
def email_sender(subject:str,body:str,to_emails : List[str]):
    emailer.send_email(
        subject=subject,
        body=body,
        to_emails=to_emails,
        from_email=emailer.username
    )
    return f" Email sent Successfully"

@mcp.tool()
def create_ticket(emp_id:str, item : str, reason : str) -> str:
    ticket_req = TicketCreate(
        emp_id = emp_id,
        item = item,
        reason = reason
    )

    return ticket_manager.create_ticket(ticket_req)

@mcp.tool()
def update_ticket_status(ticket_id: str, status: str) -> str:
    """
    Update the status of a ticket.
    :param ticket_id: Ticket ID
    :param status: New status of the ticket
    :return: Confirmation message
    """
    ticket_status_update = TicketStatusUpdate(status=status)
    return ticket_manager.update_ticket_status(ticket_status_update, ticket_id)

@mcp.tool()
def list_tickets(employee_id: str, status: str) -> str:
    """
    List tickets for an employee with optional status filter.
    :param employee_id: Employee ID
    :param status: Ticket status (optional)
    :return: List of tickets
    """
    return ticket_manager.list_tickets(employee_id=employee_id, status=status)



@mcp.tool()
def schedule_meeting(employee_id: str, meeting_datetime: datetime, topic: str) -> str:
    """
    Schedule a meeting for an employee.
    :param employee_id: Employee ID
    :param meeting_datetime: Date and time of the meeting in python datetime format
    :param topic: Topic of the meeting
    :return: Confirmation message
    """
    meeting_req = MeetingCreate(
        emp_id=employee_id,
        meeting_dt=meeting_datetime,
        topic=topic
    )
    return meeting_manager.schedule_meeting(meeting_req)


@mcp.tool()
def get_meetings(employee_id: str) -> str:
    """
    Get the list of meetings scheduled for an employee.
    :param employee_id: Employee ID
    :return: List of meetings
    """
    return meeting_manager.get_meetings(employee_id)


@mcp.tool()
def cancel_meeting(employee_id: str, meeting_datetime: datetime, topic: str) -> str:
    """
    Cancel a scheduled meeting for an employee.
    :param employee_id: Employee ID
    :param meeting_datetime: Date and time of the meeting in python datetime format
    :param topic: Topic of the meeting (optional)
    :return: Confirmation message
    """
    meeting_req = MeetingCancelRequest(
        emp_id=employee_id,
        meeting_dt=meeting_datetime,
        topic=topic
    )
    return meeting_manager.cancel_meeting(meeting_req)


@mcp.tool()
def get_employee_leave_balance(emp_id: str) -> str:
    """
    Get the leave balance of an employee.
    :param emp_id: Employee ID
    :return: Leave balance message
    """
    return leave_manager.get_leave_balance(emp_id)

@mcp.tool()
def apply_leave(emp_id: str, leave_dates: list) -> str:
    """
    Apply for leave for an employee.
    :param emp_id: Employee ID
    :param leave_dates: List of leave dates
    :return: Leave application status message
    """
    req = LeaveApplyRequest(emp_id=emp_id, leave_dates=leave_dates)
    return leave_manager.apply_leave(req)


@mcp.tool()
def get_leave_history(emp_id: str) -> str:
    """
    Get the leave history of an employee.
    :param emp_id: Employee ID
    :return: Leave history message
    """
    return leave_manager.get_leave_history(emp_id)



@mcp.prompt("onboard_new_employee")
def onboard_new_employee(employee_name: str, manager_name: str):
    return f"""Onboard a new employee with the following details:
    - Name: {employee_name}
    - Manager Name: {manager_name}
    Steps to follow:
    - Add the employee to the HRMS system.
    - Send a welcome email to the employee with their login credentials. (Format: employee_name@abc.com)
    - Notify the manager about the new employee's onboarding.
    - Raise tickets for a new laptop, id card, and other necessary equipment.
    - Schedule an introductory meeting between the employee and the manager.
    """


if __name__ == "__main__":
    mcp.run(transport = "stdio")