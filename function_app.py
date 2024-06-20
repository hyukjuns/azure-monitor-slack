import azure.functions as func
import logging
import os
# Import WebClient from Python SDK (github.com/slackapi/python-slack-sdk)
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

client = WebClient(token=os.environ.get("SLACK_BOT_TOKEN"))
logger = logging.getLogger(__name__)

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="http_trigger")
def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    try:
        req_body = req.get_json()
        logging.info(req_body)
    except ValueError:
        pass
    else:
        essentals = req_body['data']['essentials']
        alertId = essentals['alertId']
        alertRule = essentals['alertRule']
        severity = essentals['severity']
        signalType = essentals['signalType']
        monitorCondition = essentals['monitorCondition']
        payload = '''
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

        # ID of the channel you want to send the message to
        channel_id = "C078LKHB99C"

        try:
            # Call the chat.postMessage method using the WebClient
            result = client.chat_postMessage(
                channel=channel_id, 
                attachments=payload
            )
            logger.info(result)

        except SlackApiError as e:
            logger.error(f"Error posting message: {e}")
        logging.info(essentals)
        return func.HttpResponse(
             status_code=200
        )