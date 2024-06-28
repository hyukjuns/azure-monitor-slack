import azure.functions as func
import logging
import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

CHANNEL_ID = os.environ.get("SLACK_CHANNEL_ID")
client = WebClient(token=os.environ.get("SLACK_BOT_TOKEN"))
logger = logging.getLogger(__name__)

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.route(route="http_trigger")
def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    logger.info('Azure Monitor Alert Triggered')

    # 1) 수신된 경고 데이터 읽기
    try:
        request_body = req.get_json()
        logger.info(request_body)
    except Exception as e:
        logger.error(f'Get Json error occured: {e}')
        return func.HttpResponse(
             status_code=500
        )

    # 2) 저장한 데이터 파싱 & 슬랙 전송용도 메시지 만들기
    else:
        payload = request_body['data']
        try:
            slack_message = make_slack_message(payload)
        except Exception as e:
            logger.error(f'Get Json error occured: {e}')
            return func.HttpResponse(
                status_code=500
            )
        # 3) 슬랙으로 메시지 전송 
        try:
            logger.info(slack_message)
            result = client.chat_postMessage(
                channel=CHANNEL_ID, 
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

def make_slack_message(payload):
    # 공통 데이터
    essentals = payload['essentials']
    alertRule = essentals['alertRule']
    severity = essentals['severity']
    signalType = essentals['signalType']
    monitorCondition = essentals['monitorCondition']
    # 경고 발생 / 해결에 맞게 메시지 카드 색상 선택
    if monitorCondition == "Fired":
        hex_color_code = "#d9534f" # red
    elif monitorCondition == "Resolved":
        hex_color_code = "#85d254" # green
    else:
        hex_color_code = "#ffe55d" # yellow
    monitoringService = essentals['monitoringService']
    firedDateTime = essentals['firedDateTime']

    # 경고 별로 경고 컨텍스트 분류
    alertContext = payload['alertContext']
    if monitoringService == "Log Alerts V2" and signalType == "Log": # 로그
        operator =  alertContext['condition']['allOf'][0]['operator']
        threshold = alertContext['condition']['allOf'][0]['threshold']
        metricValue = alertContext['condition']['allOf'][0]['metricValue']
        dimensions = alertContext['condition']['allOf'][0]['dimensions']
        details = f"- Operator: {operator} \n- Threshold: {threshold} \n- MetricValue: {metricValue} \n- Dimensions: {dimensions}"
    elif monitoringService == "Platform" and signalType == "Metric": # 메트릭
        metricName = alertContext['condition']['allOf'][0]['metricName']
        operator = alertContext['condition']['allOf'][0]['operator']
        threshold = alertContext['condition']['allOf'][0]['threshold']
        metricValue = alertContext['condition']['allOf'][0]['metricValue']
        dimensions = alertContext['condition']['allOf'][0]['dimensions']
        details = f"- MetricName: {metricName} \n-Operator: {operator} \n-Threshold: {threshold} \n-MetricValue: {metricValue} \n-Dimensions: {dimensions}"
    elif monitoringService == "Resource Health" and signalType == "Activity Log": # 리소스 헬스
        configurationItems = essentals['configurationItems']
        title = alertContext['properties']['title']
        type = alertContext['properties']['type']
        cause = alertContext['properties']['cause']
        currentHealthStatus = alertContext['properties']['currentHealthStatus']
        details = f"- configurationItems: {configurationItems} \n- Title: {title} \n- Type: {type} \n- Cause: {cause} \n- CurrentHealthStatus: {currentHealthStatus}"
    elif monitoringService == "ServiceHealth" and signalType == "Activity Log": # 서비스 이슈
        title = alertContext['properties']['title']
        service = alertContext['properties']['service']
        region = alertContext['properties']['region']
        incidentType = alertContext['properties']['incidentType']
        trackingId = alertContext['properties']['trackingId']
        impactStartTime = alertContext['properties']['impactStartTime']
        stage = alertContext['properties']['stage']
        status = alertContext['status']
        if stage == "Complete" or stage == "Resolved":
            hex_color_code = "#85d254"
            monitorCondition = stage
        details = f"- Title: {title} \n- Service: {service} \n- Region: {region} \n- IncidentType: {incidentType} \n- TrackingId: {trackingId}- ImpactStartTime: {impactStartTime} \n- Stage: {stage} \n- Status: {status}"
    
    message = '''
    [{
    "color": "%s",
    "blocks": [
            {
                "type": "rich_text",
                "elements": [
                    {
                        "type": "rich_text_section",
                        "elements": [
                            {
                                "type": "link",
                                "url": "https://portal.azure.com/#view/Microsoft_Azure_Monitoring/AzureMonitoringBrowseBlade/~/alertsV2",
                                "text": "%s: %s",
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
                                        "text": "Alert Rule: ",
                                        "style": {
                                            "bold": true
                                        }
                                    },
                                    {
                                        "type": "text",
                                        "text": "%s"
                                    }
                                ]
                            },
                            {
                                "type": "rich_text_section",
                                "elements": [
                                    {
                                        "type": "text",
                                        "text": "MonitorCondition: ",
                                        "style": {
                                            "bold": true
                                        }
                                    },
                                    {
                                        "type": "text",
                                        "text": "%s"
                                    }
                                ]
                            },
                            {
                                "type": "rich_text_section",
                                "elements": [
                                    {
                                        "type": "text",
                                        "text": "Triggered Time: ",
                                        "style": {
                                            "bold": true
                                        }
                                    },
                                    {
                                        "type": "text",
                                        "text": "%s"
                                    }
                                ]
                            },
                            {
                                "type": "rich_text_section",
                                "elements": [
                                    {
                                        "type": "text",
                                        "text": "Severity: ",
                                        "style": {
                                            "bold": true
                                        }
                                    },
                                    {
                                        "type": "text",
                                        "text": "%s"
                                    }
                                ]
                            },
                            {
                                "type": "rich_text_section",
                                "elements": [
                                    {
                                        "type": "text",
                                        "text": "Details: \n",
                                        "style": {
                                            "bold": true
                                        }
                                    },
                                    {
                                        "type": "text",
                                        "text": "%s"
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        ]
    }]''' % (hex_color_code, monitorCondition, alertRule, alertRule, monitorCondition, firedDateTime, severity, details)
    return message