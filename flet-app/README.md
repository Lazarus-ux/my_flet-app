# Flet Web Portfolio

This folder contains the live browser portfolio for Lazarus Shiyelekeni.

It is built with Flet and organized into these sections:

- Project Timeline
- MATLAB Achievement Hub
- Technical Blog
- GitHub Evidence & Documentation
- Contact

Run steps:

1. Install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
```

2. Start the app:

```bash
python main.py
```

Notes:
- The app runs in browser mode and listens on `8550` locally on Windows or `8000` in Linux/container environments unless `PORT` or `FLET_SERVER_PORT` is provided.
- Local runs open on `127.0.0.1`; cloud deployments bind to `0.0.0.0` when `PORT` or `FLET_FORCE_WEB_SERVER` is present.
- The MATLAB section links the certificate PDFs found in `public/certificates`.
- The contact buttons open your phone, email, GitHub, LinkedIn, and Instagram links directly.
- The blog section includes visible video insert slots so you can drop in short explanation clips later if needed.
