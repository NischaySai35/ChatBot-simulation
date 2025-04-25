from flask import Flask, render_template, request, jsonify
from chatbot_code import FAQChatBot
import webbrowser
import threading

app = Flask(__name__)

# Initialize chatbot
chatbot = FAQChatBot()
# Add some FAQs
chatbot.add_faq("bank balance?", "90000")
chatbot.add_faq("min minimum bal?", "1000 for urban branches, 500 for rural branches.")
chatbot.add_faq("timings?", "Monday to Friday: 10:00 AM to 4:00 PM, Saturday: 10:00 AM to 1:00 PM.")
chatbot.add_faq("customer care number?", "1800 1234.")
chatbot.add_faq("create account?", "Fill the SB Account opening application and submit it in the bank.")
chatbot.add_faq("sb savings  interest?", "Interest is 3.00% to 3.50% per annum.")
chatbot.add_faq("internet banking activate?", "You can Register online or visit your home branch.")
chatbot.add_faq("atm withdrawal limit?", "Rs.40,000 per day is limit for debit cards.")
chatbot.add_faq("atm/debit card block?", "Call 1800 112 211 or send 'BLOCK <last 4 digits>' to 567676.")
chatbot.add_faq("yono app?", "It is a mobile banking app for SBI customers.")
chatbot.add_faq("update mobile number?", "Visit the branch or use an SBI ATM.")
chatbot.add_faq("chequebook charges?", "chequebook charges is Rs.3 per cheque leaf after free limits.")
chatbot.add_faq("fixed deposit open?", "Use the YONO app, net banking, or visit a branch.")
chatbot.add_faq("rd max tenure?", "10 years.")
chatbot.add_faq("fd max tenure?", "5 years.")
chatbot.add_faq("home loan apply?", "Apply via the YONO app or visit a branch with documents.")
chatbot.add_faq("loan interest rate?", "It varies depending on the type of loan and starts from 8.50%.")
chatbot.add_faq("reset atm pin?", "You can reset it using an SBI ATM, YONO app, or net banking.")
chatbot.add_faq("credit card eligibility?", "Eligibility depends on income, credit score, and other factors.")
chatbot.add_faq("stop cheque?", "Visit your branch or use net banking for cheque stop payment.")
chatbot.add_faq("fd premature withdrawal?", "Premature withdrawal is allowed with a penalty on interest.")
chatbot.add_faq("my bank name sbi full form?", "State Bank of India.")
chatbot.add_faq("branch name?", "Nagarabhavi Branch.")
chatbot.add_faq("user name holder?", "Nischay Sai D R.")
chatbot.add_faq("my age?", "19 years.")
chatbot.add_faq("close account?", "Go to bank and submit the Account closing application.")
chatbot.add_faq("deposit cheque?", "Go to nearest bank and put it in cheque box.")
chatbot.add_faq("my account number?", "8060 8498 XXXX.")
chatbot.add_faq("ifsc code?", "SBIN00003070.")
chatbot.add_faq("bank address?", "Kengunte circle, Nagarabhavi, Bangalore-560072.")
chatbot.add_faq("full account details?", "\nAccount Details :\n\nName: Nischay Sai D R.\nAccount Number: 8060 8498 XXXX.\nIFSC Code: SBIN00003070.")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get_response", methods=["POST"])
def get_response():
    user_query = request.json["query"]
    answer, matched_question = chatbot.get_answer(user_query.lower())

    if answer:
        # Return the answer and ask if the user wants to update
        return jsonify({
            "response": answer,
            "matched_question": matched_question,
            "update_prompt": f"Do you want to update the answer for '{matched_question}'?"
        })
    else:
        # If no answer, provide a Google search link
        google_search_url = f"https://www.google.com/search?q={user_query.replace(' ', '+')}"
        return jsonify({
            "response": None,
            "google_search": google_search_url,
            "message": "No answer found. You can try searching on Google."
        })

@app.route("/update_answer", methods=["POST"])
def update_answer():
    data = request.json
    question = data.get("question")
    new_answer = data.get("new_answer")
    if question and new_answer:
        chatbot.update_answer(question, new_answer)
        return jsonify({"message": "Answer updated successfully."})
    return jsonify({"message": "Invalid data provided."}), 400


# Function to open the browser
def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000/")

if __name__ == "__main__":
    # Open the browser in a separate thread
    threading.Timer(1.0, open_browser).start()
    app.run(debug=True)
