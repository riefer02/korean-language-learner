# Korean Language Learner

An application for learning Korean that includes both a command-line interface and a web application. Translate English phrases to Korean, generate pronunciation audio, and practice your skills through a structured learning interface.

## Features

### CLI Tool

- Translates English text to Korean using OpenAI's `gpt-4o` model
- Generates natural-sounding Korean speech using OpenAI's Text-to-Speech (TTS) API
- Saves audio output as MP3 files in the `audio_output/` directory
- Accepts input either interactively or as a command-line argument

### Web Application

- User-friendly interface for translation and learning
- Interactive practice exercises for Korean vocabulary and phrases
- Audio playback of Korean pronunciations
- Progress tracking for learning journey
- SQLite database for storing user data and learning materials

## Prerequisites

- Python 3.7.1 or newer
- An OpenAI API key
- Flask and related packages (see `requirements.txt`)

## Setup

1. **Clone the repository:**

   ```bash
   git clone <repository-url>
   cd korean-language-learner
   ```

2. **Create a `.env` file:**
   Create a file named `.env` in the project root directory and add your OpenAI API key:

   ```
   OPENAI_API_KEY='your_openai_api_key_here'
   ```

   _(This file is ignored by Git via `.gitignore`)_

3. **Set up the environment and install dependencies:**
   It's recommended to use a virtual environment.

   ```bash
   make install
   ```

   This command will:

   - Create a Python virtual environment named `venv`
   - Activate the environment
   - Install the required packages listed in `requirements.txt`

   _Alternatively, you can set up the virtual environment and install packages manually:_

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   pip install -r requirements.txt
   ```

## Usage

### CLI Tool

Make sure your virtual environment is active (`source venv/bin/activate` or use the `make` commands).

- **Interactive Mode:**

  ```bash
  make run
  ```

  The script will prompt you to enter an English phrase.

- **With a Phrase Argument:**

  ```bash
  make runp phrase="I want to learn Korean"
  ```

  Replace "I want to learn Korean" with your desired phrase.

- **Directly with Python:**
  ```bash
  python hangul.py  # Interactive mode
  python hangul.py "Where is the library?"  # With argument
  ```

### Web Application

To run the web application:

1. Ensure your virtual environment is active
2. Start the Flask development server:
   ```bash
   python run.py
   ```
3. Open your web browser and navigate to `http://localhost:5000`

## Project Structure

- `/app` - Web application components
  - `/services` - Backend services for translation, audio, etc.
  - `/static` - Static assets (CSS, JS, audio files)
  - `/templates` - HTML templates
  - `/utils` - Utility functions
- `/audio_output` - Generated audio files from the CLI tool
- `hangul.py` - CLI tool entry point
- `run.py` - Web application entry point
- `config.py` - Configuration settings
- `korean_learner.db` - SQLite database

## Cleaning Up

To remove the virtual environment, audio output directory, and compiled Python files:

```bash
make clean
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
