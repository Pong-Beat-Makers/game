# Game Server
- websocket을 이용한 Pong 게임 서버

---

## 

게임 시작 요청 -> uuid를 통해 링크 생성 -> 최대 2명 접속 가능한 웹소켓 그룹 생성
-> 2명 접속완료 시 게임 시작 -> 실시간 공 및 패들 위치 전송 

점수 
- 벽에 닿으면 득점 메시지 전송 후 위치 초기화


좌표
- 공 위치 x,y
- 공 방향 벡터
- 패들 위치 x1, x2
---

## API Specification

### 게임 기본 설정(추후 수정)
```python
# settings
self.map_width = 720
self.map_height = 480
self.ball_speed = 5
self.move_speed = 5
self.winning_score = 5
self.paddle_length = 50
self.paddle_speed = 5
```

### 멀티 게임 1대1

#### 접속
> Protocol : Websocket   
> Path : `/ws/game/<uuid>/`   
> description : 최초 두명 접속 후 게임 자동 시작


#### 게임 상태 응답
```json
{
    "ball_coords": [
        <공 x좌표>,
        <공 y좌표>
    ],
    "player1_coords": [
        <p1 paddle x좌표>,
        <p1 paddle y좌표>
    ],
    "player2_coords": [
        <p2 paddle x좌표>,
        <p2 paddle y좌표>
    ],
    "type": "send_game_status"
}
```

#### paddle 움직임 전송
```json
{
    "move" : "<up 또는 down>"
}
```


