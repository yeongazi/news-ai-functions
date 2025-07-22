import logging
import json
import os
import azure.functions as func
from azure.storage.blob import BlobServiceClient

from news_api import get_news_api
from crawler import crawl_bbc, crawl_cnn, crawl_reuters
from summarizer import summarize_text
from classifier import classify_and_extract_keywords


def main(mytimer: func.TimerRequest) -> None:
    logging.info("뉴스 수집 및 분석 시작 (카테고리 + 키워드 포함)")

    # 1. 뉴스 수집 (총 50개)
    articles = []
    articles.extend(get_news_api(country="us", page_size=30))  # NewsAPI 30개
    articles.extend(crawl_bbc(limit=10))                       # BBC 10개
    articles.extend(crawl_cnn(limit=5))                        # CNN 5개
    articles.extend(crawl_reuters(limit=5))                    # Reuters 5개

    logging.info(f"총 {len(articles)}개 기사 수집 완료")

    # 2. 요약 + 카테고리 + 키워드 추출
    for article in articles:
        content = article.get("content", "")

        # 뉴스 요약
        try:
            summary = summarize_text(content)
            article["summary"] = summary
        except Exception as e:
            logging.error(f"요약 실패: {e}")
            article["summary"] = content[:200]  # 요약 실패 시 첫 200자만 저장

        # 카테고리 & 키워드 추출
        try:
            classification = classify_and_extract_keywords(
                article.get("title", ""),
                content
            )
            article["category"] = classification.get("category", "기타")
            article["keywords"] = classification.get("keywords", [])
        except Exception as e:
            logging.error(f"카테고리/키워드 추출 실패: {e}")
            article["category"] = "기타"
            article["keywords"] = []

    # 3. Blob Storage에 저장
    try:
        blob_service = BlobServiceClient.from_connection_string(
            os.getenv("AZURE_STORAGE_CONN")
        )
        container_client = blob_service.get_container_client("news-data")
        blob_client = container_client.get_blob_client("latest_news.json")
        json_data = json.dumps(articles, ensure_ascii=False, indent=2)
        blob_client.upload_blob(json_data, overwrite=True)
        logging.info("뉴스 데이터가 Blob에 저장되었습니다.")
    except Exception as e:
        logging.error(f"Blob 저장 실패: {e}")
