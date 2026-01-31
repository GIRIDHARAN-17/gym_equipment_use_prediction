# Gym Equipment Usage Prediction

A minimal README for this project with quick setup and notes about environment files and gitignore.

## Quick Start ✅

1. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   venv\Scripts\activate   # Windows
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Train the model (if not already done):
   ```bash
   python train_model.py
   ```
4. Run the app:
   ```bash
   python app.py
   ```

## Notes 🔧

- This project includes `app.py`, `train_model.py`, the `models/` folder, `templates/` and `static/` assets.
- A `.env.example` is provided (or create a `.env` file) with suggested environment variables. Copy `.env.example` to `.env` and edit values as needed. **Do not commit a real `.env`** containing secrets — keep it local and ignored by Git.
- `.gitignore` includes common Python ignores and **ignores `models/*.pkl` by default** to avoid committing large model files. Remove that line if you want to commit trained models.

## Useful docs

- See `README_FLASK.md` and `HOW_TO_RUN.md` for detailed instructions and troubleshooting.
