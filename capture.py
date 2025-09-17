import subprocess
import time
import os
from datetime import datetime

def capture_screenshot():
    """맥OS 내장 명령어로 스크린샷을 찍는 함수"""
    now = datetime.now()
    
    # 날짜별 폴더명 생성
    date_folder = now.strftime("%Y-%m-%d")  # 2025-09-17
    
    # 맥북 기본 스크린샷 파일명 형식
    # Screenshot 2025-09-17 at 4.11.46 PM
    filename = now.strftime("Screenshot %Y-%m-%d at %I.%M.%S %p.png")
    
    # Screenshots/2025-09-17 폴더 생성
    folder_path = os.path.join("Screenshots", date_folder)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    
    # 맥OS screencapture 명령어 사용
    filepath = os.path.join(folder_path, filename)
    subprocess.run(["screencapture", "-x", filepath])
    
    print(f"스크린샷 저장완료: {filepath}")

def is_working_hours():
    """현재 시간이 오전 9시~오후 6시 사이인지 확인"""
    now = datetime.now()
    return 9 <= now.hour < 18

def wait_until_next_10min():
    """다음 10분까지 대기하는 함수"""
    now = datetime.now()
    
    # 다음 10분 계산
    next_10min = now.replace(minute=10, second=0, microsecond=0)
    if now.minute >= 10:
        # 다음 시간의 10분으로 설정
        if now.hour == 23:
            next_10min = next_10min.replace(hour=0, day=now.day+1)
        else:
            next_10min = next_10min.replace(hour=now.hour+1)
    
    # 대기 시간 계산
    wait_seconds = (next_10min - now).total_seconds()
    
    print(f"다음 캡처 시간: {next_10min.strftime('%H:%M')}")
    print(f"{int(wait_seconds)}초 대기 중...")
    
    time.sleep(wait_seconds)

def main():
    print("강의 스크린샷 자동 캡처 시작!")
    print("📅 오전 9시 ~ 오후 6시")
    print("🕙 매시 10분마다 자동 캡처")
    print("종료하려면 Ctrl+C를 누르세요.\n")
    
    try:
        while True:
            now = datetime.now()
            
            # 현재 시간이 작업 시간대이고 10분인 경우 캡처
            if is_working_hours() and now.minute == 10:
                capture_screenshot()
                # 1분 대기 (중복 실행 방지)
                time.sleep(60)
            
            # 다음 10분까지 대기
            wait_until_next_10min()
    
    except KeyboardInterrupt:
        print("\n프로그램이 종료되었습니다.")

if __name__ == "__main__":
    main()