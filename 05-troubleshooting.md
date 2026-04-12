# Troubleshooting

Problem: 401 model not supported
Fix:
- Ensure `POC_MODEL=minimax-m2.7`
- Ensure base URL is `https://opencode.ai/zen/go/v1`

Problem: no runs in LangSmith
Fix:
- Check `LANGSMITH_TRACING=true`
- Verify `LANGSMITH_API_KEY` and project value

Problem: imports fail in scripts
Fix:
- Run from repo root
- Keep script bootstrap that inserts `src/` into `sys.path`
