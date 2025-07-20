from email_validator import validate_email, EmailNotValidError

def is_valid(email: str) -> bool:
    try:
        validate_email(email, allow_smtputf8=False, check_deliverability=True)
        return True
    except EmailNotValidError:
        return False
