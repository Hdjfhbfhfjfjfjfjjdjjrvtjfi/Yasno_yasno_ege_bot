__all__ = ["USER_DATA_ARGUMENT_NAME", "TEST_RESULT_DATA_ARGUMENT_NAME", "SCHOOL_GRADE_DATA_ARGUMENT_NAME",
           "QUESTION_DATA_ARGUMENT_NAME", "EVENT_DATA_ARGUMENT_NAME", "CONFIG_ARGUMENT_NAME",
           "STATE_CONTEXT_ARGUMENT_NAME", "COMMAND_ARGUMENT_NAME"]


USER_DATA_ARGUMENT_NAME = "user_data"
"""Name of the argument used to pass user data between handlers.

This constant represents the key used in the state data dictionary to store and retrieve
user-related information during the bot's operation.
"""

TEST_RESULT_DATA_ARGUMENT_NAME = "test_result_data"
"""Name of the argument used to pass knowledge assessment test results between handlers.

This constant represents the key used in the state data dictionary to store and retrieve
test results and related data during knowledge assessment operations.
"""

SCHOOL_GRADE_DATA_ARGUMENT_NAME = "school_grade_data"
"""Name of the argument used to pass school grade information between handlers.

This constant represents the key used in the state data dictionary to store and retrieve
school grade-related information during bot operations.
"""

QUESTION_DATA_ARGUMENT_NAME = "question_data"
"""Name of the argument used to pass question data between handlers.

This constant represents the key used in the state data dictionary to store and retrieve
question-related information when adding or managing questions in the system.
"""

EVENT_DATA_ARGUMENT_NAME = "event_data"
"""Name of the argument used to pass event information between handlers.

This constant represents the key used in the state data dictionary to store and retrieve
event-related information for both excursions and knowledge assessment events.
"""

CONFIG_ARGUMENT_NAME = "config"
STATE_CONTEXT_ARGUMENT_NAME = "state"
COMMAND_ARGUMENT_NAME = "command"