import random
import time

tokens = ["A", "B", "C", "D", "E", "F"]


def create_rand_sign():
    random.shuffle(tokens)

    dollar_pos = 0
    for i in range(len(tokens) - 2, -1, -1):
        if tokens[i] >= tokens[i + 1]:
            dollar_pos = i+1
            break

    pre_segment = tokens[:dollar_pos + 1]
    post_segment = tokens[dollar_pos + 1:]

    post_segment.sort()
    final_tokens = pre_segment + ["$"] + post_segment

    return "".join(final_tokens)


def create_conseq_sign(comp_list):
    if len(comp_list) == 0:
        print("No initial sign!")
        return comp_list

    final_sign_list = ["$"] + tokens
    final_sign = "".join(final_sign_list)

    cur_sign = comp_list[0]
    while cur_sign != final_sign:
        dollar_index = cur_sign.find('$')
        # print(f'dollor index: {dollar_index}')
        if dollar_index <= 0:
            break
        i = random.randint(0, dollar_index - 1)
        char_i = cur_sign[i]
        # print(f'randomly chosen index: {i}, char: {char_i}')

        # Create a list of candidate indices.
        candidates = list(range(i, len(cur_sign) + 1))

        if len(candidates) > 1:
            # Candidate i gets 50% probability.
            weight_for_i = 0.5
            # The rest share the remaining 50% equally.
            remaining_weight = 0.5
            num_remaining = len(candidates) - 1
            weights = [weight_for_i] + [remaining_weight / num_remaining] * num_remaining
        else:
            weights = [1]
        # Give more probability to the same index for more string output
        new_index = random.choices(candidates, weights=weights, k=1)[0]

        # print(f'chosen new index: {new_index}')
        if new_index == i:
            comp_list.append((cur_sign, char_i))
            continue

        if new_index >= dollar_index:
            new_index = dollar_index
            for index in range(dollar_index + 1, len(cur_sign)):
                if ord(cur_sign[index]) > ord(char_i):
                    break
                else:
                    new_index += 1

            # print(f'final new index: {new_index}')
            char_to_move = char_i
            # print(f'pre_sign: {cur_sign[:i]}, post_sign: {cur_sign[i + 1:]}')
            cur_sign = cur_sign[:i] + cur_sign[i + 1:]
            new_index_adjusted = new_index
            cur_sign = cur_sign[:new_index_adjusted] + char_to_move + cur_sign[new_index_adjusted:]
        else:
            char_to_move = char_i
            cur_sign = cur_sign[:i] + cur_sign[i + 1:]
            new_index_adjusted = new_index
            cur_sign = cur_sign[:new_index_adjusted] + char_to_move + cur_sign[new_index_adjusted:]

        # print(cur_sign)
        comp_list.append((cur_sign, char_i))

        # Loop continues until cur_specsign matches final_specsign.
    return comp_list


def find_appropriate_string(comp_list):
    string_list = []
    counter = len(comp_list) - 1

    while counter > 0:
        cur_sign = comp_list[counter][0]
        next_sign = comp_list[counter - 1][0] if counter - 1 > 0 else comp_list[counter - 1]
        # print(f'next sign: {next_sign}')

        moved_from_index = cur_sign.find(comp_list[counter][1])
        # print(f'moving character: {comp_list[counter][1]}')

        if len(string_list) == 0:
            string_list.append(str(cur_sign[moved_from_index]))
            counter -= 1
            continue

        moved_to_index = next_sign.find(comp_list[counter][1])
        # print(f'moved to index: {moved_to_index}')
        # Iterate only over a copy of string_list to avoid modification issues.
        original_strings = string_list.copy()
        for string in original_strings:
            dollar_index = next_sign.find('$')
            range_left_char = next_sign[moved_to_index - 1] if moved_to_index > 0 else None
            # print(f'range left char: {range_left_char}')
            range_left_index = string.find(range_left_char) if range_left_char is not None else -1
            # print(f'range left index: {range_left_index}')

            range_right_char = next_sign[moved_to_index + 1] if moved_to_index + 1 < dollar_index else None
            # print(f'range right char: {range_right_char}')
            range_right_index = string.find(range_right_char) if range_right_char is not None else len(string)
            # print(f'range right index: {range_right_index}')

            for i in range(range_left_index, range_right_index):
                new_string = string[:i + 1] + str(comp_list[counter][1]) + string[i + 1:]
                string_list.append(new_string)
                # print(f'appending string: {new_string}')
            # Remove the original string after processing.
            string_list.remove(string)

        counter -= 1
        # time.sleep(0.5)

    return string_list


if __name__ == "__main__":
    sign_comp = []

    # create random specsign computation
    sign_comp.append(create_rand_sign())

    create_conseq_sign(sign_comp)
    print(sign_comp)

    strings = find_appropriate_string(sign_comp)
    print(f'size of string_list: {len(strings)}')

