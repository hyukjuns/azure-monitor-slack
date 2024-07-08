# Azure Monitor Alert to Slack

## 사전 준비
1. VSCode
2. [Python Extension](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
3. [Azure Functions Extenstion](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-azurefunctions)
4. [Azurite Extension](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-azurefunctions)
5. [Azure Function Core Tools](https://learn.microsoft.com/en-us/azure/azure-functions/create-first-function-cli-python?tabs=linux%2Cbash%2Cazure-cli%2Cbrowser#install-the-azure-functions-core-tools)

## 저장소 사용 순서
1. Clone this repo

2. local.settings.json 파일 생성

    ```
    {
        "IsEncrypted": false,
        "Values": {
            "FUNCTIONS_WORKER_RUNTIME": "python",
            "AzureWebJobsFeatureFlags": "EnableWorkerIndexing",
            "AzureWebJobsStorage": "UseDevelopmentStorage=true",
            "SLACK_BOT_TOKEN": "",
            "SLACK_CHANNEL_ID": ""
        }
    }
    ```

3. Python 가상환경 세팅

    ```
    python -m venv .venv
    source .venv/bin/activate
    ```

4. Function 로컬 실행 or Azure 배포
    - 로컬 실행
        - ```F5```: 실행 단축키
        - ```F1```: Azure Function: Excute Function Now
    - Function App 생성
        - ```F1```: Azure Function: Create Function App in Azure (Advanced)
    - 배포
        - ```F1```: Azure Function: Deploy to Function App
    

## 초기 구성 절차
1. Function App 구성
    - Tier: Consumption Plan
    - LANG: Python 3.11.2
    - Trigger Type: HTTP Trigger
    - Environments Variables:
        - 로컬에서 개발할 경우 local.settings.json에 입력, Function App에 배포할 경우 Environments에 입력
        - ```SLACK_BOT_TOKEN```
            - Slack bot의 Auth Token
        - ```SLACK_CHANNEL_ID```
            - 알람을 받을 슬랙 채널 아이디
    - Function Auth Level: Funciton

2. Slack Bot 구성
    - Slack bot 생성
    - Slack API: [chat.postMessage](https://api.slack.com/methods/chat.postMessage)
    - Slack API Permission
        - Bot Token Scope: [chat:write](https://api.slack.com/scopes/chat:write)
    - 알림 받고자 하는 채널에 Bot 추가

3. Azure Monitor에서 Action Group 구성
    - Action -> Webhook -> Function Trigger URL 입력