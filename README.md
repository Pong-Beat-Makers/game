# game
drf + channel를 이용한 실시간 ping-pong game server
***
# game_data
***
## 게임 데이터 요청 방법
#### Http Method: GET
#### Path: /game/histroy/
***
## 응답예시
#### 형식: Json
***
### 성공
#### status code: 200 OK
<pre>
<code>
{
  "id": "< 게임 데이터 id>",
  "user1_nickname": "<유저1 닉네임(게임 상 왼쪽에 있는 유저)>",
  "user2_nickname": "<유저2 닉네임(게임 상 오른쪽에 있는 유저)>",
  "user1_score": "<유저1 점수>",
  "user2_score": "<유저2 점수>",
  "match_type": "<랜덤인지 토너먼트인지 type>",
  "created_at": "<게임이 끝난 날짜와 시간>",
}
</code>
</pre>
***
### 실패
#### status code: 404 Not Found
<pre>
<code>
{
  "error": "data not found"
}
</code>
</pre>
