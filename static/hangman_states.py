def get_hangman_stage(remaining_attempts):
    stages = [
        """
        ------
        |    |
        |    O
        |   /|\\
        |   / \\
        |
        """,
    ]
    return stages[6 - remaining_attempts]