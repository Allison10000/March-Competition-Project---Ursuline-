
from calendar import calendar
"""
this program is a budgeting tool that allows the user to input their finances and get 
an analysis of their spending habits, as well as suggestions for how to improve their finances. 
It also has a calendar feature that allows the user to see when their expenses are due and 
how they can plan their finances accordingly. It's target audience is highschool students, 
college students, and any other poeple who need to be aware of their spending habits
"""


currentbalance = 0
expenses = []
expensevalues = []
largestexpense = ""
more= True
done = False
weekstart = 0

#finction to clean inputs 
def cleandata(value):
    for i in ["$", ",", " "]:
        value = value.replace(i,"")
    return float(value)

#function to update finances
def updatefinancesstart():
    #collecting values
    currentbalance = cleandata(input("balance at the start of the week: "))
    weekstart = currentbalance
    paidthisweek = input("did you get paid this week? ")
    if paidthisweek in ["yes", "Yes", "y", "Y"]:
        currentbalance = float(currentbalance) + cleandata(input("how much did you get paid this week after taxes? "))
    #calculating values
    setmore = input("did you have expenses to report this week: ")
    if setmore in ["yes", "Yes", "Y", "y"]:
        more = True
    else:
        more = False

    while more == True:
        expenses.append(input("what was the expense titled? "))
        expensevalues.append(cleandata(input("how much did you pay? ")))
        setmore = input("do you have more expenses to report? ")
        if setmore == "no" or setmore == "No" or setmore == "N":
            more = False
    print(" ")
    print(" ")
    for i in range(len(expensevalues)):
        currentbalance = currentbalance - float(expensevalues[i])
    print("you current balance is ", currentbalance)


    #manual analasys
    #how many expenses
    print("this week you had ", len(expenses), " expenses")
    #what you are on track for 
    print("this week, your net money gained/lost is ", currentbalance-weekstart)
    print(" ")
def option1():
    print("\n================ EXPENSE LIST ================\n")
    print(f"{'Expense':<25} {'Amount ($)':>12}")
    print("-" * 40)

    for title, value in zip(expenses, expensevalues):
        print(f"{title:<25} {value:>12}")

    print("\n" + "="*40 + "\n")
def option2():
    principalamount = cleandata(input("what is the principal amount: "))
    interestrate = cleandata(input("what is the interest rate as a percentage: "))
    print("this assumes you are paying the loan back on a monthly basis")
    permonth = cleandata(input("how much do you intend to pay back per month: "))

    currentmonth = 1

    # print table header
    print(f"{'Month':<10}{'Balance':<15}")
    print("-" * 25)

    while principalamount > 0:
        if currentmonth % 12 == 0:
            principalamount = principalamount + principalamount * (interestrate / 100.0)

        principalamount = principalamount - permonth
        if principalamount < 0:
            principalamount = 0

        # print each row formatted
        print(f"{currentmonth:<10}{principalamount:<15.2f}")

        currentmonth += 1
def option3():   
    twoweeksalary = cleandata(input("what is your average salary per two week paycheck: "))
    daysofmonth = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31]
    monthlyexpensesordered = []
    monthlyexpensevaluesordered = []
    moreexpenses = True
    monthlyexpenses = []
    monthlyexpensevalues = [] 
    deadlines = []
    while moreexpenses == True:
        monthlyexpenses.append(input("what is the title of the expense: "))
        monthlyexpensevalues.append(cleandata(input("how much do you pay for this expense per month: ")))
        deadlines.append(input("when is the deadline for this expense, if there is no deadline type N/A. (input day of the month) "))
        setmore = input("do you have more expenses to report? ")
        if setmore == "no" or setmore == "No" or setmore == "N":
            moreexpenses = False
    # Convert deadlines to integers or None
    clean_deadlines = []
    for d in deadlines:
        if d.lower() == "n/a":
            clean_deadlines.append(None)
        else:
            clean_deadlines.append(int(d))

    # Build calendar dictionary
    calendar = {day: [] for day in daysofmonth}

    # Step 1: Place expenses with real deadlines
    for title, value, deadline in zip(monthlyexpenses, monthlyexpensevalues, clean_deadlines):
        if deadline is not None:
            calendar[deadline].append((title, value))

    # Step 2: Distribute N/A expenses evenly
    na_items = [(t, v) for t, v, d in zip(monthlyexpenses, monthlyexpensevalues, clean_deadlines) if d is None]

    if na_items:
        spacing = len(daysofmonth) // len(na_items)
        day_pointer = 1

        for title, value in na_items:
            # Find next empty-ish day
            while day_pointer <= 31 and len(calendar[day_pointer]) > 0:
                day_pointer += 1
            if day_pointer > 31:
                day_pointer = 1  # wrap around if needed
            calendar[day_pointer].append((title, value))
            day_pointer += spacing
    # Step 3: Calculate totals
    monthly_income = twoweeksalary * 2
    total_expenses = sum(monthlyexpensevalues)
    end_balance = monthly_income - total_expenses

    # Step 4: Print calendar
    print("\n=== MONTHLY CALENDAR ===")
    for day in daysofmonth:
        print(f"Day {day}:")
        if calendar[day]:
            for item in calendar[day]:
                print(f"   - {item[0]}: ${item[1]}")
        else:
            print("   (no expenses)")

    print("\n=== SUMMARY ===")
    print(f"Income this month: ${monthly_income}")
    print(f"Total expenses: ${total_expenses}")
    print(f"End-of-month balance: ${end_balance}")   
def option4(currentbalance, expenses, expensevalues):
    """
    Lifestyle Impact Calculator
    ---------------------------
    Takes the user's current balance, list of expenses, and their values.
    Groups lifestyle-related expenses and shows how reducing them affects
    monthly and yearly savings.
    """

    # Step 1: Define lifestyle categories and keywords
    lifestyle_categories = {
        "Coffee": ["coffee", "starbucks", "latte"],
        "Eating Out": ["restaurant", "chipotle", "mcdonald", "food", "takeout", "door dash", "doordash"],
        "Uber/Transport": ["uber", "lyft", "taxi", "bus"],
        "Entertainment": ["movie", "netflix", "spotify", "concert", "game"],
        "Shopping": ["clothes", "shopping", "amazon", "target"]
    }

    # Step 2: Initialize category totals
    category_totals = {cat: 0 for cat in lifestyle_categories}

    # Step 3: Assign each expense to a category if it matches keywords
    for title, value in zip(expenses, expensevalues):
        lower_title = str(title).lower()
        try:
            amount = float(value)
        except ValueError:
            # Skip values that can't be converted to numbers
            continue

        for category, keywords in lifestyle_categories.items():
            if any(keyword in lower_title for keyword in keywords):
                category_totals[category] += amount


    # Step 4: Display current lifestyle spending
    print("\n=== CURRENT LIFESTYLE SPENDING ===")
    for category, total in category_totals.items():
        print(f"{category}: ${total:.2f}")

    # Step 5: Ask user which category they want to reduce
    print("\nWhich category would you like to reduce?")
    for i, category in enumerate(category_totals.keys(), start=1):
        print(f"{i}. {category}")

    choice = int(input("Enter the number of the category: "))
    chosen_category = list(category_totals.keys())[choice - 1]

    # Step 6: Ask reduction percentage
    reduction_percent = float(input(f"How much do you want to reduce {chosen_category} spending by (%)? "))

    # Step 7: Calculate savings
    current_spending = category_totals[chosen_category]
    monthly_savings = current_spending * (reduction_percent / 100)
    yearly_savings = monthly_savings * 12
    new_balance = currentbalance + monthly_savings

    # Step 8: Print results
    print("\n=== IMPACT ANALYSIS ===")
    print(f"Current spending on {chosen_category}: ${current_spending:.2f}")
    print(f"Monthly savings if reduced by {reduction_percent}%: ${monthly_savings:.2f}")
    print(f"Projected yearly savings: ${yearly_savings:.2f}")
    print(f"New projected end-of-month balance: ${new_balance:.2f}")

    return {
        "category": chosen_category,
        "monthly_savings": monthly_savings,
        "yearly_savings": yearly_savings,
        "new_balance": new_balance
    }
def option5(expenses, expensevalues):
    """
    Analyzes how expenses are trending over time and prints
    a terminal ASCII graph at the end.
    """

    # -----------------------------
    # Convert values to floats
    # -----------------------------
    values = []
    for v in expensevalues:
        try:
            values.append(float(v))
        except:
            values.append(0)

    if not values:
        print("No expense data available.")
        return

    # -----------------------------
    # Overall trend
    # -----------------------------
    first_half = values[:len(values)//2]
    second_half = values[len(values)//2:]

    avg_first = sum(first_half) / len(first_half) if first_half else 0
    avg_second = sum(second_half) / len(second_half) if second_half else 0

    if avg_second > avg_first:
        overall_trend = "increasing"
    elif avg_second < avg_first:
        overall_trend = "decreasing"
    else:
        overall_trend = "flat"

    percent_change = 0
    if avg_first > 0:
        percent_change = ((avg_second - avg_first) / avg_first) * 100

    # -----------------------------
    # Rolling average (3‑point)
    # -----------------------------
    rolling_avg = []
    window = 3
    for i in range(len(values)):
        if i + 1 < window:
            rolling_avg.append(None)
        else:
            window_slice = values[i-window+1:i+1]
            rolling_avg.append(sum(window_slice) / window)

    # -----------------------------
    # Print summary
    # -----------------------------
    print("\n=== EXPENSE TREND SUMMARY ===")
    print(f"Overall trend: {overall_trend}")
    print(f"Percent change: {percent_change:.2f}%")
    print("Rolling averages:", rolling_avg)

    # -----------------------------
    # ASCII Graph Helper Function
    # -----------------------------
    def ascii_trend_graph(values):
        max_val = max(values)
        min_val = min(values)
        height = 10

        if max_val == min_val:
            max_val += 1

        scaled = [
            int((v - min_val) / (max_val - min_val) * (height - 1))
            for v in values
        ]

        print("\n=== EXPENSE TREND GRAPH ===")
        for row in reversed(range(height)):
            line = ""
            for point in scaled:
                line += "●" if point == row else " "
            print(line)

        print("─" * len(values))
        print(f"Min: {min_val:.2f}   Max: {max_val:.2f}\n")

    # -----------------------------
    # Call the graph at the end
    # -----------------------------
    ascii_trend_graph(values)

    # Return data if you want to use it elsewhere
    return {
        "overall_trend": overall_trend,
        "percent_change": percent_change,
        "rolling_average": rolling_avg
    }
def option6(expenses, expensevalues):
    """
    Analyzes spending habits and prints personalized suggestions
    for reducing expenses.
    """

    # --- 0. Clean and align data types ---
    cleaned_expenses = []
    cleaned_values = []

    for title, value in zip(expenses, expensevalues):
        try:
            num_value = float(value)
            cleaned_expenses.append(title)
            cleaned_values.append(num_value)
        except (ValueError, TypeError):
            continue

    if not cleaned_expenses:
        print("No valid numeric expenses found. Check that expensevalues are numbers or numeric strings.")
        return []

    data = list(zip(cleaned_expenses, cleaned_values))

    # --- 1. Spending by category ---
    category_totals = {}
    category_counts = {}

    for title, value in data:
        category_totals[title] = category_totals.get(title, 0) + value
        category_counts[title] = category_counts.get(title, 0) + 1

    sorted_categories = sorted(category_totals.items(), key=lambda x: x[1], reverse=True)

    # --- 2. Frequent small purchases ---
    small_purchase_threshold = 15
    small_purchases = [v for v in cleaned_values if v <= small_purchase_threshold]

    # --- 3. Spikes ---
    spikes = []
    for i in range(1, len(cleaned_values)):
        if cleaned_values[i-1] > 0 and cleaned_values[i] > cleaned_values[i-1] * 1.75:
            spikes.append((cleaned_expenses[i], cleaned_values[i]))

    # --- 4. Build suggestions ---
    suggestions = []

    if sorted_categories:
        top_cat, top_value = sorted_categories[0]
        suggestions.append(
            f"You spend the most on {top_cat} (${top_value:.2f}). "
            f"Try setting a weekly cap or switching to cheaper alternatives."
        )

    for cat, count in category_counts.items():
        if count >= 5:
            suggestions.append(
                f"You purchased {cat} {count} times. "
                f"Consider batching these purchases or limiting them to certain days."
            )

    if len(small_purchases) >= 4:
        suggestions.append(
            f"You have {len(small_purchases)} small purchases under ${small_purchase_threshold}. "
            "These add up—try a no‑spend day rule or weekly limit."
        )

    for title, value in spikes:
        suggestions.append(
            f"Your spending on {title} jumped to ${value:.2f}. "
            "Review whether this was necessary or can be avoided next time."
        )

    if not suggestions:
        suggestions.append("Your spending looks stable. No major habits need adjusting!")

    # --- 5. Print suggestions ---
    print("\nSpending Suggestions:")
    for s in suggestions:
        print("- " + s)

    return suggestions
#provides more options for the user to chooose
def morefinanceoptions():
    print(" ")
    print("More Options:")
    print("option 1: see an itemized list of your expenses")
    print("option 2: interpret a loan")
    print("option 3: create a budget/payment plan for this month")
    print("option 4: lifestyle impact calculator (see how reducing certain expenses can impact your finances) ")
    print("option 5: expense trend analyzer (see how your expenses are trending over time) ") 
    print("option 6: personalized spending suggestions (get personalized suggestions for reducing your expenses based on your spending habits) ") 
    selection = input("what option: ")
    if selection == "1" or selection == "1 ":
        print(" ")
        option1()
    print(" ")
    if selection == "2" or selection == "2 ":
        print (" ")
        option2()
    if selection == "3" or selection == "3 ":
        print(" ")
        option3()
    if selection == "4" or selection == "4 ":
        print(" ")
        option4(currentbalance, expenses, expensevalues)
    if selection == "5" or selection == "5 ":
        print(" ")
        option5(expenses, expensevalues)
    if selection == "6" or selection == "6 ":
        print(" ")
        option6(expenses, expensevalues)
    selection = input("do you want to continue with additional options: ")
    if selection in ["yes", "Yes", "y", "Y"]:
        morefinanceoptions()

#main
def main():
    updatefinancesstart()
    morefinanceoptions()
main()