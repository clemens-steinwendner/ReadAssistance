from flask import Flask, render_template, url_for, jsonify, request
from story_generator import generate_sentence, generate_story
from pypinyin import pinyin, Style
import jieba
import translators as ts

app = Flask(__name__)


@app.route('/')
def index():

    sentence = "我喜欢喝水"

    segments = list(jieba.cut(sentence))

    html_segments = []

    for seg in segments:
        if seg.strip():
            html_segments.append(
                f'<span class="word" data-word="{seg}">{seg}</span>'
            )

    final_html = ''.join(html_segments)

    #full_story = generate_story()

    full_story = "我喜欢喝水" #for testing

    segments_story = list(jieba.cut(full_story))

    html_segments_story = []

    for seg in segments_story:
        if seg.strip():
            html_segments_story.append(
                f'<span class="word" data-word="{seg}">{seg}</span>'
            )

    final_html_story = ''.join(html_segments_story)


    return render_template('index.html', story = final_html, full_story_html = final_html_story)

@app.route('/generate')
def generate():
    #new_sentence = generate_sentence()
    #new_story = generate_story()
    new_story = "我喜欢喝水" #for testing

    segments = list(jieba.cut(new_story))

    html_segments = [] 

    for seg in segments:
        if seg.strip():
            html_segments.append(
                f'<span class="word" data-word="{seg}">{seg}</span>'
            )

    final_html = ''.join(html_segments)

    return jsonify({'sentence': final_html})

@app.route('/lookup')
def lookup():
    word = request.args.get('word', '')

    pinyin_list = pinyin(word, style = Style.TONE)
    pinyin_str = ' '.join([item[0] for item in pinyin_list])



    translation = ts.translate_text(query_text=word, translator = 'alibaba', from_language='zh-CHS', to_language='en').lower


    return jsonify({'pinyin': pinyin_str, 'translation': translation})



if __name__ == '__main__':
    app.run(debug = True)