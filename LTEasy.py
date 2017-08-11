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
model = models.KeyedVectors.load_word2vec_format("/Users/Earth/django_test/17kVec.txt", binary=False)

class Copy_Cat:

	def __init__(self, raw):
		text = open(raw, "r")
		all1 = text.read()
		text.close()
		all2 = all1.replace("\n", "Z")
		self.sentences = []
		s = ""
		for char in all2:
			if char != "Z":
				s = s + char 
			else:
				if s != "":
					self.sentences.append(s)
				s = ""

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
			if s != '' and good_words!=[]:
				formatted_input_sentences.append(" ".join(good_words))
		if formatted_input_sentences == []:
			return "sorry I don't understand any of '%s'" %(paragraph_input)
		output_sentences = []
		for Q in formatted_input_sentences:
			Q_avg = np.sum(np.array([model[word] for word in Q.split()]), axis=0)/np.linalg.norm(np.sum(np.array([model[word] for word in Q.split()]), axis=0))
			similarity = []
			for R in self.sentences:
				try:
					R_avg = np.sum(np.array([model[word] for word in R.split()]), axis=0)/np.linalg.norm(np.sum(np.array([model[word] for word in R.split()]), axis=0))
					similarity.append((R, np.dot(Q_avg, R_avg)))
				except:
					pass
			output_sentences.append(sorted(similarity, key=itemgetter(1), reverse=True)[0][0] + " ")
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