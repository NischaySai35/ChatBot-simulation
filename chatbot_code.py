from rapidfuzz import process

# Define a class for the Node in the linked list
class Node:
    def __init__(self, question, answer):
        self.question = question
        self.answer = answer
        self.next = None

# Define a class for the hash table
class FAQHashTable:
    def __init__(self, size=10):
        self.size = size
        self.table = [None] * size  # Array for hash table

    def hash_function(self, key):
        return sum(ord(ch) for ch in key) % self.size

    def insert(self, question, answer):
        index = self.hash_function(question)
        if self.table[index] is None:
            self.table[index] = Node(question, answer)
        else:
            current = self.table[index]
            while current:
                if current.question == question:
                    current.answer = answer  # Update if question already exists
                    return
                if current.next is None:  # Append if at the end of the list
                    current.next = Node(question, answer)
                    return
                current = current.next

    def search(self, query):
        # Get all questions stored in the hash table
        all_questions = []
        for bucket in self.table:
            current = bucket
            while current:
                all_questions.append(current.question)
                current = current.next
        
        # Use rapidfuzz to find the closest match to the query
        best_match = process.extractOne(query, all_questions, score_cutoff=80)
        if best_match:
            # Retrieve the answer for the matched question
            matched_question = best_match[0]
            index = self.hash_function(matched_question)
            current = self.table[index]
            while current:
                if current.question == matched_question:
                    return current.answer, matched_question
                current = current.next
        return None, None

# Define a class for managing the chatbot
class FAQChatBot:
    def __init__(self):
        self.faq_table = FAQHashTable()

    def add_faq(self, question, answer):
        self.faq_table.insert(question, answer)

    def get_answer(self, query):
        answer, matched_question = self.faq_table.search(query)
        return answer, matched_question

    def update_answer(self, question, new_answer):
        self.faq_table.insert(question, new_answer)

# Example usage
#print("WELCOME TO SBI CHATBOT!!!, Ask any questions\n")
if __name__ == "__main__":
    chatbot = FAQChatBot()
    
    # Simulate user queries
    while True:
        user_query = input("\nAsk your question: ")
        if user_query.lower() in ["exit", "quit", 'q']:
            print("Thank you for using the FAQ Chatbot. Goodbye!")
            break
        
        answer, matched_question = chatbot.get_answer(user_query.lower())
        
        if answer:
            print("Chatbot:", answer)
            update_choice = input(f"Do you want to update the answer for '{matched_question}'? (yes/no): ").strip().lower()
            if update_choice == "y":
                new_answer = input(f"Enter the new answer for '{matched_question}': ").strip()
                chatbot.update_answer(matched_question, new_answer)
                print("Answer updated successfully.")
        else:
            print(f"You can find your answer through this link, click link!\nhttps://www.google.com/search?q={user_query.replace(' ','+')}")
