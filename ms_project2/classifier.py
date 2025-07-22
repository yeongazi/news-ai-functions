from openai import AzureOpenAI
import os
import json

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    api_version="2024-02-01-preview",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)

def classify_and_extract_keywords(title, content):
    prompt = f"""
    아래 뉴스 기사 제목과 내용을 보고,
    다음 카테고리 중 하나로 분류하고 (IT, 정치, 경제, 생활),
    기사에서 주요 키워드 5개를 뽑아 JSON 형식으로 알려줘.

    제목: {title}
    내용: {content}

    응답 예시:
    {{
        "category": "경제",
        "keywords": ["주식시장", "금리", "환율", "기업 실적", "투자"]
    }}
    """
    try:
        response = client.chat.completions.create(
            model="gpt-35-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        # 응답이 JSON 형태가 아닐 수 있으니 안전하게 파싱
        raw = response.choices[0].message.content.strip()
        return json.loads(raw)
    except Exception as e:
        return {"category": "기타", "keywords": [f"오류: {e}"]}
