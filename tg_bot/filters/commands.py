__all__ = ["add_administrator_command", "delete_administrator_command", "get_database_command",
           "add_school_grade_command", "add_question_command", "add_excursion_command",
           "add_knowledge_assesment_command"]
from aiogram.filters.command import BotCommand


add_administrator_command: BotCommand = BotCommand(
    command="add_administrator",
    description="add administrator to database"
)
delete_administrator_command: BotCommand = BotCommand(
    command="delete_administrator",
    description="deletes administrator from database"
)
get_database_command: BotCommand = BotCommand(
    command="get_database",
    description="export database"
)
add_school_grade_command: BotCommand = BotCommand(
    command="add_school_grade",
    description="add school grade to database"
)
add_question_command: BotCommand = BotCommand(
    command="add_question",
    description="add question to database"
)
add_excursion_command: BotCommand = BotCommand(
    command="add_excursion",
    description="add excursion to database"
)
add_knowledge_assesment_command: BotCommand = BotCommand(
    command="add_knowledge_assesment",
    description="add knowledge assessment to database"
)
