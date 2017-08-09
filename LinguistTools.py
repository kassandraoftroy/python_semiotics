# -*- coding: utf-8 -*-
from operator import itemgetter
import random
import en_core_web_sm
from gensim import models
import numpy as np
import os

characters = "1 2 3 4 5 6 7 8 9 0 * & ^ ) ( } { | ] [ ' < > @ . ! ? # $ % , ~ ≈ ç √ ∫ µ ∂ ß ˚ å ø - ∂ ¨ ƒ ¥ © ˙ ∑ œ π : ; – º _ ª • § ¶ ∞ ¢ £ ™ ¡ ª – ≠ “ ‘ « “ π ø ˆ ¨ ¥ † ∑ ® œ ¡ ™ £ ÷ ≥ ç √ ≤ ∫ µ Ω ˜ ∆ ƒ ˙ © ƒ ¥ ¨ å"
stop_char = characters.split()
stop_char.append('"')
model = models.KeyedVectors.load_word2vec_format(os.path.join(os.path.dirname(__file__), "10kVec.txt"), binary=False)

class Copy_Cat:

	def __init__(self, raw):
		self.nlp = en_core_web_sm.load()
		text = open(raw, "r")
		all1 = text.read()
		text.close()
		all2 = all1.replace("\n", "Z")
		sentences = []
		s = ""
		for char in all2:
			if char != "Z":
				s = s + char 
			else:
				if s != "":
					sentences.append(s)
				s = ""
		pipeline = self.nlp.pipe([unicode(sent) for sent in sentences], n_threads=-1)
		tokenized_sents = [pipeline.next() for i in range (0, len(sentences))]
		self.lines = [tokenized_sents[i] for i in range (0, len(tokenized_sents)) if "ROOT" in [token.dep_ for token in tokenized_sents[i]]] 
		self.R_words = [[token.text for token in line] for line in self.lines]
		self.R_grammar = [[token.dep_ for token in line] for line in self.lines]
		self.R_children = [self.lines[i][self.R_grammar[i].index("ROOT")].children for i in range (0, len(self.lines))]
		self.R_children_words = [[token.text for token in self.R_children[i]] for i in range (0, len(self.lines))]
		self.R_children_grammar = [[self.lines[i][self.R_words[i].index(item)].dep_ for item in self.R_children_words[i]] for i in range (0, len(self.lines))]

	def response(self, paragraph_input):
		formatted_input_sentences = []
		words_input = paragraph_input.split()
		####clean sentences
		sentence = []
		A_sentences = []
		B_sentences = []
		for word in words_input:
			sentence.append(word.lower())
			if word[-1] in [".", "!", "?"]:
				A_sentences.append(sentence)
				sentence = []
		if sentence != []:
			A_sentences.append(sentence)
		for s in A_sentences:
			sentence = []
			for word in s:
				for character in word:
					if character in stop_char:
						word = word.replace(character, "")
				sentence.append(word)
			B_sentences.append(sentence)
		for s in B_sentences:
			good_words = []
			for word in s:
				try:
					model[word]
					good_words.append(word)
				except:
					pass
			if s != '':
				formatted_input_sentences.append(" ".join(good_words))
		output_sentences = []
		for Q in formatted_input_sentences:
			try:
				Q_tokens = self.nlp(Q.decode(encoding='UTF-8',errors= "strict"))
				Q_words = [token.text for token in Q_tokens]
				Q_vecs = [model[word.lower()] for word in Q_words]
				Q_avg = np.sum(np.array(Q_vecs), axis=0)
				Q_grammar = [token.dep_ for token in Q_tokens]
				Q_root = Q_tokens[Q_grammar.index("ROOT")].text.lower()
				Q_children = Q_tokens[Q_grammar.index("ROOT")].children
				Q_children_words = [token.text for token in Q_children]
				Q_children_grammar = [Q_tokens[Q_words.index(item)].dep_ for item in Q_children_words]
			except:
				print "!!! input error !!!"
				return find_sim()
			tier_1_similarity = []
			tier_2_similarity = []
			for X in range (0, len(self.lines)):
				if self.R_children_grammar[X] == Q_children_grammar:
					try:
						R_vecs = [model[word] for word in self.R_words[X]]
						R_avg = np.sum(np.array(R_vecs), axis=0)
						R_root = self.lines[X][self.R_grammar[X].index("ROOT")].text			
						count = 0
						piecewise_sim = 0
						for i in range (0, len(Q_children_grammar)):
							count += 1
							A_avg = np.sum(np.array([model[token.text.lower()] for token in Q_tokens[Q_words.index(Q_children_words[i])].subtree]), axis=0)
							B_avg = np.sum(np.array([model[token.text] for token in self.lines[X][self.R_words[X].index(self.R_children_words[X][i])].subtree]), axis=0)
							piecewise_sim += np.dot(A_avg, B_avg)/(np.linalg.norm(A_avg) * np.linalg.norm(B_avg))
						if count > 0:
							similarity_1 = piecewise_sim/float(count)
						else:
							similarity_1 = 0.5
						similarity_2 = np.dot(model[Q_root], model[R_root])/(np.linalg.norm(model[Q_root]) * np.linalg.norm(model[R_root]))
						similarity_3 = np.dot(Q_avg, R_avg)/(np.linalg.norm(Q_avg) * np.linalg.norm(R_avg))
						tier_1_similarity.append((self.lines[X], (similarity_1+similarity_2+similarity_3)/3.0))
					except:
						pass
				else:
					try:
						R_vecs = [model[word] for word in self.R_words[X]]
						R_avg = np.sum(np.array(R_vecs), axis=0)
						R_root = self.lines[X][self.R_grammar[X].index("ROOT")].text			
						count = 0
						piecewise_sim = 0
						for i in range (0, len(Q_children_grammar)):
							count += 1
							A_avg = np.sum(np.array([model[token.text.lower()] for token in Q_tokens[Q_words.index(Q_children_words[i])].subtree]), axis=0)
							B_avg = np.sum(np.array([model[token.text] for token in self.lines[X][self.R_words[X].index(self.R_children_words[X][i])].subtree]), axis=0)
							piecewise_sim += np.dot(A_avg, B_avg)/(np.linalg.norm(A_avg) * np.linalg.norm(B_avg))
						if count > 0:
							similarity_1 = piecewise_sim/float(count)
						else:
							similarity_1 = 0.5
						similarity_2 = np.dot(model[Q_root], model[R_root])/(np.linalg.norm(model[Q_root]) * np.linalg.norm(model[R_root]))
						similarity_3 = np.dot(Q_avg, R_avg)/(np.linalg.norm(Q_avg) * np.linalg.norm(R_avg))
						tier_2_similarity.append((self.lines[X], (similarity_1+similarity_2+similarity_3)/3.0))
					except:
						pass

			if tier_1_similarity != []:
				output = sorted(tier_1_similarity, key=itemgetter(1), reverse=True)[0][0]
			else:
				output = sorted(tier_2_similarity, key=itemgetter(1), reverse=True)[0][0]
			output_sentences.append(" ".join([token.text for token in output]) + "   ")
		final_output = " ".join(output_sentences)
		return final_output 

class Walk:

	def __init__(self, A, B):
		self.A = A.lower()
		self.B = B.lower()

	def take_walk(self):
		words = [self.A, self.B]
		try:
			z = [model[words[0]], model[words[1]]]
		except:
			z = "!!! input error: not in vocabulary !!!"
			return z 
		search_words = [words[0]]
		all_found_words = [words[0]]
		word_tracking = []
		count = 0
		N = 15
		while True:
			round_track = []
			count += 1
			new_words = []
			similarity = []
			for i in range (0, len(search_words)):
				X = model.most_similar(positive=[search_words[i]], topn=N)
				for k in range (0, len(X)):
					if X[k][0] not in all_found_words:
						round_track.append((search_words[i], X[k][0]))
						if X[k][0] not in new_words:
							new_words.append(X[k][0])
							similarity.append(float(model.similarity(words[1], X[k][0])))
			word_tracking.append(round_track)
			search_words = []
			for i in range (0, 10):
				search_words.append(new_words[similarity.index(max(similarity))])
				new_words.remove(new_words[similarity.index(max(similarity))])
				similarity.remove(max(similarity))
			for i in range (0, 5):
				random_index = random.randint(0, (len(new_words) - 1))
				search_words.append(new_words[random_index])
				new_words.remove(new_words[random_index])
			all_found_words.extend(search_words)
			if words[1] in search_words:
				break 
			if count == 16:
				count = 0
				N += (3 * N)
				search_words = [words[0]]
				all_found_words = []
				word_tracking = []
		outputs = ["number of rounds: %s" %count, "number of words searched: %s" %len(set(all_found_words))]
		target_words = [words[1]]
		path = [[words[1]]]
		printout_path = []
		for i in range (1, len(word_tracking) + 1):
			round_path = []
			for k in range (0, len(path)):
				for j in range (0, len(word_tracking[-i])):
					if word_tracking[-i][j][1] in target_words:
						round_path.append(word_tracking[-i][j][0])
			target_words = list(set(round_path))
			path.append(target_words)
		outputs.append(path)
		for i in range (1, len(path) + 1):
			printout_path.append(path[-i][-1])
		outputs.append(printout_path)
		midpoint = []
		mid_index = (len(path) / 2.0)
		if len(path) % 2 != 0:
			midpoint.extend(path[int(mid_index - 0.5)])
		else:
			midpoint.extend(path[int(mid_index)])
			midpoint.extend(path[int(mid_index - 1)])
		outputs.append(list(set(midpoint)))
		return outputs

