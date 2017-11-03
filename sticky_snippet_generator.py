import random
import numpy as np
import os
import glob
import random


class DataUtil:
    op_class = 6
    def __init__(self):
        self.items = ['A', 'B', 'C', 'D']
        self.item_len = 40
        self.sticky_dict = {'A': ['C'],
                            'B': ['D'],
                            'C': ['A'],
                            'D': ['B']}

    def get_stickiness(self, input):
        length = len(input)
        if length % 2 == 1:
            return -1
        return self._check_stickiness(input[:length/2], input[length-1:length/2-1:-1])

    def _check_stickiness(self, input1, input2):
        k = 0
        if len(input1) != len(input2):
            return k
        for i in range(len(input1)):
            if input1[i] not in self.items:
                print('Invalid data : Data should consist of "ABCD"')
            if input2[i] not in self.sticky_dict[input1[i]]:  # Checks whether reverse of second half is sticky
                return k
            k += 1
        return k

    def gen_stick_palindrome(self):
        data = self.item_len * [None]
        for i in range(self.item_len/2):
            item = random.choice(self.items)
            item_stick = random.choice(self.sticky_dict[item])
            # print('item : {}'.format(item))
            # print('item : {}'.format(item_stick))
            data[i] = item
            data[self.item_len - 1 - i] = item_stick
        return data

    def mutate_stick_pal(self, stick_pal, mutation_rate, from_ends):
        result = []
        len_pal = len(stick_pal)
        for i in range(len_pal):
            selected_char = stick_pal[i]
            print('(i,selected_char): {}'.format((i, selected_char)))
            if i in range(from_ends) or i in range(len_pal - from_ends, len_pal):
                prob = [(mutation_rate / (len(self.items) - 1)) if char != selected_char else 1 - mutation_rate for char
                        in self.items]
            else:
                prob = [(1.0 / (len(self.items) - 1)) if char != selected_char else 0.0 for char in self.items]
            print(prob)
            result.append(np.random.choice(a=self.items, p=prob))
        return ''.join(result)

    def gen_data(self, num_snippets, mutation_rate, from_ends, output_file):
        data = []
        with open(output_file, 'w') as f:
            for i in range(num_snippets):
                stick_pal = self.gen_stick_palindrome()
                result = self.mutate_stick_pal(stick_pal, mutation_rate, from_ends)
                if i != num_snippets - 1:
                    result = result + "\n"
                data.append(result)
                # print(data)
                # print(len(data))
            f.writelines(data)

    def create_data_folder(self, folder_name, no_files, start_file_index, num_snippets, mutation_rate, from_ends):
        base_name = 'data'
        ext='.txt'
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        for i in range(no_files):
            data_gen.gen_data(num_snippets = num_snippets, mutation_rate = mutation_rate, from_ends = from_ends,
                              output_file = os.path.join(folder_name, base_name+str(start_file_index+i)+ext))

    def gen_ihot(self, data):
        y=[]
        for i in range(self.op_class):
            y.append(0)
        # print(data)
        # print('stickiness {}'.format(self.get_stickiness(data)))
        k = self.get_stickiness(data) + 1
        for i in range(self.op_class):
            if i == (k/2):
                y[i] = 1
        # print(y)
        return(y)


    def load_data(self, floder_name):
        data_folder = []
        for filename in glob.glob(os.path.join(floder_name, '*.txt')):
            data_file = []
            with open(filename) as file:
                for line in file:
                    data_item_x = line.strip()
                    if (len(data_item_x) != self.item_len):
                        print("Improper file {}".format(filename))
                        data_file = None
                        break
                    data_item_int_x = [ord(char) - ord('A') for char in data_item_x]
                    data_item_y = self.gen_ihot(data_item_x)
                    data_file.append((data_item_int_x, data_item_y))
            if(data_file):
                # print(data_file_x)
                data_folder += data_file
        # print(len(data_folder_x))
        # print(data_folder_x)
        # print(len(data_folder_y))
        # print(data_folder_y)
        return Data(data = data_folder)

class Data:
    def __init__(self, data):
        self.total_data = data

    def get_epoch_data(self, batchsize):
        if not self.total_data:
            return None
        self.batched_data = []
        current_batch = 0
        tot_items = len(self.total_data)
        random.shuffle(self.total_data)
        num_batches = tot_items/batchsize
        while current_batch < num_batches:
            batch_data = []
            index_start = current_batch * batchsize
            for i in range(batchsize):
                batch_data.append(self.total_data[index_start + i])
            current_batch += 1
            self.batched_data.append(batch_data)
        return self.batched_data



data_gen = DataUtil()
# print(data.check_stickiness('AABDC', 'CCDBA'))
# print(data.is_stick_palindrome('AABDCDBDCC'))
# print(data_gen.gen_stick_palindrome())
# print(data_gen.gen_data(num_snippets = 1000, mutation_rate = 0.6, from_ends = 4, output_file = 'data.txt'))
# data_gen.create_data_folder(folder_name = 'sample', no_files = 2, start_file_index = 2, num_snippets = 1000, mutation_rate = 0.6, from_ends = 4)
data_dir = data_gen.load_data('sample')
# print(len(data.data))
# print(len(data.get_epoch_data(batchsize=100)))
batched_data = data_dir.get_epoch_data(batchsize=100)
print(batched_data[0])
print(data_dir.batched_data[0])
