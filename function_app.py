import azure.functions as func
import logging
import os
import json
# Import WebClient from Python SDK (github.com/slackapi/python-slack-sdk)
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

client = WebClient(token=os.environ.get("SLACK_BOT_TOKEN"))
logger = logging.getLogger(__name__)

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="http_trigger")
def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Azure Monitor Alert Triggered')

    # 1) 수신된 경고 데이터 읽기
    try:
        request_body = req.get_json()
        logging.info(request_body)
    except Exception as e:
        logging.info(f'Get Json error occured: {e}')
        return func.HttpResponse(
             status_code=500
        )

    # 2) 저장한 데이터 파싱 & 슬랙 전송용도 메시지 만들기
    else:
        payload = request_body['data']
        slack_message = make_slack_meesage(payload)

        # 4) 슬랙으로 메시지 전송 

        # ID of the channel you want to send the message to
        channel_id = "C078LKHB99C"
        try:
            logging.info(slack_message)
            # Call the chat.postMessage method using the WebClient
            result = client.chat_postMessage(
                channel=channel_id, 
                attachments=slack_message
            )
            logger.info(result)
            return func.HttpResponse(
             status_code=200
            )
        except SlackApiError as e:
            logger.error(f"Error posting slack message: {e}")
            return func.HttpResponse(
                status_code=500
            )

def make_slack_meesage(payload):
    essentals = payload['essentials']
    alertContext = payload['alertContext']
    # 공통 데이터
    alertId = essentals['alertId']
    alertRule = essentals['alertRule']
    severity = essentals['severity']
    signalType = essentals['signalType']
    monitorCondition = essentals['monitorCondition']
    message = '''
    [{
    "color": "#E01E5A",
    "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "Azure Monitor Alert %s",
                    "emoji": true
                }
            },
            {
                "type": "rich_text",
                "elements": [
                    {
                        "type": "rich_text_section",
                        "elements": [
                            {
                                "type": "text",
                                "text": "Alert Info\n"
                            }
                        ]
                    },
                    {
                        "type": "rich_text_list",
                        "style": "bullet",
                        "elements": [
                            {
                                "type": "rich_text_section",
                                "elements": [
                    {
                                        "type": "text",
                                        "text": "Alert Id: "
                                    },
                                    {
                                        "type": "link",
                    "url": "https://slack.com/",
                                        "text": "%s",
                    "style": {
                                            "bold": true
                                        }
                                    }
                                ]
                            },
                            {
                                "type": "rich_text_section",
                                "elements": [
                                    {
                                        "type": "text",
                                        "text": "Alert Rule: %s"
                                    }
                                ]
                            },
                            {
                                "type": "rich_text_section",
                                "elements": [
                                    {
                                        "type": "text",
                                        "text": "Severity: %s"
                                    }
                                ]
                            },
                            {
                                "type": "rich_text_section",
                                "elements": [
                                    {
                                        "type": "text",
                                        "text": "SignalType: %s"
                                    }
                                ]
                            },
                            {
                                "type": "rich_text_section",
                                "elements": [
                                    {
                                        "type": "text",
                                        "text": "MonitorCondition: %s"
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        ]
    }]''' % (alertRule, alertId, alertRule, severity, signalType, monitorCondition)

    # 경고 별로 경고 컨텍스트 분류
    # if essentals['monitoringService'] == "Log Alerts V2" and essentals['signalType'] == "Log": # 로그
       
    # elif essentals['monitoringService'] == "Platform" and essentals['signalType'] == "Metric": # 메트릭
        
    # elif essentals['monitoringService'] == "Resource Health" and essentals['signalType'] == "Activity Log": # 리소스 헬스
        
    # elif essentals['monitoringService'] == "ServiceHealth" and essentals['signalType'] == "Activity Log": # 서비스 이슈
        
    return message