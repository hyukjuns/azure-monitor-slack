import logging
import os
import azure.functions as func
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import make_slack_message


CHANNEL_ID = os.environ.get("SLACK_CHANNEL_ID")
client = WebClient(token=os.environ.get("SLACK_BOT_TOKEN"))

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.function_name(name="AzureMonitorTrigger")
@app.route(route="azure_monitor")
def azure_monitor_http_trigger(req: func.HttpRequest) -> func.HttpResponse:

    logging.info('Azure Monitor Alert Triggered')

    # 1) 수신된 경고 데이터 읽기
    try:
        request_body = req.get_json()
        logging.info(request_body)
    except Exception as e:
        logging.error(f'Error at Get Json: {e}')
        return func.HttpResponse(status_code=500)
    # 2) 저장한 데이터 파싱 & 슬랙 전송용도 메시지 만들기
    else:
        payload = request_body['data']
        try:
            slack_message = make_slack_message.azure_monitor(payload)
        except Exception as e:
            logging.error(f'Error at Make Slack Message: {e}')
            return func.HttpResponse(status_code=500)
        # 3) 슬랙으로 메시지 전송 
        try:
            result = client.chat_postMessage(
                channel=CHANNEL_ID, 
                attachments=slack_message
            )
            logging.info(result)
            return func.HttpResponse(status_code=200)
        except SlackApiError as e:
            logging.error(f"Error at Sending Slack Message: {e}")
            return func.HttpResponse(status_code=500 )

# Processing Grafana Alert
@app.function_name(name="GrafanaTrigger")
@app.route(route="grafana")
def grafana_http_trigger(req: func.HttpRequest) -> func.HttpResponse:

    logging.info('Grafana Alert Triggered')

    try:
        request_body = req.get_json()
        logging.info(request_body)
    except Exception as e:
        logging.error(f'Get Json error occured: {e}')
        return func.HttpResponse(status_code=500)
    else:
        try:
            slack_message = make_slack_message.grafana(request_body)
        except Exception as e:
            logging.error(f'Error at Make Slack Message: {e}')
            return func.HttpResponse(status_code=500)
        try:
            result = client.chat_postMessage(
                channel=CHANNEL_ID, 
                attachments=slack_message
            )
            logging.info(result)
            return func.HttpResponse(status_code=200)
        except SlackApiError as e:
            logging.info(e)
            return func.HttpResponse(status_code=500)
