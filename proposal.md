# Goal of this project
Managing money is not an easy task, it will be hard to figure out how the money goes.
Sometimes the items on receipts are hard to recognize, easpicially for me, a non-native English speaker.
And I wish there can be someone stop me from buying duplicate stuff that I just forget I have one but frozed in the deepest side of my freezer.
We hope to build a personal financial management app, which can have the abilities with:
     1. record costs
     2. summary weekly / monthly spending
     3. auto merge (ex. merge items purchased from Costco to the spending in Costco in same purchase)
     4. show how money goes (category / merchant)
     5. can help recognize the items on my receipts
     6. recognize the unformatted text like "bought a used PC with 300 dollars yesterday" -> ("buy used PC", "300", "2024-10-15(example of yesterday)")
     7. spending forecast



## Current Target
What we want to do in this part is build a MVP (minimum viable product) for personal financial management app.

## idea
Most of the functions can be achieved by hard coding, but we want to use LLM to replace it, and add functions providing more tools to the model.
So want we are designing is letting a model which can understand what the user wants to do, and want tools it has, and then doing the corresponding operations by ReACT.


- When doing refund, the agent will check whether the spending exists in the system, if yes, the refund will be recorded as well. (ex. refund the item bought from Costco, the refund will be recorded in the Costco spending), if not, the system will pop an error message and ask the user to input the refund information.