# Dooray MCP Server

Dooray API를 활용한 일정 관리 MCP 서버입니다.

## 기능

- Dooray API를 통한 일정 추가
- 시작/종료 시간 자동 설정
- 위치 및 설명 정보 지원

## 설치 방법

1. 저장소 클론
```bash
git clone https://github.com/yourusername/dooray-mcp.git
cd dooray-mcp
```

2. 가상환경 생성 및 활성화
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# 또는
.\.venv\Scripts\activate  # Windows
```

3. 의존성 설치
```bash
pip install -e .
```

## 환경 변수 설정

`.env` 파일을 생성하고 다음 변수들을 설정하세요:

```
DOORAY_API_KEY=your_api_key
DOORAY_MEMBER_ID=your_member_id
DOORAY_CALENDAR_ID=your_calendar_id
```

## 사용 방법

서버 실행:
```bash
python dooray-mcp-server.py
```

## 라이선스

MIT License
