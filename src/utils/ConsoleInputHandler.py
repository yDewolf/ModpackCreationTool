class ConsoleInputHandler:
    @staticmethod
    def selectFromOptions(message: str, options: list[str], last_as_zero: bool = True) -> int:
        # Print options:
        options_str = ""
        for option in options:
            options_str += f"{option}\n"
        
        print(options_str)

        while True:
            selected_choice = input(message)
            choice_idx = int(selected_choice) - 1

            if choice_idx > 0 and choice_idx < len(options):
                return choice_idx
    
    @staticmethod
    def confirmChoice(message: str):
        return bool(ConsoleInputHandler.selectFromOptions(message, ["Yes", "No"]))
