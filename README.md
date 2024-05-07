
# FinTech_Summer_Opportunities

YOUTUBE LINK TO DEMO: https://youtu.be/dTbdzrBG37s
NOTE - 
The code to download files(sec-edgar.py) was purposefully not included in the app code. Though automatic downloading of the files is key, adding this to the app code would add huge wait-times for the app to download all files and then analyse them. This would also make the demo inefficient, therefor in demo I show how this code downloads the files needed, and then switch to how the app would work. The files were also seperated to make code review easier.

Application project for FinTech Summer Opportunities

TECH STACK - 
With implementation ease and efficiency in mind, I completed the task ursing various python libraries as listed below:]
 - BeautifulSoup
After implementing the SEC downloader, I used beautifulSoup to parse the HTML of the documents to find the necessary text/tables. I used this web scrapper over others due to past implementing experience.
 - OpenAI
For the LLM functionality, I used the openAI API since I have previous experience implementing.
 - Tkinter
To create the UI I used this python GUI library. Compared to developing the app on another seperate platform like Android Studio, due to the simple nature of the app it is much easier to implement the app in python instead of integrating python to another platform. Android Studio provides a much better UI platform, but since UI isn't the main concern of this task I did not use it.

RATIONAL FOR CHOOSING SPECIFIC INSIGHTS:

Company Background - This section is highly useful for the user to get a brief, high level description of the company, its competitors, and who it's main consumers are. Through this information, users can familiarize themselves with less known corportation, look into competing firms in the industry, and have an overall better understanding of the role the company plays in its industries. This information is not scrapped from the 10-K, instead it is generated by LLM. This is because after experimenting with multiple companies, comparing where I scrape their "Business" section compared to using the LLM to generate it, the LLM almost always provided better insights. 

Comprehensive Income - 

This table provides holistic financial information beyond just net income, it allows users to see non-operating costs like investments, foreign currency fluctuations. Such non-operating costs allow the investor to determine sustainability of income, and gain an overall better understanding of investment potential.

Balance Sheets/Financial Position - 

This analysis helps investors determine financial health by understanding a companies ability to meet its short and long term obligations. Investors can also understand liquidity, which is key to cover short-term debts in case of something going wrong. These trends can very important to analyse financial health.
Cash flows - 
This analysis shows company's ability to generate cash to meet short term obligation, such as operating expenses and bills. This section also allows investors to see where the company generates most cash from. This section can also show investors where the company allocates capital. This information and trends helps provide insight into long term investment viability into company. 

Risks - 

By understanding the challenges that company could face in smooth operations, investors can make better decisions on the risk vs. benefit of investing in a specific company. Investors can also see risk mitigation strategies, which help investors feel more relaxed to concerns of risk exposure. 

WHY MD&A SECTION WAS LEFT OUT -

The Management's Discussion and Analysis(MD&A) provides many key insights to the company's finances and future outlook. However, the previously analyzed financial statements provide a much more detailed look into a company's finances. Though the company's outlook is important to understand where the compnay is going, due to the large volume of information that an LLM would have to go though in this section(many of the financial details which would be already covered in previous financial section) which would add on to already long response times of the app, this section was left out. 
