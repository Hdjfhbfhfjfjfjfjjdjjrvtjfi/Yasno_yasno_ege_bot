__all__ = ["add_administrator_command", "delete_administrator_command", "get_database_command",
           "add_school_grade_command", "add_question_command", "add_excursion_command",
           "add_knowledge_assesment_command"]
from aiogram.filters.command import BotCommand


add_administrator_command: BotCommand = BotCommand(
    command="add_administrator",
    description="add administrator to database"
)
"""Command for adding a new administrator to the system.

This command allows authorized users to add new administrators to the database.
The command requires appropriate permissions to execute.
"""

delete_administrator_command: BotCommand = BotCommand(
    command="delete_administrator",
    description="deletes administrator from database"
)
"""Command for removing an administrator from the system.

This command allows authorized users to remove existing administrators from the database.
The command requires appropriate permissions to execute.
"""

get_database_command: BotCommand = BotCommand(
    command="get_database",
    description="export database"
)
"""Command for exporting the database contents.

This command allows authorized users to export the current state of the database.
The command requires appropriate permissions to execute.
"""

add_school_grade_command: BotCommand = BotCommand(
    command="add_school_grade",
    description="add school grade to database"
)
"""Command for adding a new school grade to the system.

This command allows authorized users to add new school grades to the database.
The command requires appropriate permissions to execute.
"""

add_question_command: BotCommand = BotCommand(
    command="add_question",
    description="add question to database"
)
"""Command for adding a new question to the system.

This command allows authorized users to add new questions to the database.
The command requires appropriate permissions to execute.
"""

add_excursion_command: BotCommand = BotCommand(
    command="add_excursion",
    description="add excursion to database"
)
"""Command for adding a new excursion event to the system.

This command allows authorized users to add new excursion events to the database.
The command requires appropriate permissions to execute.
"""

add_knowledge_assesment_command: BotCommand = BotCommand(
    command="add_knowledge_assesment",
    description="add knowledge assessment to database"
)
"""Command for adding a new knowledge assessment to the system.

This command allows authorized users to add new knowledge assessment tests to the database.
The command requires appropriate permissions to execute.
"""
