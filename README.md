# ReadAssistance
A tool for users studying chinese that helps develop reading skills and help reinforce vocabulary

## Features

- **Story Generation:** Integrated OpenAI API to generate short stories in simplified Chinese according to users HSK level
- **Interactive Elements:** Clickable words, can display pinyin and translation
- **Translation Function:** Translate single words and full-story


## Technologies Used

- **Backend:** Python, Flask
- **Frontend:** HTML (Jinja templates), JavaScript, and CSS
- **Database:** Flask-SQLAlchemy
- **Translation & Text Processing:** 
  - `pypinyin` for converting Chinese characters to pinyin  
  - `jieba` for Chinese word segmentation  
  - `translators` for performing translations
- **Environment Variables:** `python-dotenv`
- **Additional APIs:** `openai` for AI-driven features

## Installation & Setup

1. **Clone the Repository:**

```bash
   git clone https://github.com/clemens-steinwendner/ReadAssistance
   cd ReadAssistance
   ```

2. **Install dependencies:**
    It is also recommended to set up a virtual environment.

    Make sure you have the requirements.txt file in your folder to install all necessary dependencies

```bash
    pip install -r requirements.txt
```
3. **Set Up Environment Variables:**

    Insert your openAI-API-key in order to use generation
```env
    OPENAI_API_KEY=your_openai_api_key_here
```
4. **Run the application:**

```bash
    python app.py
```

## Usage

- **Home Page:** On loading, you’ll see the interactive story with options.
- **HSK Level Selection:** Choose the desired HSK level from the dropdown menu.
- **Generate Story:** Click on the “Generate New Story” button to generate a fresh story or “Generate Second Part” to continue.
- **Interactive Translations:** Click any highlighted Chinese word to see its pinyin and English translation.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.



