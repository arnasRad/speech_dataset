import properties


class ShortSentencesMerger:
    def __init__(self, sentences_list):
        self.sentences = sentences_list
        self.sentences_size = len(self.sentences)
        self.valid_sentences = [self.sentences[0]]
        self.skip_iteration = False

    def __sentence_is_shorter_than_min_length(self, sentence):
        return len(sentence) < properties.min_dataset_sentence_len

    def __is_not_second_to_last_iteration(self, index):
        return index != (self.sentences_size - 2)

    def __merge_last_sentence_to_shorter_neighbor(self, iteration_index, current_sentence):
        if len(self.valid_sentences[-1]) < len(self.sentences[iteration_index + 1]):
            self.valid_sentences[-1] += " " + current_sentence
            self.valid_sentences.append(self.sentences[-1])
        else:
            next_sentence = self.sentences[iteration_index + 1]
            new_sentence = current_sentence + " " + next_sentence
            self.valid_sentences.append(new_sentence)

    def __process_last_iteration(self, iteration_index, current_sentence):
        if self.skip_iteration:
            self.valid_sentences.append(self.sentences[-1])

        if self.__sentence_is_shorter_than_min_length(current_sentence):
            self.__merge_last_sentence_to_shorter_neighbor(iteration_index, current_sentence)
        else:
            self.valid_sentences.append(current_sentence)
            self.valid_sentences.append(self.sentences[-1])
        return self.valid_sentences

    def __merge_sentence_to_shorter_neighbor(self, iteration_index, current_sentence):
        if len(self.valid_sentences[-1]) < len(self.sentences[iteration_index + 1]):
            self.valid_sentences[-1] += " " + current_sentence
        else:
            next_sentence = self.sentences[iteration_index + 1]
            new_sentence = current_sentence + " " + next_sentence
            self.valid_sentences.append(new_sentence)
            self.skip_iteration = True

    def __process_iteration(self, iteration_index, current_sentence):
        if self.skip_iteration:
            self.skip_iteration = False
            return

        if self.__sentence_is_shorter_than_min_length(current_sentence):
            self.__merge_sentence_to_shorter_neighbor(iteration_index, current_sentence)
        else:
            self.valid_sentences.append(current_sentence)

    # sentences that are shorter than minimal length are merged to either the previous or the next sentence in the list
    #   depending on which one is shorter
    # the sentence is merged to the previous sentence by appending it at the end of the previous sentence
    # the sentence is merged to the next sentence by prepending it at the start of the next sentence
    # returns a list of sentences with valid length
    def merge_short_sentences(self):
        for i, sentence in enumerate(self.sentences[1:-1], start=1):
            if self.__is_not_second_to_last_iteration(i):
                self.__process_iteration(i, sentence)
            else:
                self.__process_last_iteration(i, sentence)
        return self.valid_sentences
