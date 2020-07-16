# importing regex and random libraries
import re
import random

class AlienBot:
  # potential greetings
  greetings = ("Hello", "Hi", "Good day")
  # potential negative responses
  negative_responses = ("no", "nope", "nah", "naw", "not a chance", "sorry")
  # keywords for exiting the conversation
  exit_commands = ("quit", "pause", "exit", "goodbye", "bye", "later")
  # random starter questions
  random_questions = (
        "Why are you here? ",
        "Are there many humans like you? ",
        "What do you consume for sustenance? ",
        "Is there intelligent life on this planet? ",
        "Does Earth have a leader? ",
        "What planets have you visited? ",
        "What technology do you have on this planet? "
    )

  def __init__(self):
    self.alienbabble = {'describe_planet_intent': [r'.*\s*your planet.*', r'^(describe).*planet.*'],
                        'answer_why_intent': [r'^(why).*'],
                        'cubed_intent': [r'.*cube.*(\d+)']
                            }

  # Define .greet() below:
  def greet(self):
    self.name = input("What's your name?")
    will_help = input(random.choice(list(self.greetings)) + str(self.name) + ", I'm Etcetera. I'm not from this planet. Will you help me learn about your planet? If you want to end the conversation, please, respond with the one of the following: " + ", ".join(list(self.exit_commands)) + "\n")
    if will_help.lower() in list(self.negative_responses):
      print("Ok, have a nice Earth day!")
      return
    else:
      self.chat()

  # Define .make_exit() here:
  def make_exit(self, reply):
    esc = False
    for com in self.exit_commands:
      if com in reply:
        print("Ok, have a nice Earth day!")
        esc = True
    return esc

  # Define .chat() next:
  def chat(self):
    reply = ""
    while not self.make_exit(reply):
      reply = input(random.choice(self.random_questions)).lower()
      self.match_reply(reply)
      reply = input()

  # Define .match_reply() below:
  def match_reply(self, reply):
    intent = ""
    found = False
    number = 0
    for k, v in list(self.alienbabble.items()):
      for rexp in v:
        if re.match(rexp, reply):
          intent = k
          found = True
          number = re.match(rexp, reply).group(1)
    if found and intent == "describe_planet_intent":
      return self.describe_planet_intent()
    if found and intent == "answer_why_intent":
      return self.answer_why_intent()
    if found and intent == "cubed_intent":
      return self.cubed_intent(int(number))
    else:
      return self.no_match_intent()

  # Define .describe_planet_intent():
  def describe_planet_intent(self):
    responses = ("My planet is a utopia of diverse organisms and species. ", "I am from Opidipus, the capital of the Wayward Galaxies. ")
    print(random.choice(responses))

  # Define .answer_why_intent():
  def answer_why_intent(self):
    responses = ("I come in peace. ", "I am here to collect data on your planet and its inhabitants. ", "I heard the coffee is good. ")
    print(random.choice(responses))
       
  # Define .cubed_intent():
  def cubed_intent(self, number):
    print(f'The cube of {number} is {number**3}. My race is good at math')

  # Define .no_match_intent():
  def no_match_intent(self):
    responses = ("Please tell me more", "Tell me more", "Why do you say that?", "Can you elaborate?", "Interesting, can you tell me more?", "I see", "Why?")
    print(random.choice(responses))

# Create an instance of AlienBot below:
bot = AlienBot()
bot.greet()