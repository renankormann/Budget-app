'''
Created on Jul 10, 2023

@author: renan
'''

class Category:
    # Set up a class variable for the total amount of money in the budget.
    total_money = 0

    # Initiate the class with the ledger list.
    def __init__(self, name, ledger = []):
        self.name = name
        self.ledger = list(ledger)

    # Setup the deposit method
    def deposit(self, amount, description = ""):
        self.amount_deposit = amount
        self.total_money += self.amount_deposit
        self.description_deposit = description
        self.deposit_dic = {"amount" : float(self.amount_deposit), "description" : self.description_deposit} 
        self.ledger.append(self.deposit_dic)

    # Setup withdraw methot
    def withdraw(self, amount, description = ""):
        self.amount_withdraw = - amount
        self.description_withdraw = description
        self.withdraw_dic = {"amount" : float(self.amount_withdraw), "description" : self.description_withdraw}
        if self.check_funds(abs(self.amount_withdraw)):
            self.ledger.append(self.withdraw_dic)
            self.total_money += self.amount_withdraw
            return True
        else:
            return False

    # Check funds method
    def check_funds(self, amount):
        self.value = amount
        if self.value <= self.total_money:
            return True
        else:
            return False
    # Get balance method
    def get_balance(self):
        return(float("{:.2f}".format(self.total_money)))

    # Transfer method
    def transfer(self, amount, other_catg):
        self.amount_transfer = amount
        self.amount_tdescription = "Transfer to " + other_catg.name
        self.amount_received_descpt = "Transfer from " + self.name
        if abs(self.amount_transfer) > self.total_money:
            return False
        else:
            other_catg.deposit(self.amount_transfer, self.amount_received_descpt)
            self.withdraw(self.amount_transfer, self.amount_tdescription)
            return True

    # defining how the object will be printed when defined
    def __str__(self):
        self.printing = ""
        # Assigning title to self.printing
        self.halfway = 15 - len(self.name)/2
        while len(self.printing) < 30:
            if len(self.printing) == int(self.halfway):
                self.printing += self.name
            else:
                self.printing += "*"
            if len(self.printing) == 30:
                self.printing += "\n"

        # Assigning each transaction to self.printing
        for item in self.ledger:
            if len(item["description"]) >= 23:
                self.desc_hold = item["description"][:23]
            else:
                self.desc_hold = item["description"]
            self.amount_hold = "{:.2f}".format(item["amount"])

            while len(self.desc_hold) + len(self.amount_hold) < 30:
                self.desc_hold += " "

            self.printing += self.desc_hold
            self.printing += self.amount_hold
            self.printing += "\n"

        self.printing += "Total: " + "{:.2f}".format(self.total_money)   

        return self.printing


# Create the function for the graph
def create_spend_chart(catg_list):
    each_catg_total = []
    pos_total = 0
    for obj in catg_list:
        each_catg_total.append(0)
        for position in range(len(obj.ledger)):
            if obj.ledger[position]["amount"] < 0:
                each_catg_total[pos_total] += abs(obj.ledger[position]["amount"])
        pos_total += 1

    # Calculate the total amount money spent.
    total_spent = 0
    for item in each_catg_total:
        total_spent += item

    # Turn each value into percentage.
    for i in range(len(each_catg_total)):
        each_catg_total[i] = 100 * (each_catg_total[i] / total_spent)

    # I am going to create a list for each row of the table without the x-axis legend.
    table_lines = []
    line = 0
    for percentage in range(100, -10, -10):
        table_lines.append("")
        if percentage == 100:
            table_lines[line] += str(percentage) + "|" + " "
        elif percentage >= 10 and percentage <= 90:
            table_lines[line] += " " + str(percentage) + "|" + " "
        else:
            table_lines[line] += "  " + str(percentage) + "|" + " "
        
        for position in range(len(each_catg_total)):
            if each_catg_total[position] >= percentage:
                table_lines[line] += "o  "
            else:
                table_lines[line] += "   "
        
        table_lines[line] += "\n"
        line += 1
        
    # Now, we add the x-axis row made of "-"
    table_lines.append("    ")
    for i in range(3 * len(each_catg_total) + 1):
        table_lines[len(table_lines)-1] += "-"
    table_lines[len(table_lines)-1] += "\n"
    
    # To do the vertical legend I will create a list with the names of each categories.
    catg_names = []
    position = 0
    for obj in catg_list:
        catg_names.append(catg_list[position].name)
        position += 1


    ready_table = "Percentage spent by category\n"
    for item in table_lines:
        ready_table += item
    
    
    # Now, to I have to make each of the strings in the list catg_names to be displayed appropriately and vertically.
    # To do that, I will make a list with each row of the legend to be displayed.
    rows_amount = len(max(catg_names, key=len))
    legend_lines = []
    for line in range(rows_amount):
        legend_lines.append("")
        for i in range(5):
            legend_lines[line] += " "
        for name in catg_names:
            if line + 1 > len(name):
                legend_lines[line] += "   "
            else:
                legend_lines[line] += name[line] + "  "
        if line < rows_amount - 1:
            legend_lines[line] += "\n"
        
    for item in legend_lines:
        ready_table += item

    return ready_table