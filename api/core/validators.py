class AbstractValidator:
    def validate(self) -> None:
        """
        Call all validators in class.
        """
        for validator in dir(self):
            if validator.startswith("validate_"):
                try:
                    getattr(self, validator)()
                except TypeError:
                    pass
