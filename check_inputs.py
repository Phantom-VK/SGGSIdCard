def branch_check(branch):
    branches = ["bit", "bec", "bpd", "bel", "bcs"]
    return branch in branches


def check_reg(registration: str):
    registration = registration.lower()
    if len(registration) != 10:
        return False

    if not registration[:3].isdigit() or not registration[7:].isdigit():
        return False

    if not branch_check(registration[4:7]):
        return False

    print(registration)
    return True

# # Example usage
# reg = "123bit4567"
# is_valid = check_reg(reg)
# print(f"Is the registration valid? {is_valid}")
