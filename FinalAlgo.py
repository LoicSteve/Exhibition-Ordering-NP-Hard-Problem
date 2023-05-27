# Author: Loic steve
def segregator():
    for i in range(1, len(lines)):
        temp = lines[i].split()
        temp[2] = set(temp[2:])
        del temp[3:]
        temp.insert(0, str(i - 1))
        if temp[1] == 'L':
            frames.append(temp)
        else:
            portrait.append(temp)


def portrait_merger(portrait1, portrait2=[]):
    t = []
    t.append('{} {}'.format(portrait1[0], portrait2[0]))
    t.append('P')
    if len(portrait2):
        new_set = portrait1[3].union(portrait2[3])
    else:
        new_set = portrait1[3]
    t.append(str(len(new_set)))
    t.append(new_set)
    frames.append(t)


def frame_generator():
    head = 0
    pt = 1
    while len(portrait):
        if not portrait[head][3] & portrait[pt][3]:
            portrait_merger(portrait[head], portrait[pt])
            del portrait[head]
            del portrait[pt - 1]
            pt = 1
        elif pt + 1 < len(portrait):
            pt += 1
        elif head + 1 < len(portrait) - 1:
            head += 1
            pt = head + 1
        else:
            portrait_len = len(portrait)
            mod = portrait_len % 2
            if mod == 0:
                for i in range(0, portrait_len - 1, 2):
                    portrait_merger(portrait[i], portrait[i + 1])
            else:
                for i in range(0, portrait_len - 2, 2):
                    portrait_merger(portrait[i], portrait[i + 1])
                portrait_merger(portrait[portrait_len - 1])
            del portrait[0:]


def calculate_local_satisfaction(frameglass1, frameglass2):
    common_tags = len(set(frameglass1[3]) & set(frameglass2[3]))
    tags_only_in_fg1 = len(set(frameglass1[3]) - set(frameglass2[3]))
    tags_only_in_fg2 = len(set(frameglass2[3]) - set(frameglass1[3]))
    return min(common_tags, tags_only_in_fg1, tags_only_in_fg2)


def optimize_frameglass_order(frames):
    num_frames = len(frames)
    best_order = []
    best_score = 0

    def backtrack(order, used_frames):
        nonlocal best_order, best_score

        if len(order) == num_frames:
            score = sum(calculate_local_satisfaction(frames[i], frames[j]) for i, j in zip(order[:-1], order[1:]))
            if score > best_score:
                best_score = score
                best_order = order.copy()
            return

        for i in range(num_frames):
            if i not in used_frames:
                used_frames.add(i)
                order.append(i)
                backtrack(order, used_frames)
                order.pop()
                used_frames.remove(i)

    backtrack([], set())

    return [frames[i][0] for i in best_order]


def main():
    final = []
    unhung_frames = frames.copy()
    unhung_frames = unhung_frames[1:]
    final.append(frames[0][0])
    index = 0

    while len(unhung_frames):
        highest_recorded_common_tags = 0
        index_of_recorded_common_tags = 0

        for i in range(1, len(unhung_frames)):
            total_common_tags = calculate_local_satisfaction(frames[index], unhung_frames[i])
            if total_common_tags > highest_recorded_common_tags:
                highest_recorded_common_tags = total_common_tags
                index_of_recorded_common_tags = i

        final.append(unhung_frames[index_of_recorded_common_tags][0])
        index = frames.index(unhung_frames[index_of_recorded_common_tags])
        del unhung_frames[index_of_recorded_common_tags]

    with open('Output_file.txt', 'w') as f:
        f.write(str(len(final)) + "\n")
        for value in final:
            f.write(value + "\n")


if __name__ == "__main__":
    input_file = "0_example.txt" # 1
    # input_file = "10_computable_moments.txt" # 1549
    # input_file = "11_randomizing_paintings.txt" # 434235
    # input_file = "110_oily_portraits.txt"  # 416326
    # input_file = "1_binary_landscapes.txt" # 202689

    # total score = 1054800
    frames = []
    portrait = []

    with open(input_file, "r") as f:
        lines = f.read().splitlines()

    segregator()
    frame_generator()
    main()
