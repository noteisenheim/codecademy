import numpy as np
import re
import random
from test_model import encoder_model, decoder_model, num_decoder_tokens, num_encoder_tokens, input_features_dict, target_features_dict, reverse_target_features_dict, max_decoder_seq_length, max_encoder_seq_length

class ChatBot:
	negative_commands = ["no", "don't", "never", "nah"]
	exit_commands = ["quit", "esc", "exit", "stop", "q"]
	start_commands = ["Hello! Don't mind to talk?", "Good day. Let's talk about weather!", "Oh, hi there! Do you want to talk a bit?"]

	def start_chat(self):
		resp = input(random.choice(self.start_commands)).lower()
		if resp in self.negative_commands:
			print("Oh, that's a pity. Anyway, was nice to meet you.\n")
			return
		else:
			while not self.make_exit(resp):
				resp = input(self.generate_response(resp) + "\n").lower()

	def make_exit(self, reply):
		found = False
		for cmnd in self.exit_commands:
			if cmnd in reply:
				found = True
		return found

	def string_to_matrix(self, reply):
		tokens = re.findall(r"[\w']+|[^\s\w]", reply)
		matrix = np.zeros((1, max_encoder_seq_length, num_encoder_tokens), dtype='float32')
		for timestep, token in enumerate(tokens):
			if token in input_features_dict:
				matrix[0, timestep, input_features_dict[token]] = 1.0
		return matrix

	def generate_response(self, reply):
		reply = self.string_to_matrix(reply)

		# Encode the input as state vectors.
		states_value = encoder_model.predict(reply)

		# Generate empty target sequence of length 1.
		target_seq = np.zeros((1, 1, num_decoder_tokens))
		# Populate the first token of target sequence with the start token.
		target_seq[0, 0, target_features_dict['<START>']] = 1.

		# Sampling loop for a batch of sequences
		# (to simplify, here we assume a batch of size 1).
		decoded_sentence = ''

		stop_condition = False
		while not stop_condition:
			# Run the decoder model to get possible 
			# output tokens (with probabilities) & states
			output_tokens, hidden_state, cell_state = decoder_model.predict(
			[target_seq] + states_value)

			# Choose token with highest probability
			sampled_token_index = np.argmax(output_tokens[0, -1, :])
			sampled_token = reverse_target_features_dict[sampled_token_index]
			decoded_sentence += " " + sampled_token

			# Exit condition: either hit max length
			# or find stop token.
			if (sampled_token == '<END>' or len(decoded_sentence) > max_decoder_seq_length):
				stop_condition = True

			# Update the target sequence (of length 1).
			target_seq = np.zeros((1, 1, num_decoder_tokens))
			target_seq[0, 0, sampled_token_index] = 1.

			# Update states
			states_value = [hidden_state, cell_state]

		decoded_sentence = decoded_sentence.replace("<START>", "")
		decoded_sentence = decoded_sentence.replace("<END>", "")
		return decoded_sentence


bot = ChatBot()
bot.start_chat()