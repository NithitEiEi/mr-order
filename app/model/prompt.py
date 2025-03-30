prompt = """
    Your task is turning incoming message into text JSON
    for parsing to actual JSON later. The information you
    generate can be blanked or make a default value based
    on each JSON key specifications I will provide to you.

    Note: You must return JSON in text like
    " 
    {
        data...
    }
    "
    no json type in text and no ``` cover the json

    "intent": "make", "update", "cancel", "general"
        - make is customer make food ordering in the message
          should request menus and amount of each menu.
          Menu that you create should exist in seller's menu.
          if customer already have order it's consider an update
        - update is customer try to change information in
          their order like change or add menu or others data
          if add menu, also generate old menu again with additional menu
        - cancel is customer cancel their order just shown "intent" key
        - general is regular message like greeting, questioning
          or other things that no request menus and amount
          just show "intent" key
        - ask is either relate to the ordering and other topic, but it
          about asking the seller about something 

    example in case "cancel" and "general"
    "
    {
        "intent": "cancel" / "general" / "ask", # based on your classification
        # ignore other fields
    }
    "
    
    example in case "make" and "update"
    in "update" combine with the customer old order.
    customer may fill missing data or change some data.
    no old order consider make new order.
    "
    {
        "intent": "make", # customer request for orders
        "payment": "CASH" / "TRANSFER", # payment method
                                        # default "TRANSFER"
        "address": "..." # customer's address
                         # maybe formal address or just
                         # explain the places around
        "menu": "valid" / "invalid", # invalid in case have non-exist menu request
        "detail": [
            {
                "menu": "..." # menu ID
                "name": "..." # menu name
                "amount": 1, # amount required to the menu
            }
        ], # [] if menu key is "invalid"
        "total": 100 # fill the actual total price 
    }
    "
"""

slip_prompt = """
  Your task have to read the image can fill data with
  text JSON and I will parse to the actual JSON later
  image has 2 types
  - slip: payment slip that customer send to the seller
  - others: others image that is not payment slip
  this is text JSON example
  
  "{
    type: "others" / "slip", # image type
    sender: "", # the sender name in slip
    receiver: "" # the receiver name in slip
    amount: 1 # the amount paid in the slip
    date: "" # datetime in UTF ISO format
    ref: "" # ref number of the slip
  }"

  Only output the JSON structure without any additional text,
  formatting hints, or language indicators.
"""

receipt_prompt = """
  Your task have to read the image fill data to the JSON
  image has 2 types
  - receipt: the image is receipt and able to extract text
  - others: others things that are not receipt
  this is example JSON

  "
  {
    type: "others" / "receipt", # based on the image
    date: "", # date in receipt in UTF ISO format
              # date default as today
    detail: [
      item: "", # ingredient ID exsit in the shop
      name: "", # name of the ingredient if thai gnerate thai alphabet not uft code like u0e21
      quantity: 1, # quantity of the items bill
      price: 1, # price of that item in bill
    ],
  }
  "
  NOTE that detail item must exist in the ingredient list
  if in the receipt don't have any items in the list, fill
  empty array []

  ingredient list:
"""