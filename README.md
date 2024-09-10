# Azure Monitor Alert to Slack

### 사전 준비
#### 1.  Azure 개발 환경 셋업
1. VSCode
2. [Python Extension](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
3. [Azure Functions Extenstion](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-azurefunctions)
4. [Azurite Extension](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-azurefunctions)
5. [Azure Function Core Tools](https://learn.microsoft.com/en-us/azure/azure-functions/create-first-function-cli-python?tabs=linux%2Cbash%2Cazure-cli%2Cbrowser#install-the-azure-functions-core-tools)

#### 2. 슬랙 봇 준비

- Slack bot 생성
- Slack API: [chat.postMessage](https://api.slack.com/methods/chat.postMessage)
- Slack API Permission
    - Bot Token Scope: [chat:write](https://api.slack.com/scopes/chat:write)
- 알림 받고자 하는 채널에 Bot 추가


### 주의사항
- Azure Monitor Alert 설정 시 Common Alert Schema 사용 필수 [공식문서](https://learn.microsoft.com/ko-kr/azure/azure-monitor/alerts/alerts-common-schema)

### 저장소 사용 순서
1. 저장소 다운로드

    ```
    git clone https://github.com/hyukjuns/azure-monitor-alert-function.git
    ```

2. 로컬 개발 환경에 `local.settings.json` 파일 생성

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

4. Function App 실행
    - 로컬 개발 환경 실행
        - ```F5```: 실행 단축키
        - ```F1```: Azure Function: Excute Function Now
    - Azure 클라우드 실행 (Function App 생성 및 배포)
        - ```F1```: Azure Function: Create Function App in Azure (Advanced)
        - ```F1```: Azure Function: Deploy to Function App
    

### 구성 참고 내용
1. Function App 스펙
    - Tier: Consumption Plan
    - LANG: Python 3.11.2
    - Trigger Type: HTTP Trigger
    - Environments Variables:
        - 로컬: local.settings.json
        - 클라우드 Function App: Environments
            - ```SLACK_BOT_TOKEN```: Slack bot의 Auth Token
            - ```SLACK_CHANNEL_ID```: 알람을 받을 슬랙 채널 아이디
    - Function Auth Level: Funciton

2. Azure Monitor에서 Action Group 구성 시
    - Action -> Webhook -> Function Trigger URL 입력
    - Azure Monitor Alert 설정 시 Common Alert Schema 사용 필수 [공식문서](https://learn.microsoft.com/ko-kr/azure/azure-monitor/alerts/alerts-common-schema)
### Release Note
> 2024.09 개선 내역
```
1. 디멘션 개행 출력 및 Key Value 파싱
2. 타임 포맷 변경
3. 알람 타겟 명시 (디멘션에 없을 경우에도 확인 가능)
4. 메시지 프리뷰 기능 추가 - 
Slack 메시지 카드 중 Attachment,Block 사용시 text 항목이 없기 때문에 fallback 항목 추가하여 프리뷰 기능 사용 가능 (프리뷰 기능은 기본적으로 슬랙 페이로드에 text 필드가 포함되어야 보임, Attachement, block 사용시 fallback 항목으로 대체 가능) 
5. 경고 발송용 Functon에 에러 감지 경고 별도 추가
6. 리소스 헬스 경고 발생/복구 시 탐지되도록
```