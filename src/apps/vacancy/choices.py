from django.utils.translation import gettext_lazy as _


class TestProjectStatus:
    """
    Status of the TestProject
    """
    NEW = 'new'
    IN_PROCESS = 'in_process'
    COMPLETED = 'completed'
    ON_CHECKING = 'on_checking'
    REJECTED = 'rejected'

    ITEMS = [
        NEW,
        IN_PROCESS,
        COMPLETED,
        ON_CHECKING,
        REJECTED,
    ]

    CHOICES = (
        (NEW, _('New')),
        (IN_PROCESS, _('In process')),
        (COMPLETED, _('Completed')),
        (ON_CHECKING, _('On checking')),
        (REJECTED, _('Rejected')),
    )


class VacancyStatus:
    """
    Statuses of the vacancy:
     - new
     - resume_sent
     - rejected
     - invited_to_an_interview
     - received_task
     - completed_task
     - task_sent
     - passed
    """
    NEW = 'new'
    RESUME_SENT = 'resume_sent'
    REJECTED = 'rejected'
    INVITED_TO_AN_INTERVIEW = 'invited_to_an_interview'
    RECEIVED_TASK = 'received_task'
    COMPLETED_TASK = 'completed_task'
    TASK_SENT = 'task_sent'
    PASSED = 'passed'

    ITEMS = (
        NEW,
        RESUME_SENT,
        REJECTED,
        INVITED_TO_AN_INTERVIEW,
        RECEIVED_TASK,
        COMPLETED_TASK,
        TASK_SENT,
        PASSED,
    )

    CHOICES = (
        (NEW, _('New')),
        (RESUME_SENT, _('Resume sent')),
        (REJECTED, _('Rejected')),
        (INVITED_TO_AN_INTERVIEW, _('Invited to an interview')),
        (RECEIVED_TASK, _('Received task')),
        (COMPLETED_TASK, _('Completed task')),
        (TASK_SENT, _('Task sent')),
        (PASSED, _('Passed')),
    )


class LanguageLevels:
    A1 = 'a1'
    A2 = 'a2'
    B1 = 'b1'
    B2 = 'b2'
    C1 = 'c1'
    C2 = 'c2'

    ITEMS = [
        A1,
        A2,
        B1,
        B2,
        C1,
        C2,
    ]

    CHOICES = (
        (A1, _('A1')),
        (A2, _('A2')),
        (B1, _('B1')),
        (B2, _('B2')),
        (C1, _('C1')),
        (C2, _('C2')),
    )
