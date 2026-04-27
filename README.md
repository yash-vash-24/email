# 📧 Intelligent Email Assistant

**AI-powered email automation** – Generate replies, categorize emails, and save time.

## Features
- Auto-generate professional email replies using AI
- Categorize emails by content and keywords  
- Multi-provider support (Gmail, Outlook, Yahoo, IMAP/SMTP)

## Setup
```bash
pip install -r requirements.txt
```
use .env.example to configure variables

## Run
```bash
# Web interface (recommended)
streamlit run app.py

# CLI
python main.py
```

## Tech Stack
Python • Hugging Face Transformers • LangChain • Streamlit • IMAP/SMTP

### Issue: Generated text is incomplete
**Solution:** Increase max_length parameter in generate_reply function

---

## References & Resources

- [Hugging Face Documentation](https://huggingface.co/)
- [Transformers Library](https://huggingface.co/docs/transformers)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [LangChain Documentation](https://python.langchain.com/)

---

## Author

**Name:** Yash Vashsith
**Roll Number:** 2301730149
**Project:** Intelligent Email Assistant
**Date:** 2024-2025

---

## Conclusion

The Intelligent Email Assistant demonstrates practical application of Generative AI in automating email communication. By combining Hugging Face models, LangChain, and Python, we create an efficient tool that saves time and improves email management productivity.

This project showcases:
- Integration of modern AI APIs
- Practical automation techniques
- User-friendly interface design
- Real-world application development

---

**Last Updated:** 2024
**Version:** 1.0
