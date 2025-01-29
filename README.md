# MARAE

Provides EnAI.  

**deploys automatically to AWS ECR on push to main!**  
To deploy into production, pull latest terraform state from the backend-tf-config repo and run `terraform apply`.
  
**Run locally:** `fastapi run app/main.py`

---

**Current models:**

- OpenAI: gpt-4o <- new tab - 32k context window
- Anthropic: Claude 3.5 Sonnet - 80k context window
- Google: Gemini 1.5-flash-002 - 900k context window
- Cerebras: llama3.1-70b <- palette chat - 16k context window