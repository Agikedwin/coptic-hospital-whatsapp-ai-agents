

def phone_number_types(phone_no:str):
    cleaned = phone_no.replace(" ", "").replace("-", "")

    if cleaned.startswith("0") and len(cleaned) == 10:
        phone_no = "+254" + cleaned[1:]
    elif cleaned.startswith("254"):
        phone_no = "+" + cleaned
    else:
        phone_no = cleaned
    return phone_no