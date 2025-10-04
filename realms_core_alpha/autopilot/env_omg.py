from dotenv import dotenv_values
env_path = "F:/Realms/realms_core_alpha/.env"
env_vars = dotenv_values(env_path)
for key, val in env_vars.items():
    print(f"{key} = {val}")