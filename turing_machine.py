import pandas as pd

def split(word): 
    return [char for char in word]

def print_turing_machine_id(tape, tm_head_position, tm_state, step_no):
    # START: Print Turing Machine ID
    tape_copy = tape.copy()
    tape_copy.insert(tm_head_position, tm_state)
    print('-' * 50)
    print("Step:", step_no)
    print('-' * 50)
    print(tape_copy)
    print()

    step_no += 1
    # END: Pring Turing Machine ID

    return step_no

def simulate_tm(TM_df, tm_state, tm_head_position, tape, final_state):

    step_no = 1

    while tm_state not in [final_state, 'invalid']:

        # Print ID
        step_no = print_turing_machine_id(tape, tm_head_position, tm_state, step_no)

        # START: Simulate Step
        tape_symbol = tape[tm_head_position]

        # Retrieve the transition instructions for the current turing machine state and tape symbol
        transition_instructions = TM_df.at[tm_state, tape_symbol]

        # If there are no instructions for the current turing machine state and tape symbol
        if not(transition_instructions):
            # Mark state as invalid and end the loop
            tm_state = 'invalid'
            tape[tm_head_position] = tape_symbol
        else:
            # Change the turing machine's state
            tm_state = transition_instructions[0]

            # Write the symbol to the tape
            tape[tm_head_position] = transition_instructions[1]

            # START: Move
            tm_direction = transition_instructions[2]

            if tm_direction == 'R':
                tm_head_position += 1
            else: 
                tm_head_position -= 1
            # END: Move

            # If we have no more symbols, append a blank on the relevant side of the tape so we can continue processing.
            if tm_head_position == len(tape) - 1:
                tape.append('B')
            elif tm_head_position == 0:
                tape.insert(0, 'B')
                tm_head_position += 1

        # END: Simulate Step

    # Print final ID
    step_no = print_turing_machine_id(tape, tm_head_position, tm_state, step_no)

    return tape

# --- Assignment 2: Input 10011

# TM_df = pd.DataFrame()
# TM_df['δ(q,a)']=['q0','q1','q2','qf']
# TM_df['0']=[('q0', '1', 'R'), ('q2', '0', 'L'), (), ()]
# TM_df['1']=[('q1', '1', 'R'), ('q2', '1', 'L'), ('q0', '0', 'R'), ()]
# TM_df['B']=[('qf', 'B', 'R'), ('q2', 'B', 'L'), (), ()]
# TM_df=TM_df.set_index('δ(q,a)')

# tm_state = 'q0'
# tape = split('10011')
# tm_head_position = 0
# final_state = 'qf'

# tape = simulate_tm(TM_df, tm_state, tm_head_position, tape, final_state)

# --- Assignment 2: Input 11111

# TM_df = pd.DataFrame()
# TM_df['δ(q,a)']=['q0','q1','q2','qf']
# TM_df['0']=[('q0', '1', 'R'), ('q2', '0', 'L'), (), ()]
# TM_df['1']=[('q1', '1', 'R'), ('q2', '1', 'L'), ('q0', '0', 'R'), ()]
# TM_df['B']=[('qf', 'B', 'R'), ('q2', 'B', 'L'), (), ()]
# TM_df=TM_df.set_index('δ(q,a)')

# tm_state = 'q0'
# tape = split('11111')
# tm_head_position = 0
# final_state = 'qf'

# tape = simulate_tm(TM_df, tm_state, tm_head_position, tape, final_state)

# --- Workshop 10 Slides 25-31

# TM_df = pd.DataFrame()
# TM_df['δ(q,a)']=['q']
# TM_df['0']=[('q', '0', 'R')]
# TM_df['1']=[('f', '0', 'R')]
# TM_df['B']=[('q', '1', 'L')]
# TM_df=TM_df.set_index('δ(q,a)')

# tm_state = 'q'
# tape = split('00')
# tm_head_position = 0
# final_state = 'f'

# tape = simulate_tm(TM_df, tm_state, tm_head_position, tape, final_state)