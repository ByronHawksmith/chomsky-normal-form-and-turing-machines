class CFG_to_CNF_Converter:

    def __init__(self, productions, variables, terminals, terminal_variable_dict):
        self.new_var_count = 0
        self.productions = productions
        self.variables = variables
        self.terminals = terminals
        self.terminal_variable_dict = terminal_variable_dict

    def create_new_variable(self):
        self.new_var_count += 1
        return 'A' + str(self.new_var_count)

    def break_product(self, production_variables, variables, new_productions):

        new_variables = []

        for idx, _ in enumerate(production_variables):
            # If First Production Variable
            if idx == 0:
                new_var = self.create_new_variable()
                new_variables.append(new_var)
                new_productions.append((production_variables[idx], [production_variables[idx + 1], new_var]))

            # If Second to Last Production Variable
            elif idx == len(production_variables) - 3:
                new_productions.append((new_variables[len(new_variables) - 1], [production_variables[idx + 1], production_variables[idx + 2]]))
                break

            # Else
            else:
                # If Last Variable
                if idx + 1 == len(production_variables) - 1:
                    break
                # Else; Middle Variable
                else:
                    new_var = new_variables[len(new_variables) - 1]
                    new_var_2 = self.create_new_variable()
                    new_variables.append(new_var)
                    new_variables.append(new_var_2)
                    new_productions.append((new_var, [production_variables[idx + 1], new_var_2]))

        variables = variables + new_variables
        
        return new_productions

    def cfg_to_cnf(self):

        new_productions = []

        # Step 2b: Replace terminals with new variables
        for production in self.productions:
            # If the right hand side of the production is of length > 2
            if len(production[1]) > 2:
                # For each symbol in the right hand side of the production
                for idx, symbol in enumerate(production[1]):
                    # If the symbol is a terminal
                    if symbol in self.terminals:
                        # If the terminal variable already exists
                        if symbol in self.terminal_variable_dict:
                            # Replace the symbol (which is a terminal) with it's associated variable in the dictionary
                            production[1][idx] = self.terminal_variable_dict[symbol]
                        # If the terminal variable does not exist
                        else:
                            # Create a new variable
                            new_variable = self.create_new_variable()
                            # Store a record of which terminal this new variable is associated with
                            self.terminal_variable_dict[symbol] = new_variable
                            # Append the new variable to the variables dictionary
                            self.variables.append(new_variable)
                            # Create a new production (new_variable, [symbol])
                            new_productions.append((new_variable, [symbol]))
                            # Replae the symbol (which is a terminal) with it's associated variable in the dictionary
                            production[1][idx] = self.terminal_variable_dict[symbol]
        
        for idx, production in enumerate(self.productions):
            # Get all variables for a particular production by combining the lhs and the rhs
            production_variables = list(production[0]) + production[1]

            # Ignore this production if it is currently in CNF
            if len(production_variables) > 3:
                self.break_product(production_variables, self.variables, new_productions)
            else:
                new_productions.append(production)

        # Return the new_productions array which represent the CFG converted into CNF
        return new_productions