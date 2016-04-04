mport pandas
import json


'''
Boyer Moore String Search implementation in Python
 __author__: Pawda
 Date: 2016-04-04
'''

# method bad character to find the shift bit. len(ref) == len(read)
def bad_cha(ref,read):
    for i in range(1, len(read)+1):
        if not read[-i] == ref[-i]:
            for j in range(1,len(read)-i+1):
                if ref[-i] == read[-(i+j)]:
                    return j
            return len(read)-i+1
    return "success"

# method good suffix to find the shift bit. len(ref) == len(read)
def good_suffix(ref,read):
    suffix = ""

    # check if ref == read: if not, get the suffix
    for i in range(1, len(read)+1):
        if read[-i] == ref[-i]:
            suffix = read[-i:]
        else:
            i-=1
            break
    if suffix == read:
        return "success"
    post = read[:-i]
    l_suffix = len(suffix)
    # check if the suffix occurs in the post part
    for j in range(len(post)-l_suffix+1):
        if j == 0:
            if post[-(j+l_suffix):] == suffix:
                return j+l_suffix
        else:
            if post[-(j+l_suffix):-j] == suffix:
                return j+l_suffix

    # check if the suffix of suffix occurs in the prefix of prefix
    for k in range(l_suffix-1):
        if suffix[-(l_suffix-k-1):] == post[:l_suffix-k-1]:
            return len(read)-(l_suffix-(k+1))

    # if no other matches we can directly move to the last part
    return len(read)

# this is the main function to find the ***matches*** by BM algorthm
def search(ref,read):
    r_list = []
    i = 0
    l_read = len(read)
    while i+l_read <= len(ref):
        result = bad_cha(ref[i:l_read+i],read)
        if result == "success":
            n_dict = dict()
            n_dict['alignment'] = read
            n_dict['No'] = i+1
            r_list.append(n_dict)
            i += l_read
            continue
        else:
            result_gs = good_suffix(ref[i:l_read+i],read)
            result = max(result_gs,result)
        i += result
    print r_list

# main execution of the python program.
if __name__ == "__main__":
    tw = pandas.read_csv('mini_twitter.csv')
    for each_value in tw.value:
        result = json.loads(each_value)
        pattern = "the"
        search(result['text'],pattern)

