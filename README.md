
# やりたいこと
Alexaからlambdaを呼び出して中野区のゴミの曜日を返します。
全く触ったことのない人でも一から作れるように書きました。

![alexa.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/619762/479c5032-72bd-f550-e10d-bcc353a8af8c.png)


[ALEXAで開発入門してみたので自分なりに纏めてみる](https://qiita.com/godan09/items/6dafc3da51b10532dbe1)
こちらの記事を参考に作ってみました。
細かいところまで説明されていてとても勉強になりましたが、
AWSの仕様変更のためか途中でつまづいたのでその辺りも本稿で記載します。

# 必要なもの

* [Amazon開発者ポータル](https://developer.amazon.com/ja/)のアカウント取得 (Alexaのスキル作成に必要)
* [AWSマネジメントコンソール](https://aws.amazon.com/jp/console/)のアカウント取得 (lambda実装に必要)
* Amazon echo (なくても大丈夫)

# Alexa Skill Kit

echoから受け取った音声から**変数**を抽出し、
lambdaへ渡すためのスキルを作成します。

### スキルの作成

Amazon developerから`Alexa Skills Kit`を押下

![alexa-Page-3.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/619762/e7b464aa-7616-1259-2607-8680ca762da5.png)


Amazon developer consoleより`スキルの作成`を押下

![alexa-Page-2.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/619762/1148d3a0-2120-f686-91ed-7430637442f2.png)

以下を入力して`スキルを作成`を押下

スキル名: `TrashDay`
デフォルトの言語: `日本語`
スキルに追加するモデルを選択: `カスタム`
スキルのバックエンドリソースをホスティングする方法を選択: 
`ユーザ定義のプロビジョニング` (今回は独自にlambdaにホスティングする)

![alexa-Page-4.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/619762/069b398c-6c2b-a92c-d9b3-73e68e5bd9c5.png)

### 呼び出し名

スキルを呼び出すための呼び出し名を入力

スキルの呼び出し名: `テルミーゴミー`

「アレクサ、テルミーゴミーを開いて」でスキルが起動する
![alexa2-Page-2.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/619762/9d582e2d-4973-8e0e-acde-22c9fac6110d.png)


### スロットタイプ

アクションを呼び出すときに発言に含まれる変数を予め用意する。

スロットタイプの横の`追加`を押下し新規作成。
![alexa2-Page-3.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/619762/abf5af19-4b17-2f91-225f-aba49f43febf.png)

スロットタイプ名を`type`にして`カスタムスロットタイプを作成`を押下
![alexa2-Page-4.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/619762/77524b56-1962-6d33-07cf-8200976eb9c4.png)

以下のスロット値を追加。
なお、アレクサという値は必須ではない（ちょっとした遊び心※後述）
![alexa2-Page-1.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/619762/33c166ef-3417-4842-0547-0792e8db243d.png)


### インテント

呼び出されたスキル(=テルミーゴミー)が実行するアクションを定義する。
今回は、ゴミの曜日を応えるアクションのみ作成する。

インテントの横の`追加`を押下し新規作成。
![alexa2-Page-5.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/619762/1456f847-54ca-29cc-4278-f70cbcb1e52e.png)

インテント名を`TellTrashDay`として`カスタムインテントを作成`を押下
![alexa2-Page-6.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/619762/4b649542-72e4-2d6b-c0c0-bc48d3792cbf.png)

インテントスロット名を`type`とし、先程作成したスロットタイプ`type`を選択
![alexa2-Page-7.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/619762/00c6fb38-4d66-4a58-30b5-d46cd3b71883.png)

サンプル発話に下記を追加。
なお、{type}の後ろには**半角スペース**がいるので注意。
![alexa2-Page-8.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/619762/9dc05755-f0b2-4472-4bab-ffcf26330b43.png)

以上により、サンプル発話にある発言をしたときに{type}部分が変数として抽出されます。

### 

# AWS lambda

Alexaから渡された変数をもとに応答を選択してレスポンスする関数をホスティングします。

### 関数の作成

AWSマネジメントコンソールからlambdaの画面へ遷移し、`関数の作成`を押下
![alexa2-Page-9.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/619762/f0ede319-ff09-1383-45b4-1b27ac169675.png)

AWSで提供される`alexa-skills-kit-color-expert-python`を選択
Alexaが好きな色を聞いてくるサンプルアプリケーションが組み込まれています。
![alexa2-Page-10.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/619762/868cc4aa-9734-579c-de8b-ea06568962f5.png)

アプリケーション名とTopicNameParameterを`TrashDay`にして`デプロイ`を押下
TopicNameParameterはCloudFormationで渡されるパラメーターに格納されますが、
特に関数内で使用されている形跡はないので任意の値で大丈夫です。
![alexa2-Page-11.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/619762/e6d765ec-efc2-d947-ac7e-ec2ddd790506.png)

### TrashDay.pyをデプロイ

左メニューから関数を選択し先程のアプリケーション名が記載さている関数を押下
![alexa2-Page-12.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/619762/5cb4fa21-10bf-7de5-f860-e654c2fcea8e.png)

ラムダ関数を選択して、下画面のエディタを[TrashDay.py](https://github.com/sasaku-panda/alexa_TrashDay.git)の内容に置換
![alexa2-Page-13.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/619762/b47bc992-715c-bb83-3b66-6176b08f6a80.png)

```python:TrashDay.py
# coding:utf-8
"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6

For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""

from __future__ import print_function


# --------------- Helpers that build all of the responses ----------------------

### 各インテントを処理し終わった後にAlexaに戻すために使う関数
def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }

### build_speechlet_responseで作ったJSONを更に返答用のJSONに格納して返す関数
def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "やぁ、こんにちは、テルミーゴミーだよ、 " \
                    "捨てたいゴミの指定曜日を応えるよ！ " 
    
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "捨てたいゴミの指定曜日を応えるよ！ " 

    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "またきてね " 

    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()

### 発言に対応するインテントを判定し各関数に分岐する関数
def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers

    ### TellTrashDayを含む各インテントに分岐
    if intent_name == "TellTrashDay":
        return set_TellTrashDay_text(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------
### lambdaが呼ばれた時に一番最初に実行される関数
### eventにはlambdaへのリクエスト情報が格納される
def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    # get applicationId from request.json
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])
    ### スキル名のみの呼び出しで、インテントが含まれていないとき実行される
    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    ### ユーザがインテントに対応する発言をしたとき実行される
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    ### 終了時、応答可能なインテントがないとき、エラー時に実行される
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])


### スロットタイプに一致するゴミの曜日を返す関数
def set_TellTrashDay_text(intent, session):
    """ Sets the color in the session and prepares the speech to reply to the
    user.
    """

    card_title = intent['name']
    session_attributes = {}
    should_end_session = False
    speech_output = "早く言えよ、お前をクズカゴに捨てたっていいんだぞ"

    ### 燃えるゴミリスト
    burn_list = ['燃える', '生', '紙くずの']
    ### 燃えないゴミリスト
    notburn_list = ['燃えない', 'プラスチックの', 'プラの', 'プラ']
    ### アルミ缶系ゴミリスト
    can_list = ['アルミ缶の', 'アルミ缶', '空き缶の', 'ペットボトルの', 'ビンの', '缶の', '缶', 'スチール缶の']
    ### ダンボールゴミリスト
    paper_list = ['ダンボールの', '新聞紙の', '古紙の', '紙の', '紙']
    ### 危険物系ゴミリスト
    glass_list = ['ガラスの', '金属の', '陶器の']
    ### 言ったらやばいやつ
    alexa_list = ['アレクサの', 'アレクサ']

    if 'type' in intent['slots']:
        ### 3rd part was 'name' so changed to 'value'
        trash_type = intent['slots']['type']['value'] 

        if trash_type in burn_list:
            speech_output = '火曜日と金曜日です'
        elif trash_type in notburn_list:
            speech_output = '月曜日です'
        elif trash_type in can_list:
            speech_output = '水曜日です'
        elif trash_type in paper_list:
            speech_output = '月曜日です'
        elif trash_type in glass_list:
            speech_output = '土曜日です'
        elif trash_type in alexa_list:
            speech_output = '宇宙ゴミになりたいようだな'
    else:
        speech_output = "すみません、ちょっと何言ってるか分からないです"

    print(speech_output)
    reprompt_text = speech_output
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

```

### トリガーとなるAlexa Skills Kitを指定

`トリガーを追加`を押下
![alexa2-Page-14.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/619762/1c560531-c609-f7c5-6450-1242d5f24056.png)

一旦、Alexa developer consoleに戻り、エンドポイントからスキルIDをコピー
![alexa2-Page-16.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/619762/4f0d5f06-c4b2-5964-3158-027ce18fca6e.png)

AWSに戻り、`Alexa Skills Kit`を選択してコピーしたスキルIDをペーストし`追加`を押下
![alexa2-Page-15.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/619762/563e1633-3801-7ee4-eda4-ae4e0d122497.png)

正常に追加されたらlambda側の設定は完了です。あと一息。

# エンドポイントにlambdaを指定

最後に、先程作成したlambda関数をAlexa側で指定します。

AWSのlambdaの画面上部にあるARNをコピー
![alexa2-Page-18.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/619762/ba4dc120-e9b4-ee2b-a383-7b1fdabc833b.png)

Alexaのエンドポイントのデフォルトの地域にペースト
![alexa2-Page-17.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/619762/c6fd0f72-94e1-16c6-f7af-6ae5c219ce22.png)

`エンドポイントの保存`を押下
![alexa2-Page-18.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/619762/a6b7deea-3062-0455-f57e-f1f889245cc9.png)

以上で全ての設定が完了したので、`モデルを保存`して`モデルをビルド`します。
![alexa2-Page-19.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/619762/a2fc39e2-69e4-c3d6-c485-7250fc526b93.png)

# テスト

alexa developer consoleのテストで実際に動作するか確認します。

スキルテストが有効になっているステージを`開発中`に変更
![alexa2-Page-20.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/619762/0d904d9e-c951-5f26-254e-d19c1e762c96.png)

スキルを起動して、インテントに追加したアクションを試します。
![alexa2-Page-21.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/619762/be32185b-161f-f7ce-2981-243d1e9b1065.png)

動きました！！

ユーモアもバッチリです。
![alexa2-Page-22.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/619762/eaac979c-efb0-92ac-b5b4-98471e1fab76.png)

ちなみに、スキルをストアで公開しなくても、
自分のechoでなら何も設定しなくてもスキルを使えました。
(ブラウザ上でテストしていたら、うちのechoが反応してびっくりしました笑）
Amazonアカウントで自動的に連携されているみたいですね。

# トラブルシューティング

### lambda関数内に日本語があるとエンコードエラー

コードの先頭に`# coding:utf-8`を付加し、日本語を読み込めるようにしています。

### うまく動作しないときは
Alexaのテスト画面にJSON入力が表示されるのでlambdaのテストにコピーして試してみることで、Alexaとlambdaのどっちに原因があるのか切り分けることができます。





