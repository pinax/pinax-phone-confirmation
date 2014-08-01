def digits_only(phone, country_code=None):
    digits = []
    for x in phone:
        try:
            digits.append(str(int(x)))  # do this instead of re [^\d] to handle other digit encodings
        except ValueError:
            pass
    digits = "".join(digits)
    if country_code:
        digits = "%s%s" % (country_code.country_code, digits)
    return digits
