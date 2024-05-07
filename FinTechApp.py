#importing all needed libraries
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import ttk
from openai import OpenAI

#Initialize OpenAI
client = OpenAI()

#Main method that gets file, and posts the openAI insights to app
def mainMethod():
    #Get the inputted ticker
    ticker = entry.get()
    #Call openAI
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You help provide short explanations of companies based on ticker symbols on the NYSE"},
            {"role": "user", "content": f"Explain what the company with ticker {ticker} does, who its main customers are, market share, and competition."}
        ]
    )
    #Following code keeps calling the findTable function and posts the revieved OpenAI info to respective section on app.
    companyBackground.config(text=str(completion.choices[0].message.content))
    html_doc = openFile(ticker)  # Get the HTML content
    if html_doc:
        soup = BeautifulSoup(html_doc, 'html.parser')
        income_info = findTable('Consolidated Statements of Comprehensive Income', soup)
        IncomeInfo.config(text=income_info)  # Update the IncomeInfo label text
        balance_info = findTable('Consolidated Balance Sheets', soup)
        BalanceInfo.config(text=balance_info)  # Update the IncomeInfo label text
        cash_info = findTable('Consolidated Statements of Cash Flows',soup)
        CashInfo.config(text=cash_info)  # Update the IncomeInfo label text
        ops_info = findTable('Consolidated Statements of Operations',soup)
        OpsInfo.config(text=ops_info)  # Update the IncomeInfo label text
        risks = summarize_risks(soup)
        RiskInfo.config(text=risks)

#Method that will open the most recent file of the compnay
def openFile(ticker):
    file_path_2023 = f'/Users/pranavmarneni/sec-edgar-filings/{ticker}/10-K/2023.txt/primary-document.html'
    try:
        # Try to open the HTML file for 2023
        with open(file_path_2023, 'r') as file:
            html_doc = file.read()
            return html_doc  # Return the HTML content
    except FileNotFoundError:
        # If file for 2023 doesn't exist, try to open the file for 2022
        file_path_2022 = f'/Users/pranavmarneni/sec-edgar-filings/{ticker}/10-K/2022.txt/primary-document.html'
        try:
            with open(file_path_2022, 'r') as file:
                html_doc = file.read()
                # Update the date to 2022
                date = "2022"
                return html_doc  # Return the HTML content
        except FileNotFoundError:
            # If neither file exists, print an error message
            print("Files for both 2023 and 2022 not found!")
            return None  # Return None if file not found

#Method that takes the information from findTable and generates LLM insights
def summarize_info(info):
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an investor, you will evaluate companies."},
            {"role": "user", "content": f"Evaluate this financial information briefly: {info}"}
        ]
    )
    summary = (completion.choices[0].message)
    return summary.content

#Method that scrapes table info and send to summarize_info, which in turn posts the LLM result.
def findTable(table_name, soup):
    # Check if the lowercase, uppercase, or capitalized version of table_name exists
    for name in [table_name, table_name.upper(), table_name.capitalize()]:
        current = soup.find('div', string=name)
        if current:
            table = current.find_next('table')
            if table:
                # Print the table content
                print(f"Table containing {name} information:")
                info = table.get_text(strip=True)
                return summarize_info(info)
            else:
                print(f"Table not found after {name} div.")
                print()
                break  # Exit loop if div found but table not found
    else:
        # In some companies, balance sheet is reported as financial position resulting in previous for loop not working
        if table_name == 'Consolidated Balance Sheets':
            print(f"{table_name} not found. Looking for Consolidated Statements of Financial Position.")
            return findTable("Consolidated Statements of Financial Position", soup)
        else:
            print(f"{table_name} not found.")
            return ""

#Method to specifically find and summarize risks of investing in respective company
def summarize_risks(soup):
    riskList = []

    # Find the div containing "PART I" section
    part1_div = soup.find('div', string='PART I')

    # If "PART I" section is found
    if part1_div:
        # Find all div elements within "PART I" section
        div_elements = part1_div.find_all_next('div')
        for div in div_elements:
            # Check if the div contains risk factor information based on specific styles
            # Each company, each year changes the format in which it shows risks
            # To make this more robust additional styles are needed to be added
            # For purspose of demo and lack of time to go through every single company only more common formats are included.
            span_style = div.find('span', style='color:#000000;font-family:\'Arial\',sans-serif;font-size:10pt;font-style:italic;font-weight:700;line-height:120%')
            #To find the style, go to HTML document and find how the span for risks is styled
            if span_style:
                riskList.append(div.get_text(strip=True))
            else:
                #Check for alternate 
                span_style = div.find('span',style='color:#000000;font-family:\'Helvetica\',sans-serif;font-size:9pt;font-style:italic;font-weight:700;line-height:120%')
                if span_style:
                    riskList.append(div.get_text(strip=True))
    #Call on openAI for insight
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are helping investors evaluate companies."},
            {"role": "user", "content": f"Briefly explain the risks of investing in this company. Also explain if investing in this company still makes sense of doesn't: {riskList} "}
        ]
    )
    return(completion.choices[0].message.content)

#|||||||||| Below this all code is for the simple UI of app |||||||||||#
#||||||||||-------------------------------------------------|||||||||||#
root = tk.Tk()
root.title("Business Analysis")

canvas = tk.Canvas(root)

# Create a frame to contain all the widgets
scrollable_frame = tk.Frame(canvas)

# Function to update the scroll region of the canvas
def update_scroll_region(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

# Bind the function to the canvas resize event
canvas.bind("<Configure>", update_scroll_region)

# Add a scrollbar to scroll through the canvas
scrollbar = ttk.Scrollbar(root, orient=tk.VERTICAL, command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Attach the canvas to the scrollbar
canvas.configure(yscrollcommand=scrollbar.set)

# Add the scrollable frame to the canvas
canvas.create_window((0, 0), window=scrollable_frame, anchor=tk.NW)

# Place widgets inside the scrollable frame
label = tk.Label(scrollable_frame, text="Enter Company Ticker:")
label.pack()

#User enters ticker here
entry = tk.Entry(scrollable_frame)
entry.pack()
#Initialize submit button
button = tk.Button(scrollable_frame, text="Submit", command=mainMethod)
button.pack()
#Following is labels and sections for information
BackgroundLabel = tk.Label(scrollable_frame, text="COMPANY BACKGROUND:")
BackgroundLabel.pack()

companyBackground = tk.Label(scrollable_frame, text="", wraplength=850)
companyBackground.pack()

IncomeLabel = tk.Label(scrollable_frame, text="CONSOLIDATED INCOME STATEMENTS:")
IncomeLabel.pack()

IncomeInfo = tk.Label(scrollable_frame, text="", wraplength=1000)
IncomeInfo.pack()

BalanceLabel = tk.Label(scrollable_frame, text="BALANCE SHEETS:")
BalanceLabel.pack()

BalanceInfo = tk.Label(scrollable_frame, text="", wraplength=1000)
BalanceInfo.pack()

CashLabel = tk.Label(scrollable_frame, text="CASH FLOWS:")
CashLabel.pack()

CashInfo = tk.Label(scrollable_frame, text="", wraplength=1000)
CashInfo.pack()

OpsLabel = tk.Label(scrollable_frame, text="STATEMENT OF OPERATIONS:")
OpsLabel.pack()

OpsInfo = tk.Label(scrollable_frame, text="", wraplength=1000)
OpsInfo.pack()

RisksLabel = tk.Label(scrollable_frame, text="POSSIBLE RISKS:")
RisksLabel.pack()

RiskInfo = tk.Label(scrollable_frame, text="", wraplength=1000)
RiskInfo.pack()

canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

#Start the interactive loop
root.mainloop()