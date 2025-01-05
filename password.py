import subprocess
import traceback

try:
    data = subprocess.check_output("netsh wlan show profiles").decode("cp866").split("\n")
    profiles = [el.split(":")[1].strip() for el in data if "Все профили пользователей" in el] # Use strip to remove whitespace
    result_password = 'Мои мои wifi с паролями:\n'
    for profile in profiles:
        try:
            result = subprocess.check_output(
                ['netsh', 'wlan', 'show', 'profile', profile, 'key=clear']  # Correct typo here 'profiles' to 'profile'
            ).decode("cp866").split("\n")
            for inner_result in result:
                if "Содержимое ключа" in inner_result:
                    result_password += f"\t{profile} -> {inner_result.split(':')[1].strip()}\n"  # Use strip for the password
        except subprocess.CalledProcessError as e:
              result_password += f"\tError getting password for profile {profile}: {e}\n" # Error output
        except Exception as e:
             result_password += f"\tError getting password for profile {profile}: {e}\n"  # Generic Error output

    print(result_password)
except Exception as e:
    traceback.print_exc()

