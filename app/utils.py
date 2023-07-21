MIN_LENGHT = 8

def check_valid_password(psw):
    up_case = False
    lw_case = False
    num = False
    sp_char = False

    if len(psw) < MIN_LENGHT:
        return f"The password must have a length greater equal {MIN_LENGHT}"

    for char in psw:
        if char.isdigit():
            num = True
        elif char.isalpha():
            if char.upper() == char:
                up_case = True
            else:
                lw_case = True
        else:
            sp_char = True
    
    if not up_case:
        return "The password must contain an uppercase alphabet character"
    if not lw_case:
        return "The password must contain an lowercase alphabet character"
    if not num:
        return "The password must contain a numeric character"
    if not sp_char:
        return "The password must contain a special character like: !£$%&*"
    return None