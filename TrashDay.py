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
