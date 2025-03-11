from flask import Flask, render_template, url_for, jsonify, request
from story_generator import generate_sentence, generate_story
from pypinyin import pinyin, Style
import jieba
import translators as ts
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///translations.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

punctuation_chars = set("，。！？；：,.!?;:")

class WordCache(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    word = db.Column(db.String(100), unique = True, nullable = False)
    pinyin = db.Column(db.String(200))
    translation = db.Column(db.String(500))

    def __repr__(self):
        return f'WordCache {self.word}'
    

def get_pinyin_translation(word):
    cached = WordCache.query.filter_by(word=word).first()
    if cached:
        return cached.pinyin, cached.translation
    else:
        # If not cached, compute
        # pinyin
        pinyin_list = pinyin(word, style=Style.TONE)
        pinyin_str = ' '.join(item[0] for item in pinyin_list)
        # translation
        translation_str = ts.translate_text(
            query_text=word,
            translator='alibaba',
            from_language='zh-CHS',
            to_language='en'
        ).lower()  # note the parentheses for .lower()

        # Store in DB
        new_entry = WordCache(word=word, pinyin=pinyin_str, translation=translation_str)
        db.session.add(new_entry)
        db.session.commit()

        return pinyin_str, translation_str

@app.route('/')
def index():

    sentence = "中国故事生成器"

    segments = list(jieba.cut(sentence))

    html_segments = []

    for seg in segments:
        if seg in punctuation_chars:
            html_segments.append(seg)
        else:

            #pinyin, translation = get_pinyin_translation(seg)


            html_segments.append(
                f'<span class="word" data-word="{seg}">{seg}</span>'
            )

    final_html = ''.join(html_segments)

    #full_story = generate_story()

    full_story = "" #for testing

    segments_story = list(jieba.cut(full_story))

    html_segments_story = []

    for seg in segments_story:
        if seg in punctuation_chars:
            html_segments_story.append(seg)
        else:

            #pinyin, translation = get_pinyin_translation(seg)


            html_segments_story.append(
                f'<span class="word" data-word="{seg}">{seg}</span>'
            )

    final_html_story = ''.join(html_segments_story)


    return render_template('index.html', story = final_html, full_story_html = final_html_story)

@app.route('/generate')
def generate():
    #new_sentence = generate_sentence()

    hsk_level = request.args.get('hsk_level', '1')
    new_story = generate_story(hsk_level = hsk_level)
    #new_story = "我喜欢喝水" #for testing

    

    #print("generating..." + hsk_level)

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
    data = request.get_json()
    words = data['words']
    result_map = {}
    for w in words:
        p, t = get_pinyin_translation(w)
        result_map[w] = {'pinyin': p, 'translation':t}
    return jsonify(result_map)

#@app.route('/lookup')
#def lookup():
#    word = request.args.get('word', '')
#
#    pinyin_list = pinyin(word, style = Style.TONE)
#    pinyin_str = ' '.join([item[0] for item in pinyin_list])
#
#
#
#    translation = ts.translate_text(query_text=word, translator = 'alibaba', from_language='zh-CHS', to_language='en').lower()
#
#
#    return jsonify({'pinyin': pinyin_str, 'translation': translation})


if __name__ == '__main__':

    with app.app_context():
        db.create_all()
    app.run(debug = True)