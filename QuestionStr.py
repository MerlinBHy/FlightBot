# -*- coding:UTF-8 -*-
class QuestionStr:
    def __init__(self):
        self.start_q = "请问有什么可以帮您？\n"
        self.start_location_q = "请问您的出发城市是？\n"
        self.end_location_q = "请问您的目标城市是？\n"
        self.fight_type_q = "请问是单程航班还是往返航班？\n"
        self.start_date_q = "出发日期是？\n"
        self.return_date_q = "返回日期是\n"
        self.end_str ="你需要预订的是："

    def __input_start_q(self):
        text = raw_input(self.start_q)
        return text

    def __input_start_location_q(self):
        text = raw_input(self.start_location_q)
        return text

    def __input_end_location_q(self):
        text = raw_input(self.end_location_q)
        return text

    def __input_fight_type_q(self):
        text = raw_input(self.fight_type_q)
        return text

    def __input_start_date_q(self):
        text = raw_input(self.start_date_q)
        return text

    def __input_return_date_q(self):
        text = raw_input(self.return_date_q)
        return text

    def __input_end_str(self, info):
        text = raw_input(self.end_str + info +"\n确认请回复Y更改信息回复N")
        return text

    def get_question_str(self, status):
        switcher = {
            0: self.__input_start_q,
            1: self.__input_start_location_q,
            2: self.__input_end_location_q,
            3: self.__input_fight_type_q,
            4: self.__input_start_date_q,
            5: self.__input_return_date_q,
            6: self.__input_end_str
        }
        func = switcher.get(status, lambda: "nothing")
        return func

if __name__ == '__main__':
    q = QuestionStr()
    text = q.get_question_str(2)()
    print(text)