import json
import logging
import os
# Import WebClient from Python SDK (github.com/slackapi/python-slack-sdk)
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# WebClient instantiates a client that can call API methods
# When using Bolt, you can use either `app.client` or the `client` passed to listeners.
client = WebClient(token=os.environ.get("SLACK_BOT_TOKEN"))
logger = logging.getLogger(__name__)

raw_data = '''{
  "schemaId": "azureMonitorCommonAlertSchema",
  "data": {
    "essentials": {
      "alertId": "/subscriptions/<subscription ID>/providers/Microsoft.AlertsManagement/alerts/b9569717-bc32-442f-add5-83a997729330",
      "alertRule": "WCUS-R2-Gen2",
      "severity": "Sev3",
      "signalType": "Metric",
      "monitorCondition": "Resolved",
      "monitoringService": "Platform",
      "alertTargetIDs": [
        "/subscriptions/<subscription ID>/resourcegroups/pipelinealertrg/providers/microsoft.compute/virtualmachines/wcus-r2-gen2"
      ],
      "configurationItems": [
        "wcus-r2-gen2"
      ],
      "originAlertId": "3f2d4487-b0fc-4125-8bd5-7ad17384221e_PipeLineAlertRG_microsoft.insights_metricAlerts_WCUS-R2-Gen2_-117781227",
      "firedDateTime": "2019-03-22T13:58:24.3713213Z",
      "resolvedDateTime": "2019-03-22T14:03:16.2246313Z",
      "description": "",
      "essentialsVersion": "1.0",
      "alertContextVersion": "1.0"
    },
    "alertContext": {
      "properties": null,
      "conditionType": "SingleResourceMultipleMetricCriteria",
      "condition": {
        "windowSize": "PT5M",
        "allOf": [
          {
            "metricName": "Percentage CPU",
            "metricNamespace": "Microsoft.Compute/virtualMachines",
            "operator": "GreaterThan",
            "threshold": "25",
            "timeAggregation": "Average",
            "dimensions": [
              {
                "name": "ResourceId",
                "value": "3efad9dc-3d50-4eac-9c87-8b3fd6f97e4e"
              }
            ],
            "metricValue": 7.727
          }
        ]
      }
    },
    "customProperties": {
      "Key1": "Value1",
      "Key2": "Value2"
    }
  }
}'''



json_data = json.loads(raw_data)
essentals = json_data['data']['essentials']
alertId = essentals['alertId']
alertRule = essentals['alertRule']
severity = essentals['severity']
signalType = essentals['signalType']
monitorCondition = essentals['monitorCondition']

print(json_data['data']['essentials']) 

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
    formatted_text = f"```{json.dumps(alertId, indent = 2)}```"
    result = client.chat_postMessage(
        channel=channel_id, 
        attachments=payload
    )
    logger.info(result)

except SlackApiError as e:
    logger.error(f"Error posting message: {e}")


