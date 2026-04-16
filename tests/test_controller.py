import json
import unittest
from pathlib import Path

from scripts.roundtable_controller import STATE_FILE, reset_state, route_message


class RoundtableControllerTests(unittest.TestCase):
    def setUp(self):
        reset_state()

    def load_state(self):
        return json.loads(Path(STATE_FILE).read_text(encoding='utf-8'))

    def test_start_question_creates_candidate_pool(self):
        out = route_message('人类的未来会被硅基生命代替吗？')
        self.assertIn('选 3 位你最想听的人物', out)
        state = self.load_state()
        self.assertEqual(state['status'], 'awaiting_participant_pick')
        self.assertEqual(len(state['candidate_pool']), 10)

    def test_pick_directly_enters_first_round(self):
        route_message('人类的未来会被硅基生命代替吗？')
        out = route_message('1.3.6')
        self.assertIn('STATUS: DISCUSSION_ROUND', out)
        self.assertIn('ROUND_TITLE: 第一轮', out)
        state = self.load_state()
        self.assertEqual(state['status'], 'awaiting_user_choice')
        self.assertEqual(state['current_round'], 1)
        self.assertEqual(state['pending_user_input_type'], 'user_choice')

    def test_choice_e_then_free_speech_advances_exactly_one_round(self):
        route_message('人类的未来会被硅基生命代替吗？')
        route_message('1.3.6')
        out1 = route_message('E')
        self.assertIn('另外想说的话', out1)
        state = self.load_state()
        self.assertEqual(state['status'], 'awaiting_free_speech')
        out2 = route_message('我更担心意义感被稀释。')
        self.assertIn('STATUS: DISCUSSION_ROUND', out2)
        self.assertIn('USER_INTERVENTION_TYPE: free_speech', out2)
        state = self.load_state()
        self.assertEqual(state['status'], 'awaiting_user_choice')
        self.assertEqual(state['current_round'], 2)

    def test_choice_d_advances_exactly_one_round_without_waiting(self):
        route_message('人类的未来会被硅基生命代替吗？')
        route_message('1.3.6')
        out = route_message('D')
        self.assertIn('STATUS: DISCUSSION_ROUND', out)
        self.assertIn('USER_INTERVENTION_TYPE: silent', out)
        self.assertIn('USER_INTERVENTION_CONTENT: D', out)
        state = self.load_state()
        self.assertEqual(state['current_round'], 2)

    def test_natural_sentence_at_choice_stage_is_treated_as_other_words(self):
        route_message('人类的未来会被硅基生命代替吗？')
        route_message('1.3.6')
        out = route_message('我觉得最大的问题不是替代，而是失去定义意义的能力。')
        self.assertIn('STATUS: DISCUSSION_ROUND', out)
        self.assertIn('USER_INTERVENTION_TYPE: free_speech', out)
        state = self.load_state()
        self.assertEqual(state['current_round'], 2)

    def test_reaching_max_rounds_finishes_discussion(self):
        route_message('人类的未来会被硅基生命代替吗？')
        route_message('1.3.6')
        state = self.load_state()
        state['max_rounds'] = 1
        Path(STATE_FILE).write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding='utf-8')
        out = route_message('D')
        self.assertIn('STATUS: FINAL_CONCLUSION', out)
        out2 = route_message('如果现在重新开始，我该怎么选城市？')
        self.assertIn('选 3 位你最想听的人物', out2)
        state = self.load_state()
        self.assertEqual(state['status'], 'awaiting_participant_pick')


if __name__ == '__main__':
    unittest.main()
