from flask import Flask, render_template, url_for, jsonify, request
from story_generator import generate_sentence, generate_story, generate_second_part
from pypinyin import pinyin, Style
import jieba
import translators as ts
from flask_sqlalchemy import SQLAlchemy
import re

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///translations.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

punctuation_chars = set("，。！？；：,.!?;:")

current_story = ""


#The database for caching pinyin and translation of words (in case they are reused)
class WordCache(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    word = db.Column(db.String(30), unique = True, nullable = False)
    pinyin = db.Column(db.String(100))
    translation = db.Column(db.String(50))

    def __repr__(self):
        return f'WordCache {self.word}'
    

# Method for putting an entry into the database and returning pinyin and translation of the input
def get_pinyin_translation(word):
    cached = WordCache.query.filter_by(word=word).first()

    # in case the word was already tranlsated earlier in the session
    if cached:
        return cached.pinyin, cached.translation
    else:
        
        pinyin_list = pinyin(word, style=Style.TONE)
        pinyin_str = ' '.join(item[0] for item in pinyin_list)
        
        translation_str = ts.translate_text(
            query_text=word,
            translator='alibaba',
            from_language='zh-CHS',
            to_language='en'
        ).lower()  

        
        new_entry = WordCache(word=word, pinyin=pinyin_str, translation=translation_str)
        db.session.add(new_entry)
        db.session.commit()

        return pinyin_str, translation_str

@app.route('/')
def index():

    #title
    sentence = "中国故事生成器"

    segments = list(jieba.cut(sentence))

    html_segments = []

    for seg in segments:
        if seg in punctuation_chars:
            html_segments.append(seg)
        else:

            #we only write the words in the beginning (without the underlying pinyin and translation)
            #those are done in the background as they take a lot of time
            html_segments.append(
                f'<span class="word" data-word="{seg}">{seg}</span>'
            )

    final_html = ''.join(html_segments)

    return render_template('index.html', story = final_html)

@app.route('/generate')
def generate():

    global current_story

    hsk_level = request.args.get('hsk_level', '1')
    new_story = generate_story(hsk_level = hsk_level)

    #save the current story 
    current_story = new_story

    #split word for word using jieba
    segments = list(jieba.cut(new_story))

    html_segments = [] 


    #every element is a single html element
    for seg in segments:
        if seg in punctuation_chars:
            html_segments.append(seg)
        else:

            html_segments.append(
                f'<span class="word" data-word="{seg}">{seg}</span>'
            )

    final_html = ''.join(html_segments)

    return jsonify({'sentence': final_html})

@app.route('/generate_second')
def generate_second():
    #here we use the current_story we saved in order to generate a second part
    global current_story

    if(current_story == ""): return generate()

    hsk_level = request.args.get('hsk_level', '1')

    new_story = generate_second_part(current_story, hsk_level)

    current_story = new_story

    segments = list(jieba.cut(new_story))

    html_segments = [] 

    for seg in segments:
        if seg in punctuation_chars:
            html_segments.append(seg)
        else:

            html_segments.append(
                f'<span class="word" data-word="{seg}">{seg}</span>'
            )

    final_html = ''.join(html_segments)

    return jsonify({'sentence': final_html})


@app.route('/translate_all', methods=['POST'])
def translate_all():
    #we take every word and translate it
    data = request.get_json()
    words = data['words']
    result_map = {}
    for w in words:
        p, t = get_pinyin_translation(w)
        result_map[w] = {'pinyin': p, 'translation':t}
    return jsonify(result_map)

@app.route('/translate_story')
def translate_story():
    #we translate the full story in the lower div
    text = current_story

    print(text)

    translation_str = ts.translate_text(
        query_text=text,
        translator='alibaba',
        from_language='zh-CHS',
        to_language='en'
    )
    sentences = re.findall(r'[^.!?]+[.!?]', translation_str)

    # Trim whitespace around each sentence
    sentences = [s.strip() for s in sentences]

    return jsonify({'sentences': sentences})
    



if __name__ == '__main__':

    with app.app_context():
        db.create_all()
    app.run(debug = True)