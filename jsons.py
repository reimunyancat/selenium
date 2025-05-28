import os
import json
import re
import random

MAX_LINES = 20  # 기본 최대 줄 수
MAX_LINES_PER_TOPIC = 20  # 주제당 최대 줄 수

def convert(max_lines=MAX_LINES, max_lines_per_topic=MAX_LINES_PER_TOPIC):
    """
    텍스트 파일을 JSONL 파인튜닝 데이터로 변환
    
    매개변수:
    - max_lines: 생성할 전체 대화 쌍의 최대 수
    - max_lines_per_topic: 각 주제(파일)당 최대 대화 쌍 수
    """
    if not os.path.exists('texts'):
        print("텍스트 파일이 있는 'texts' 폴더가 존재하지 않습니다.")
        return
    
    os.makedirs('data', exist_ok=True)
 
    text_files = [f for f in os.listdir('texts') if f.endswith('.txt')]
    
    if not text_files:
        print("'texts' 폴더에 텍스트 파일이 없습니다.")
        return

    output_file = 'data/fine.jsonl'
    
    data = []
      # 각 파일별 처리할 샘플 수를 계산
    samples_per_file = {}
    total_files = len(text_files)
    
    # 각 파일마다 균등하게 할당하되, 주제당 최대 제한 적용
    base_samples_per_file = min(max_lines_per_topic, max_lines // total_files) if total_files > 0 else 0
    
    for text_file in text_files:
        samples_per_file[text_file] = base_samples_per_file
    
    for text_file in text_files:
        topic = os.path.splitext(text_file)[0]  # 파일 이름에서 확장자 제거
        file_samples_count = 0  # 현재 파일에서 추가된 샘플 수
        
        try:
            with open(os.path.join('texts', text_file), 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 내용을 적절한 크기의 챙크로 나누기
            chunks = split_content_into_chunks(content)
            
            # 각 청크를 질문-답변 형식으로 변환
            for i, chunk in enumerate(chunks):
                # 이 파일에 대한 샘플 수가 제한에 도달하면 중단
                if file_samples_count >= samples_per_file[text_file]:
                    break
                
                # 질문 생성 (주제에 따라 여러 유형의 질문 생성)
                questions = generate_questions(topic, i, len(chunks))
                
                # 질문별 파인튜닝 데이터 생성
                for question in questions:
                    # 이 파일에 대한 샘플 수가 제한에 도달하면 중단
                    if file_samples_count >= samples_per_file[text_file]:
                        break
                        
                    data.append({
                        "messages": [
                            {"role": "user", "content": question},
                            {"role": "assistant", "content": chunk}
                        ]
                    })
                    file_samples_count += 1
        
        except Exception as e:
            print(f"파일 '{text_file}' 처리 중 오류 발생: {e}")
      # 전체 데이터 수가 max_lines를 초과하면 랜덤하게 샘플링
    if len(data) > max_lines:
        print(f"전체 데이터가 제한({max_lines}개)을 초과하여 무작위로 샘플링합니다.")
        data = random.sample(data, max_lines)
    
    # JSONL 파일로 저장
    with open(output_file, 'w', encoding='utf-8') as f:
        for item in data:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')
    
    print(f"파인튜닝 데이터 변환 완료: {len(data)}개의 대화 쌍이 {output_file}에 저장되었습니다.")


def split_content_into_chunks(content, max_chunk_size=500):
    """
    긴 콘텐츠를 적절한 크기의 청크로 나눔
    """
    # 단락으로 분리
    paragraphs = re.split(r'\n\s*\n', content)
    
    chunks = []
    current_chunk = ""
    
    for paragraph in paragraphs:
        # 단락이 너무 길면 문장 단위로 나누기
        if len(paragraph) > max_chunk_size:
            sentences = re.split(r'(?<=[.!?])\s+', paragraph)
            for sentence in sentences:
                if len(current_chunk) + len(sentence) <= max_chunk_size:
                    current_chunk += sentence + " "
                else:
                    if current_chunk:
                        chunks.append(current_chunk.strip())
                    current_chunk = sentence + " "
        else:
            if len(current_chunk) + len(paragraph) <= max_chunk_size:
                current_chunk += paragraph + "\n\n"
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = paragraph + "\n\n"
    
    if current_chunk:
        chunks.append(current_chunk.strip())
    
    return chunks


def generate_questions(topic, chunk_index, total_chunks):
    """
    주제와 청크 위치에 따라 다양한 질문 생성
    """
    questions = []
    
    # 기본 질문 형식들
    if chunk_index == 0:
        questions.append(f"{topic}에 대해 설명해주세요.")
        questions.append(f"{topic}이(가) 무엇인가요?")
        questions.append(f"{topic}에 대한 기본 정보를 알려주세요.")
    
    if total_chunks > 1:
        questions.append(f"{topic}의 주요 특징은 무엇인가요?")
        questions.append(f"{topic}에 대해 좀 더 자세히 알려주세요.")
        
    if chunk_index == total_chunks - 1:
        questions.append(f"{topic}에 대한 중요한 정보를 요약해주세요.")
    
    # 다양한 질문 추가
    questions.append(f"{topic}에 대해 알고 싶습니다.")
    
    return questions


if __name__ == "__main__":
    convert()
    print("파일 변환 완료! 'data' 폴더에서 결과를 확인하세요.")
