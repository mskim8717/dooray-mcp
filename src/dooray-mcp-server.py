from mcp.server.fastmcp import FastMCP
import requests
import json
from datetime import datetime, timezone, timedelta
from typing import Optional, Dict, Any
from pydantic import Field
from dotenv import load_dotenv
import os

load_dotenv()

# Create MCP server
mcp = FastMCP("dooray-calendar")


@mcp.tool()
def get_schedule(start_date: Optional[str] = Field(description="The start date of the schedule"), 
                 start_time: Optional[str] = Field(description="The start time of the schedule"),
                 end_date: Optional[str] = Field(description="The end date of the schedule"),
                 end_time: Optional[str] = Field(description="The end time of the schedule"),
                 start_iso_format: Optional[str] = Field(description="The start date time of the schedule in ISO 8601 format"),
                 end_iso_format: Optional[str] = Field(description="The end date time of the schedule in ISO 8601 format")) -> str:
    """
    Target: dooray API를 호출하여 두레이 일정을 조회합니다.

    Args:
        start_date          : 시작 날짜 (예: '2025-04-04'), 입력하지 않으면 오늘 날짜로 해줘
        start_time          : 시작 시간 (예: '14:00'), 입력하지 않으면 현재 시간으로 해줘
        end_date            : 종료 날짜 (예: '2025-04-05'), 입력하지 않으면 오늘 날짜로 해줘
        end_time            : 종료 시간 (예: '15:00'), 입력하지 않으면 현재 시간으로 해줘
        start_iso_format    : ISO 8601 형식으로 변환된 날짜/시간 문자열(예: '2025-04-04T14:00:00+09:00')
        end_iso_format      : ISO 8601 형식으로 변환된 날짜/시간 문자열(예: '2025-04-04T14:00:00+09:00')

    Returns:
        str: 일정 조회 결과 메시지
    """

    # 현재 날짜/시간 가져오기
    if not start_date:
        start_date = datetime.now().strftime("%Y-%m-%d")

    if not start_time:
        start_time = datetime.now().strftime("%H:%M")

    if not end_date:
        start_date = datetime.now().strftime("%Y-%m-%d")

    if not end_time:
        end_time = (datetime.now() + timedelta(hours=1)).strftime("%H:%M")

    # date와 time을 결합하여 datetime 객체로 변환
    datetime_start_str = f"{start_date} {start_time}"
    start_dt = datetime.strptime(datetime_start_str, "%Y-%m-%d %H:%M")

    datetime_end_str = f"{end_date} {end_time}"
    end_dt = datetime.strptime(datetime_end_str, "%Y-%m-%d %H:%M")

    # ISO 8601 형식으로 변환 (Timezone 설정 포함)
    start_iso_format = start_dt.replace(tzinfo=timezone(timedelta(hours=9))).isoformat()
    end_iso_format = end_dt.replace(tzinfo=timezone(timedelta(hours=9))).isoformat()

    calendar_id = os.getenv('DOORAY_CALENDAR_ID')

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f"dooray-api {os.getenv('DOORAY_API_KEY')}"
    }
    url = f"https://api.gov-dooray.com/calendar/v1/calendars/*/events?calendars={calendar_id}&category=general&timeMin={start_iso_format}&timeMax={end_iso_format}"
    response = requests.get(url, headers=headers, verify=False)

    if response.status_code == 200:
        return f"{response.text}"
    else:
        return f"일정 조회 중 오류가 발생했습니다: {response.text}"


@mcp.tool()
def add_schedule(title: str = Field(description="The title of the schedule", default="새 일정"), 
                 start_date: Optional[str] = Field(description="The start date of the schedule"), 
                 start_time: Optional[str] = Field(description="The start time of the schedule"),
                 end_date: Optional[str] = Field(description="The end date of the schedule"),
                 end_time: Optional[str] = Field(description="The end time of the schedule"),
                 start_iso_format: Optional[str] = Field(description="The start date time of the schedule in ISO 8601 format"),
                 end_iso_format: Optional[str] = Field(description="The end date time of the schedule in ISO 8601 format"),
                 location: Optional[str] = Field(description="The location of the schedule"),
                 description: Optional[str] = None) -> str:
    """
    Target: dooray API를 호출하여 두레이 일정을 추가합니다.

    Args:
        title               : 일정 제목
        start_date          : 시작 날짜 (예: '2025-04-04'), 입력하지 않으면 오늘 날짜로 해줘
        start_time          : 시작 시간 (예: '14:00'), 입력하지 않으면 현재 시간으로 해줘
        end_date            : 종료 날짜 (예: '2025-04-05'), 입력하지 않으면 오늘 날짜로 해줘
        end_time            : 종료 시간 (예: '15:00'), 입력하지 않으면 현재 시간으로 해줘
        start_iso_format    : ISO 8601 형식으로 변환된 날짜/시간 문자열(예: '2025-04-04T14:00:00+09:00')
        end_iso_format      : ISO 8601 형식으로 변환된 날짜/시간 문자열(예: '2025-04-04T14:00:00+09:00')
        location            : 일정 장소 (선택사항)
        description         : 일정 설명 (선택사항)

    Returns:
        str: 일정 추가 결과 메시지
    """
    # 현재 날짜/시간 가져오기
    if not start_date:
        start_date = datetime.now().strftime("%Y-%m-%d")

    if not start_time:
        start_time = datetime.now().strftime("%H:%M")

    if not end_date:
        start_date = datetime.now().strftime("%Y-%m-%d")

    if not end_time:
        end_time = (datetime.now() + timedelta(hours=1)).strftime("%H:%M")
    
    if not location:
        location = ""

    if not description:
        description = ""

    # date와 time을 결합하여 datetime 객체로 변환
    datetime_start_str = f"{start_date} {start_time}"
    start_dt = datetime.strptime(datetime_start_str, "%Y-%m-%d %H:%M")

    datetime_end_str = f"{end_date} {end_time}"
    end_dt = datetime.strptime(datetime_end_str, "%Y-%m-%d %H:%M")

    # ISO 8601 형식으로 변환 (Timezone 설정 포함)
    start_iso_format = start_dt.replace(tzinfo=timezone(timedelta(hours=9))).isoformat()
    end_iso_format = end_dt.replace(tzinfo=timezone(timedelta(hours=9))).isoformat()

    # API 요청 데이터 준비
    schedule_data = {
        "title": title,
        "start_date": start_date,
        "start_time": start_time,
        "end_date": end_date,
        "end_time": end_time,
        "start_iso_format": start_iso_format,
        "end_iso_format": end_iso_format,
        "location": location or "",
        "description": description or ""
    }
    print(f"schedule_data: {schedule_data}")
    
    # 여기서 실제 외부 Dooray API 호출 코드를 구현합니다
    try:
        """
        POST /calendar/v1/calendars/{calendar-id}/events
        일정을 등록
        """
        member_id = os.getenv('DOORAY_MEMBER_ID') 
        calendar_id = os.getenv('DOORAY_CALENDAR_ID')

        body = {
            "users": {
                "to": [{
                    "type": "member",
                    "member": {
                        "organizationMemberId": member_id
                    }
                }],
                "cc": [{
                    "type": "member",
                    "member": {
                        "organizationMemberId": member_id
                    }
                }]
            },
            "subject": title,
            "body": {
                "mimeType": "text/html",
                "content": description,
            },
            "startedAt": start_iso_format,
            "endedAt": end_iso_format,
            "wholeDayFlag": "false",                  #/* 종일 일정인 경우 true */
            "location": location,
            "personalSettings": {
                "alarms": [{
                    "action": "app",               #/* mail app */
                    "trigger": "TRIGGER:-PT10M"     #/* rfc2445, duration, trigger */
                }],
                "busy": "true",                       #/* true: 바쁨, false: 한가함 표시 */
                "class": "public"                   #/* pubilc: 공개, private: 비공개 */
            }
        }

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"dooray-api {os.getenv('DOORAY_API_KEY')}"
        }
        url = f"https://api.gov-dooray.com/calendar/v1/calendars/{calendar_id}/events"
        response = requests.post(url, headers=headers, data=json.dumps(body, ensure_ascii=False, indent="\t").encode('utf-8'), verify=False)

        if response.status_code == 200:
            return f"'{title}' 일정이 {start_date} {start_time}에 성공적으로 추가되었습니다."
        else:
            return f"일정 추가 중 오류가 발생했습니다: {response.text}"
            

    except Exception as e:
        return f"일정 추가 중 오류가 발생했습니다: {str(e)}"


if __name__ == "__main__":
    mcp.run()