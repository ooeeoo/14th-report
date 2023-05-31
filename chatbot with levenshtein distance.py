import pandas as pd
import random

class SimpleChatBot:
    def __init__(self, filepath):
        self.questions, self.answers = self.load_data(filepath) # load_data()를 활용하여 질문과 답변을 리스트 형태로 각각 저장

    # 파일 경로에 존재하는 csv 파일을 읽고, 질문과 답변을 리스트 형태로 각각 저장
    def load_data(self, filepath):
        data = pd.read_csv(filepath)    # csv 파일로 읽어 질문과 답변을 분리
        questions = data['Q'].tolist()  # 질문열만 뽑아 파이썬 리스트로 저장
        answers = data['A'].tolist()    # 답변열만 뽑아 파이썬 리스트로 저장
        return questions, answers

    # 레벤슈타인 거리를 계산하는 함수
    def calc_distance(self, input_sentence, question):
        if input_sentence == question: return 0      # 같으면 0을 반환
        input_len = len(input_sentence)              # input_sentance의 길이 계산
        question_len = len(question)                 # question의 길이 계산
        if input_sentence == "": return question_len # input_sentence에 "" 입력시 question의 길이 만큼 거리가 존재
        if question == "": return input_len          # question에 "" 입력시 input_sentence의 길이 만큼 거리가 존재

        matrix = [[] for i in range(input_len+1)] 
        # [[],
        #  [],
        #  [],
        #  []]

        for i in range(input_len+1):
            matrix[i] = [0 for j in range(question_len+1)]
        # [[0, 0, 0, 0],
        #  [0, 0, 0, 0],
        #  [0, 0, 0, 0],
        #  [0, 0, 0, 0]]
        
        for i in range(input_len+1):
            matrix[i][0] = i
        for j in range(question_len+1):
            matrix[0][j] = j
        # [[0, 1, 2, 3],
        #  [1, 0, 0, 0],
        #  [2, 0, 0, 0],
        #  [3, 0, 0, 0]] 

        for i in range(1, input_len+1):
            ac = input_sentence[i-1]
            for j in range(1, question_len+1):
                bc = question[j-1] 
                cost = 0 if (ac == bc) else 1  #  파이썬 조건 표현식 예:) result = value1 if condition else value2
                matrix[i][j] = min([
                    matrix[i-1][j] + 1,     # 문자 제거: 위쪽에서 +1
                    matrix[i][j-1] + 1,     # 문자 삽입: 왼쪽 수에서 +1   
                    matrix[i-1][j-1] + cost # 문자 변경: 대각선에서 +1, 문자가 동일하면 대각선 숫자 복사
                ])
        return matrix[input_len][question_len]  

    # 질문 받은 내용과 가장 유사한 질문을 데이터셋에서 찾고, 이에 해당하는 답변을 반환하는 함수
    def find_best_answer_lev(self, input_sentance):
        similarities = []                     # 입력 받은 질문과 데이터셋 내 질문 간 레벤슈타인 거리를 저장할 리스트를 생성
        for i in range(len(self.questions)):
            similar = self.calc_distance(input_sentance, self.questions[i])  # calc_distance()를 활용하여 레벤슈타인 거리를 계산
            similarities.append(similar + (random.random() / 10))            # similarities 리스트에 계산된 레벤슈타인 거리를 추가, 
                                                                             # 이때 같은 유사도 내에서 무작위 답변을 위한 난수 추가
        best_match_index = similarities.index(min(similarities))             # similarities 리스트 내 레벤슈타인 거리가 가장 작은 인수의 index를 산출
        # return self.answers[best_match_index], self.questions[best_match_index], min(similarities)
        return self.answers[best_match_index]
    
    ############################################# CSV 파일 경로 수정 필요
# filepath = 'c:\\Users\\lifec\\OneDrive\\Desktop\\바탕화면 백업\\사이버 대학\\4학년 1학기\\AI개발실무\\14주차 챗봇\\chatbot\\ChatbotData.csv'
filepath = 'ChatbotData.csv'
chatbot = SimpleChatBot(filepath)  # 인스턴스를 생성

# '종료'라는 단어가 입력될 때까지 챗봇과의 대화를 반복합니다.
while True:
    input_sentence = input('You: ')
    if input_sentence.lower() == '종료':
        break
    response = chatbot.find_best_answer_lev(input_sentence)
    print('Chatbot:', response)
    # response, response_2, response_3 = chatbot.find_best_answer_lev(input_sentence) # test
    # print('Chatbot:', response, '            Best_similarity_question :', response_2, '           Similarity :', response_3) # test