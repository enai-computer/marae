import os
from dotenv import load_dotenv

class SecretsService:
    def __init__(self, env: str):
        self.secrets = {}

        if env == "prod":
            self.fetch_secrets_from_aws()
        else:
            self.fetch_secrets_from_env()

    def fetch_secrets_from_env(self):
        load_dotenv()
        self.secrets = {
            "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY"),
            "OPENAI_ORG_ID": os.getenv("OPENAI_ORG_ID"),
            "OPENAI_PROJECT_ID": os.getenv("OPENAI_PROJECT_ID"),
            "PERPLEXITY_API_KEY": os.getenv("PERPLEXITY_API_KEY"),
            "JWT_SECRET_KEY": os.getenv("JWT_SECRET_KEY"),
            "JWT_ALGORITHM": os.getenv("JWT_ALGORITHM"),
            "JWT_ACCESS_TOKEN_EXPIRE_MINUTES": os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES"),
            "TEAM_ID": os.getenv("TEAM_ID"),
            "BUNDLE_ID": os.getenv("BUNDLE_ID"),
            "KEY_ID": os.getenv("KEY_ID"),
            "PRIVATE_KEY_PATH": os.getenv("PRIVATE_KEY_PATH"),
            "POSTHOG_API_KEY": os.getenv("POSTHOG_API_KEY"),
            "CEREBRAS_API_KEY": os.getenv("CEREBRAS_API_KEY")
        }

    def fetch_secrets_from_aws(self):
        self.fetch_secrets_from_env()
        self.secrets["PRIVATE_KEY_PATH"] = "env-data/prod-marae-dc.p8"

    def get_secret(self, secret_name):
        return self.get_secret_value_response[secret_name]

print("Run mode: ", os.getenv("RUN_MODE"))
secretsStore = SecretsService(os.getenv("RUN_MODE"))
