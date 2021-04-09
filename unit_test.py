import unittest
import pandas as pd
from cfg_to_cnf import CFG_to_CNF_Converter
from turing_machine import simulate_tm, split

class Test_CNF_to_CFG_methods(unittest.TestCase):

    def test_one(self):
        variables = ['S']
        terminals = ['0', '1']
        productions = [
            ('S', ['0', 'S', '0']),
            ('S', ['1', 'S', '1']),
            ('S', ['1']),
            ('S', ['0'])
            ]
        terminal_variable_dict = dict()

        converter = CFG_to_CNF_Converter(productions, variables, terminals, terminal_variable_dict)

        cnf = converter.cfg_to_cnf()

        cnf_correct_output_string = "[('A1', ['0']), ('A2', ['1']), ('S', ['A1', 'A3']), ('A3', ['S', 'A1']), ('S', ['A2', 'A4']), ('A4', ['S', 'A2']), ('S', ['1']), ('S', ['0'])]"

        self.assertEqual(str(cnf), cnf_correct_output_string, "Test")

    def test_two(self):
        variables = ['S', 'T', 'U']
        terminals = ['0', '1']
        productions = [
            ('S', ['0', 'S', '0']),
            ('S', ['1', 'S', '1']),
            ('S', ['1']),
            ('S', ['0']),
            ('S', ['T', 'T']),
            ('S', ['U', 'U']),
            ('T', ['1']),
            ('U', ['0']),
            ]
        # If a variable already exists, such that it points to ONE and ONLY ONE terminal, add it to the
        # terminal variable dictionary so we don't accidentally produce useless states, otherwise, leave
        # blank.
        terminal_variable_dict = {
            '1': 'T',
            '0': 'U'
        }

        converter = CFG_to_CNF_Converter(productions, variables, terminals, terminal_variable_dict)

        cnf = converter.cfg_to_cnf()

        cnf_correct_output_string = "[('S', ['U', 'A1']), ('A1', ['S', 'U']), ('S', ['T', 'A2']), ('A2', ['S', 'T']), ('S', ['1']), ('S', ['0']), ('S', ['T', 'T']), ('S', ['U', 'U']), ('T', ['1']), ('U', ['0'])]"

        self.assertEqual(str(cnf), cnf_correct_output_string, "Test")

    def test_three(self):
        variables = ['S']
        terminals = ['0', '1']
        productions = [
            ('S', ['0']),
            ('S', ['1'])
            ]
        terminal_variable_dict = dict()

        converter = CFG_to_CNF_Converter(productions, variables, terminals, terminal_variable_dict)

        cnf = converter.cfg_to_cnf()

        cnf_correct_output_string = "[('S', ['0']), ('S', ['1'])]"

        self.assertEqual(str(cnf), cnf_correct_output_string, "Test")

    def test_four(self):
        variables = ['A', 'B', 'D']
        terminals = ['c', 'e']
        productions = [('A',['B','c','D','e'])]
        terminal_variable_dict = dict()

        converter = CFG_to_CNF_Converter(productions, variables, terminals, terminal_variable_dict)

        cnf = converter.cfg_to_cnf()

        cnf_correct_output_string = "[('A1', ['c']), ('A2', ['e']), ('A', ['B', 'A3']), ('A3', ['A1', 'A4']), ('A4', ['D', 'A2'])]"

        self.assertEqual(str(cnf), cnf_correct_output_string, "Test")

class Test_Turing_Machine(unittest.TestCase):

    def test_one(self):
        # states = ['q0','q1','q2','qf']
        # input_symbols = ['0','1']
        # tape_symbols = ['0','1','B']

        TM_df = pd.DataFrame()
        TM_df['δ(q,a)']=['q0','q1','q2','qf']
        TM_df['0']=[('q0', '1', 'R'), ('q2', '0', 'L'), (), ()]
        TM_df['1']=[('q1', '1', 'R'), ('q2', '1', 'L'), ('q0', '0', 'R'), ()]
        TM_df['B']=[('qf', 'B', 'R'), ('q2', 'B', 'L'), (), ()]
        TM_df=TM_df.set_index('δ(q,a)')

        tm_state = 'q0'
        tape = split('10011')
        tm_head_position = 0
        final_state = 'qf'

        tape = simulate_tm(TM_df, tm_state, tm_head_position, tape, final_state)

        expected_final_tape = ['B', '0', '1', '1', '0', '0', 'B', 'B', 'B']

        self.assertEqual(tape, expected_final_tape, "Test")

    def test_two(self):
        # states = ['q0','q1','q2','qf']
        # input_symbols = ['0','1']
        # tape_symbols = ['0','1','B']

        TM_df = pd.DataFrame()
        TM_df['δ(q,a)']=['q0','q1','q2','qf']
        TM_df['0']=[('q0', '1', 'R'), ('q2', '0', 'L'), (), ()]
        TM_df['1']=[('q1', '1', 'R'), ('q2', '1', 'L'), ('q0', '0', 'R'), ()]
        TM_df['B']=[('qf', 'B', 'R'), ('q2', 'B', 'L'), (), ()]
        TM_df=TM_df.set_index('δ(q,a)')

        tm_state = 'q0'
        tape = split('11111')
        tm_head_position = 0
        final_state = 'qf'

        tape = simulate_tm(TM_df, tm_state, tm_head_position, tape, final_state)

        expected_final_tape = ['B', '0', '0', '0', '0', '0', 'B', 'B', 'B']

        self.assertEqual(tape, expected_final_tape, "Test")

    def test_three(self):
        # states = ['q','f']
        # input_symbols = ['0','1']
        # tape_symbols = ['0','1','B']

        TM_df = pd.DataFrame()
        TM_df['δ(q,a)']=['q']
        TM_df['0']=[('q', '0', 'R')]
        TM_df['1']=[('f', '0', 'R')]
        TM_df['B']=[('q', '1', 'L')]
        TM_df=TM_df.set_index('δ(q,a)')

        tm_state = 'q'
        tape = split('00')
        tm_head_position = 0
        final_state = 'f'

        tape = simulate_tm(TM_df, tm_state, tm_head_position, tape, final_state)

        expected_final_tape = ['0', '0', '0', 'B', 'B']

        self.assertEqual(tape, expected_final_tape, "Test")