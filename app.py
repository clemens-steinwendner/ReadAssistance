from flask import Flask, render_template, url_for, jsonify, request
from story_generator import generate_sentence
from pypinyin import pinyin, Style
import jieba

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

    full_story = "一天，小白去河边。河里有一条大鱼。小白看鱼，很高兴"

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
    new_sentence = "我喜欢"

    segments = list(jieba.cut(new_sentence))

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

    translation = "bruvver"

    return jsonify({'pinyin': pinyin_str, 'translation': translation})



if __name__ == '__main__':
    app.run(debug = True)