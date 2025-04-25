# Korean Language Learner CLI

This command-line tool translates English phrases into Korean and generates an MP3 audio file of the Korean translation using the OpenAI API.

## Features

- Translates English text to Korean using OpenAI's `gpt-4o` model (or user-specified).
- Generates natural-sounding Korean speech using OpenAI's Text-to-Speech (TTS) API (`tts-1` model).
- Saves the audio output as an MP3 file in the `audio_output/` directory.
- Accepts input either interactively or as a command-line argument.
- Uses structured JSON output from the translation model for robustness.
- Uses a `Makefile` for easy setup and execution.

## Prerequisites

- Python 3.7.1 or newer
- An OpenAI API key

## Setup

1.  **Clone the repository (if applicable):**

    ```bash
    git clone <repository-url>
    cd korean-language-learner
    ```

2.  **Create a `.env` file:**
    Create a file named `.env` in the project root directory and add your OpenAI API key:

    ```
    OPENAI_API_KEY='your_openai_api_key_here'
    ```

    _(This file is ignored by Git via `.gitignore`)_

3.  **Set up the environment and install dependencies:**
    It's recommended to use a virtual environment.

    ```bash
    make install
    ```

    This command will:

    - Create a Python virtual environment named `venv`.
    - Activate the environment (implicitly for the installation).
    - Install the required packages listed in `requirements.txt` (`openai`, `python-dotenv`).

    _Alternatively, you can set up the virtual environment and install packages manually:_

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    pip install -r requirements.txt
    ```

## Usage

Make sure your virtual environment is active (`source venv/bin/activate` or use the `make` commands).

- **Interactive Mode (using Makefile):**

  ```bash
  make run
  ```

  The script will prompt you to enter an English phrase.

- **With a Phrase Argument (using Makefile):**

  ```bash
  make runp phrase="I want to learn Korean"
  ```

  Replace "I want to learn Korean" with your desired phrase.

- **Directly with Python (Interactive):**

  ```bash
  python hangul.py
  ```

- **Directly with Python (Phrase Argument):**
  ```bash
  python hangul.py "Where is the library?"
  ```

## Output

The script will print the Korean translation to the console and save the corresponding audio file (e.g., `i_want_to_learn_korean.mp3`) in the `audio_output/` directory.

## Cleaning Up

To remove the virtual environment, audio output directory, and compiled Python files:

```bash
make clean
```
