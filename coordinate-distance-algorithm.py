import math

coords_list = ((380, 6), (380, 7), (378, 16), (378, 17), (378, 18), (378, 19), (378, 20),
               (378, 21), (378, 22), (378, 23), (378, 51), (378, 52), (375, 74), (374, 79),
               (374, 80), (373, 91), (373, 95), (372, 100), (372, 101), (129, 145))


def coord_sort(cords_input):
    coord_sorted = list()
    coord_unsorted = list(cords_input)
    curr_coord = ()
    tempcurr_cord = ()
    hypot = 99999

    for val in coord_unsorted:
        valhypot = math.sqrt(val[0] * val[1])
        hypot = min(valhypot, hypot)

        if hypot == valhypot:
            curr_coord = val

    coord_unsorted.remove(curr_coord)
    coord_sorted.append(curr_coord)

    for x in range(9999):
        if len(coord_unsorted) == 0:
            break

        tempcurr_cord = coord_unsorted[0]
        hypot = 9999
        minval = 9999
        for val in coord_unsorted:
            valhypot = math.sqrt(abs((curr_coord[0] - val[0]) * (curr_coord[1] - val[1])))
            hypot = min(valhypot, hypot)

            if hypot == valhypot:
                if tempcurr_cord[0] == val[0]:
                    minval = min(minval, abs(curr_coord[1] - val[1]))
                    if abs(curr_coord[1] - val[1]) == minval:
                        tempcurr_cord = val

                elif tempcurr_cord[1] == val[1]:
                    minval = min(minval, abs(curr_coord[0] - val[0]))
                    if abs(curr_coord[0] - val[0]) == minval:
                        tempcurr_cord = val

                else:
                    tempcurr_cord = val

        curr_coord = tempcurr_cord
        coord_unsorted.remove(curr_coord)
        coord_sorted.append(curr_coord)

        if len(coord_unsorted) < 0:
            break

    return coord_sorted


print(coord_sort(coords_list))
